# open-webui-proxy

A proxy that  provides authentication against Entra ID using a SPN and handles the actual API requests.
The proxy is build using `FastAPI`, which is a `Python` based framework for creating RESTful APIs.

# Start the proxy for local development & testing

This can be easily done using `fastapi CLI`, but first you have to create your personal `.env` (just copy the [.env-example](.env-sample)) and a virtual environment using `UV`. This environment will load all necessary packages, which are part of the [pyproject.toml](pyproject.toml).

```
uv init open-webui-proxy
uv run --env-file .env fastapi dev app/main.py
```

You now could validate if the endpoint is available using `curl`, such like `curl -s http://localhost:8000 | grep 'ready to serve'`.

# Include new packages

if you want to include new packages, please use `uv`.

```
uv add httpx
uv sync
```

Don't forget to render the [requirements.txt](requirements.txt) and [requirements-dev.txt](requirements-dev.txt) again.

```
uv pip compile -o requirements.txt pyproject.toml
uv pip compile pyproject.toml --extra dev -o requirements-dev.txt
```

# Start the container using Docker or Podman

Just use the following commands and have a look at the [Dockerfile](Dockerfile).

```
docker build -t open-webui-proxy:1.0.0 .
docker run --name open-webui-proxy -p 8000:8000 -d open-webui-proxy:1.0.0
```

Or just run the prebuild image from my `

```
docker run --name open-webui-proxy -p 8000:8000 -d docker://docker.io/avwsolutions/open-webui-proxy:latest
```

# Start the solution using Docker or Podman compose

Just have a look at the [compose.yaml](compose.yaml) for more info.

```
docker compose up -d
```

# Testing 

Currently working on a `pytest` to  be included, but you may test this using the following `curl` command, which is `Pwsh` friendy.

```
curl http://localhost:8000/v1/chat/completions -H "Content-Type: application/json" `-d '{"model":"gpt-4o","messages":[{"role":"user","content":"hello"}]}'
```
