# Life OS infrastructure

This repository defines the local/production-shaped Docker Compose services for
Life OS. Deployment to the Oracle server is intentionally a separate, manual
step.

## Services

### n8n

The existing n8n image, loopback-only port mapping, `.env` injection, persistent
workflow/credential data (`./data:/home/node/.n8n`), and shared files
(`./files:/files`) are preserved. Variables used by OmniRoute can continue to
come from the ignored `.env` file or n8n's persisted credential store. The
default Compose network is not marked internal, so n8n retains outbound access
to OmniRoute and other configured APIs.

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

Build and run locally when a Docker daemon is available:

```sh
docker compose build youtube-enricher
docker compose up -d
docker compose exec n8n wget -qO- http://youtube-enricher:8080/health
```

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
