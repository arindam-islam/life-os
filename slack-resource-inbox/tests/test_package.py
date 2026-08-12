import json
import pathlib
import unittest


PACKAGE_DIR = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW_PATH = PACKAGE_DIR / "workflow.json"
SCHEMA_PATH = PACKAGE_DIR / "event-envelope.schema.json"
README_PATH = PACKAGE_DIR / "README.md"
DEPLOYMENT_PATH = PACKAGE_DIR / "DEPLOYMENT.md"
MANIFEST_PATH = PACKAGE_DIR / "activation-manifest.json"
APPROVAL_PATH = PACKAGE_DIR / "APPROVAL.md"
CHANNEL_ID = "C0BPQBNTK8R"
WORKSPACE_ID = "T0BLLQ18E5C"


def walk(value):
    yield value
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


class SlackResourceInboxPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = json.loads(WORKFLOW_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.readme = README_PATH.read_text(encoding="utf-8")
        cls.deployment = DEPLOYMENT_PATH.read_text(encoding="utf-8")
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        cls.approval = APPROVAL_PATH.read_text(encoding="utf-8")
        cls.nodes = {node["name"]: node for node in cls.workflow["nodes"]}

    def test_workflow_is_inactive_and_scoped_to_exact_private_channel(self):
        self.assertFalse(self.workflow["active"])
        trigger = self.nodes["Watch Private Resource Inbox"]
        self.assertEqual(trigger["type"], "n8n-nodes-base.slackTrigger")
        self.assertEqual(trigger["parameters"]["trigger"], ["message"])
        self.assertFalse(trigger["parameters"]["watchWorkspace"])
        self.assertEqual(
            trigger["parameters"]["channelId"]["value"], CHANNEL_ID
        )

    def test_workflow_contains_no_bound_credentials_or_secrets(self):
        self.assertTrue(all("credentials" not in node for node in self.workflow["nodes"]))
        serialized_keys_and_values = [
            str(item).lower() for item in walk(self.workflow)
        ]
        for forbidden in ("xoxb-", "xapp-", "signing_secret", "password"):
            self.assertFalse(
                any(forbidden in item for item in serialized_keys_and_values),
                forbidden,
            )

    def test_handoff_uses_loopback_authenticated_webhook_without_bound_secret(self):
        handoff = self.nodes["Forward to Authenticated Capture Webhook"]
        self.assertEqual(handoff["type"], "n8n-nodes-base.httpRequest")
        self.assertEqual(handoff["parameters"]["method"], "POST")
        self.assertEqual(
            handoff["parameters"]["url"],
            "http://127.0.0.1:5678/webhook/life-os/capture",
        )
        self.assertEqual(
            handoff["parameters"]["genericAuthType"], "httpHeaderAuth"
        )
        self.assertNotIn("credentials", handoff)
        self.assertTrue(handoff.get("retryOnFail", False))
        self.assertEqual(handoff.get("maxTries"), 3)
        self.assertEqual(handoff.get("waitBetweenTries"), 5000)
        self.assertFalse(handoff.get("continueOnFail", False))
        self.assertNotIn("n8n-nodes-base.executeWorkflow", json.dumps(self.workflow))

    def test_connections_form_trigger_normalize_handoff_chain(self):
        self.assertEqual(
            self.workflow["connections"]["Watch Private Resource Inbox"]["main"][0][0][
                "node"
            ],
            "Normalize and Guard Inbox Event",
        )
        self.assertEqual(
            self.workflow["connections"]["Normalize and Guard Inbox Event"]["main"][0][
                0
            ]["node"],
            "Suppress Previously Captured Message",
        )
        self.assertEqual(
            self.workflow["connections"]["Suppress Previously Captured Message"][
                "main"
            ][0][0]["node"],
            "Forward to Authenticated Capture Webhook",
        )
        self.assertEqual(
            self.workflow["connections"]["Suppress Previously Captured Message"][
                "main"
            ][1],
            [],
        )

    def test_deduplication_is_persistent_scoped_and_fail_closed(self):
        node = self.nodes["Suppress Previously Captured Message"]
        self.assertEqual(node["type"], "n8n-nodes-base.removeDuplicates")
        self.assertEqual(node["typeVersion"], 2)
        parameters = node["parameters"]
        self.assertEqual(
            parameters["operation"], "removeItemsSeenInPreviousExecutions"
        )
        self.assertEqual(parameters["logic"], "removeItemsWithAlreadySeenKeyValues")
        self.assertEqual(parameters["dedupeValue"], "={{ $json.deduplication_key }}")
        self.assertEqual(parameters["options"], {"scope": "node", "historySize": 10000})

    def test_handoff_maps_observed_capture_processor_contract(self):
        body = self.nodes["Forward to Authenticated Capture Webhook"]["parameters"][
            "jsonBody"
        ]
        for field in (
            "raw_input",
            "normalized_input",
            "content",
            "source_type",
            "source_url",
            "title",
            "type",
            "deduplication_key",
            "source_metadata",
        ):
            self.assertIn(field, body)

    def test_normalizer_has_dedupe_safety_and_minimal_file_handling(self):
        code = self.nodes["Normalize and Guard Inbox Event"]["parameters"]["jsCode"]
        for required_fragment in (
            CHANNEL_ID,
            WORKSPACE_ID,
            "bot_message",
            "message_changed",
            "message_deleted",
            "deduplication_key",
            "approval_required_for_external_actions",
            "slack_file",
            "size_bytes",
        ):
            self.assertIn(required_fragment, code)
        self.assertIn("[^\\s<>()|>]", code)
        for forbidden_fragment in ("url_private", "url_private_download", "token"):
            self.assertNotIn(forbidden_fragment, code)

    def test_schema_matches_channel_source_and_approval_guard(self):
        properties = self.schema["properties"]
        self.assertEqual(properties["source"]["const"], "slack_resource_inbox")
        source_properties = properties["source_metadata"]["properties"]
        self.assertEqual(source_properties["workspace_id"]["const"], WORKSPACE_ID)
        self.assertEqual(source_properties["channel_id"]["const"], CHANNEL_ID)
        self.assertTrue(
            properties["routing"]["properties"][
                "approval_required_for_external_actions"
            ]["const"]
        )

    def test_runbook_has_approval_test_and_non_destructive_rollback(self):
        normalized_runbook = " ".join(self.deployment.split())
        for required in (
            "Approval gates",
            "Acceptance test while inactive",
            "Replay the same normalized test event once",
            "Deactivate only",
            "Do not restart or recreate n8n or OmniRoute",
        ):
            self.assertIn(required, normalized_runbook)
        self.assertIn("not live", self.readme.lower())
        self.assertIn("six synthetic events", self.readme)

    def test_activation_manifest_matches_workflow_and_has_no_bindings(self):
        self.assertTrue(self.manifest["must_import_inactive"])
        self.assertEqual(self.manifest["slack"]["workspace_id"], WORKSPACE_ID)
        self.assertEqual(self.manifest["slack"]["channel_id"], CHANNEL_ID)
        self.assertEqual(self.manifest["slack"]["oauth_scopes"], ["groups:history"])
        self.assertTrue(
            all(item["binding"] is None for item in self.manifest["credential_bindings"])
        )
        dedupe = self.manifest["deduplication"]
        self.assertEqual(dedupe["history_size"], 10000)
        self.assertFalse(dedupe["discarded_output_connected"])
        self.assertTrue(
            self.manifest["production_invariants"][
                "capture_processor_must_not_be_modified"
            ]
        )

    def test_approval_is_bounded_and_does_not_authorize_external_actions(self):
        normalized = " ".join(self.approval.split())
        for required in (
            "read-only access",
            "credential store",
            "one clearly labelled production capture",
            "activating only the Slack Resource Inbox adapter",
            "does not authorize Slack posts",
            "changes to the existing Capture Processor",
            "container recreation",
            "bypassing any human approval gate",
        ):
            self.assertIn(required, normalized)


if __name__ == "__main__":
    unittest.main()
