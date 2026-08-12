# Life OS infrastructure

This repository defines the local/production-shaped Docker Compose services for
Life OS. Deployment to the Oracle server is intentionally a separate, manual
step.

## Services

### n8n

The existing n8n image, loopback-only port mapping, `.env` injection, persistent
workflow/credential data (`./data:/home/node/.n8n`), and shared files
(`./files:/files`) are preserved. Variables used by OmniRoute can continue to
come from the ignored `.env` file or n8n's persisted credential store.

The default network is the pre-existing external network `n8n_default`.
Compose attaches n8n and the enricher to it but does not create, recreate, or
delete it. The independently managed `omniroute` container must remain attached
to this network. Never use `docker compose up --remove-orphans` or `docker
compose down --remove-orphans` on this project because OmniRoute may carry old
Compose project labels even though it is now independently managed.

### YouTube enricher v1

`youtube-enricher` is a separate, non-root container. It is available to n8n at
`http://youtube-enricher:8080` on the Compose network. There is deliberately no
host `ports` mapping, so the API is not published by Docker.

Endpoints:

- `GET /health` returns service and runtime dependency status, and reports
  unhealthy if `yt-dlp` or Deno is unavailable.
- `POST /enrich` accepts JSON in the form
  `{"url":"https://www.youtube.com/watch?v=..."}`.

Successful enrichment returns structured video, channel, publication,
engagement, caption-availability, chapter, and extractor metadata. Caption
track URLs are intentionally omitted because they are temporary signed URLs.
The service runs `yt-dlp` with `--skip-download` and `--no-playlist`; it does not
download the video, subtitles, or playlist entries.

The image includes Deno and the `yt-dlp` default dependency group required for
current YouTube JavaScript challenge support. Extraction has bounded socket,
retry, subprocess, and web-worker timeouts.

## Configuration and operation

The real `.env`, `data/`, `config/`, and `files/` paths are intentionally ignored
by Git. Do not add secrets to `.env.example` or commit runtime data.

Validate the configuration with a safe environment template:

```sh
N8N_ENV_FILE=.env.example docker compose --env-file .env.example config
```

Build and deploy only the enricher when a Docker daemon and the external
`n8n_default` network are available. Targeting the service avoids recreating the
already-running n8n container:

```sh
docker compose build youtube-enricher
docker compose up -d --no-deps youtube-enricher
docker exec n8n wget -qO- http://youtube-enricher:8080/health
```

A full `docker compose up -d --build` does not manage the external network or
the separately managed OmniRoute container, but it may recreate n8n when its
tracked configuration changes. That causes downtime and is unnecessary for the
initial enricher rollout.

Run deterministic API tests inside the built image:

```sh
docker build -t life-os-youtube-enricher:test youtube-enricher
docker run --rm \
  -v "$PWD/youtube-enricher/tests:/app/tests:ro" \
  life-os-youtube-enricher:test \
  python -m unittest discover -s tests -v
```

Live YouTube extraction must be checked from the production host before enabling
an n8n workflow because YouTube may apply IP reputation, geographic, consent, or
authentication restrictions. Do not bypass access controls or add browser
cookies to this service.
