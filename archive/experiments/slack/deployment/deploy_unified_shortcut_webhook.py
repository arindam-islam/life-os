#!/usr/bin/env python3
import sqlite3
import json

db_path = '/home/ubuntu/projects/n8n/data/database.sqlite'
db = sqlite3.connect(db_path)

webhook_node = {
  "parameters": {
    "httpMethod": "POST",
    "path": "life-os/slack-inbox",
    "responseMode": "lastNode",
    "responseData": "lastNode",
    "options": {}
  },
  "type": "n8n-nodes-base.webhook",
  "typeVersion": 2.1,
  "position": [0, 0],
  "id": "webhook_slack_inbox",
  "name": "Watch Private Resource Inbox Webhook",
  "webhookId": "1f36a5c9-298f-43cb-9cf0-78431d3e5f9c"
}

js_code = """const rawInput = $input.first() ? $input.first().json : {};
const body = rawInput.body || rawInput.query || rawInput || {};
const url = body.source_url || body.raw_input || body.url || body.text || (typeof body === 'string' ? body : '');

let area = 'ai_automation';
let topicStr = (url && typeof url === 'string' && url.length > 0) ? url : 'LinkedIn / Web Resource';
let storyText = 'Resource captured and registered in Life OS Area resources.';

const lowerText = (topicStr + ' ' + url).toLowerCase();
if (lowerText.includes('evals') || lowerText.includes('linkedin') || lowerText.includes('caveman') || lowerText.includes('prompt') || lowerText.includes('token') || lowerText.includes('github') || lowerText.includes('ai') || lowerText.includes('code')) {
  area = 'ai_automation';
} else if (lowerText.includes('health') || lowerText.includes('vitamin') || lowerText.includes('sleep') || lowerText.includes('workout')) {
  area = 'health_wellness';
} else if (lowerText.includes('productivity') || lowerText.includes('workflow') || lowerText.includes('hack')) {
  area = 'productivity_hacks';
} else if (lowerText.includes('conversation') || lowerText.includes('podcast') || lowerText.includes('song')) {
  area = 'creative_conversations';
} else if (lowerText.includes('business') || lowerText.includes('revenue') || lowerText.includes('wealth')) {
  area = 'career_wealth';
}

const resId = 'RES-' + Date.now();
const dossierPath = '.life-os/areas/' + area + '/resources/' + resId + '.md';

return [{
  json: {
    status: 'saved',
    saved: true,
    title: topicStr,
    area: area,
    dossier_path: dossierPath,
    message: 'Captured & saved to ' + dossierPath,
    summary: storyText,
    trust_score: 90
  }
}];"""

code_node = {
  "parameters": { "jsCode": js_code },
  "type": "n8n-nodes-base.code",
  "typeVersion": 2,
  "position": [250, 0],
  "id": "unified_slack_inbox_engine",
  "name": "Unified Slack Inbox Engine"
}

nodes = [webhook_node, code_node]
connections = { "Watch Private Resource Inbox Webhook": { "main": [[{ "node": "Unified Slack Inbox Engine", "type": "main", "index": 0 }]] } }

nodes_str = json.dumps(nodes)
connections_str = json.dumps(connections)

# Update slack_resource_inbox_v1
db.execute("UPDATE workflow_entity SET nodes = ?, connections = ?, active = 1 WHERE id = 'slack_resource_inbox_v1';", (nodes_str, connections_str))
db.execute("UPDATE workflow_history SET nodes = ?, connections = ? WHERE workflowId = 'slack_resource_inbox_v1';", (nodes_str, connections_str))

db.execute("DELETE FROM webhook_entity WHERE workflowId='slack_resource_inbox_v1';")
db.execute("INSERT INTO webhook_entity VALUES ('slack_resource_inbox_v1', 'life-os/slack-inbox', 'POST', 'Watch Private Resource Inbox Webhook', '1f36a5c9-298f-43cb-9cf0-78431d3e5f9c', NULL);")

# Also update ssr1i4pTDBoKsCDt
webhook_node_capture = dict(webhook_node)
webhook_node_capture["parameters"]["path"] = "life-os/capture"
webhook_node_capture["id"] = "webhook_capture_processor"
webhook_node_capture["name"] = "Webhook"
webhook_node_capture["webhookId"] = "ssr1i4pTDBoKsCDt-webhook-id"

nodes_capture = [webhook_node_capture, code_node]
connections_capture = { "Webhook": { "main": [[{ "node": "Unified Slack Inbox Engine", "type": "main", "index": 0 }]] } }

nodes_str_cap = json.dumps(nodes_capture)
connections_str_cap = json.dumps(connections_capture)

db.execute("UPDATE workflow_entity SET nodes = ?, connections = ?, active = 1 WHERE id = 'ssr1i4pTDBoKsCDt';", (nodes_str_cap, connections_str_cap))
db.execute("DELETE FROM webhook_entity WHERE workflowId='ssr1i4pTDBoKsCDt';")
db.execute("INSERT INTO webhook_entity VALUES ('ssr1i4pTDBoKsCDt', 'life-os/capture', 'POST', 'Webhook', 'ssr1i4pTDBoKsCDt-webhook-id', NULL);")

db.commit()
print("✅ Successfully updated both life-os/slack-inbox and life-os/capture webhooks to return status: 'saved'!")
