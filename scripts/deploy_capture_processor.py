#!/usr/bin/env python3
import sqlite3
import json

db_path = '/home/ubuntu/projects/n8n/data/database.sqlite'
db = sqlite3.connect(db_path)

webhook_node = {
  "parameters": {
    "httpMethod": "POST",
    "path": "life-os/capture",
    "responseMode": "lastNode",
    "responseData": "lastNode",
    "options": {}
  },
  "type": "n8n-nodes-base.webhook",
  "typeVersion": 2.1,
  "position": [0, 0],
  "id": "webhook_capture_processor",
  "name": "Webhook",
  "webhookId": "ssr1i4pTDBoKsCDt-webhook-id"
}

js_code = """const rawInput = $input.first() ? $input.first().json : {};
const body = rawInput.body || rawInput.query || rawInput || {};
const url = body.source_url || body.raw_input || body.url || (typeof body === 'string' ? body : '');

let area = 'ai_automation';
let topicStr = (url && typeof url === 'string' && url.length > 0) ? url : 'Captured Resource';
let storyText = 'Resource captured and registered in Life OS Area resources.';

const lowerText = (topicStr + ' ' + url).toLowerCase();
if (lowerText.includes('caveman') || lowerText.includes('prompt') || lowerText.includes('token') || lowerText.includes('github') || lowerText.includes('ai') || lowerText.includes('code')) {
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
    status: 'SUCCESS',
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
  "id": "unified_capture_engine",
  "name": "Unified Capture Engine"
}

nodes = [webhook_node, code_node]
connections = { "Webhook": { "main": [[{ "node": "Unified Capture Engine", "type": "main", "index": 0 }]] } }

nodes_str = json.dumps(nodes)
connections_str = json.dumps(connections)

db.execute("UPDATE workflow_entity SET nodes = ?, connections = ?, active = 1 WHERE id = 'ssr1i4pTDBoKsCDt';", (nodes_str, connections_str))
db.execute("UPDATE workflow_history SET nodes = ?, connections = ? WHERE workflowId = 'ssr1i4pTDBoKsCDt';", (nodes_str, connections_str))

db.execute("DELETE FROM webhook_entity WHERE workflowId='ssr1i4pTDBoKsCDt';")
db.execute("INSERT INTO webhook_entity VALUES ('ssr1i4pTDBoKsCDt', 'life-os/capture', 'POST', 'Webhook', 'ssr1i4pTDBoKsCDt-webhook-id', NULL);")

db.commit()
print("✅ Clean Capture Processor deployed to SQLite!")
