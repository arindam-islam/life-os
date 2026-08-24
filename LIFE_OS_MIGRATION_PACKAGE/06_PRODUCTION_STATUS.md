# Production Status


Date:

2026-08-24


## OCI

Host:

n8n-server


OS:

Ubuntu 24.04


Status:

ONLINE


## Running Services


### n8n

Status:
Healthy


Purpose:
Automation engine


### Status Bridge

Status:
Healthy


Purpose:
Health telemetry


### Status View

Status:
Running


Purpose:
Operating dashboard


### YouTube Enricher

Status:
Healthy


Purpose:
Content metadata processing


## Verification

Health checks passed:

n8n /healthz

status bridge /healthz


## Deployment Rule

Production changes require:

1. Local testing
2. Git commit
3. Pull on OCI
4. Verification
