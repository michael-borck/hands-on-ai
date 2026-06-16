# Host a Shared Ollama (for Educators)

Sometimes you want a whole class pointing at one model server. Every student
(including the ones on Google Colab) just sets two environment variables and
starts working. No local installs, no "it runs differently on my laptop", no GPU
on the student side. You host the model once and everyone shares it.

This is optional, and it is a bit more setup for you, the educator. If your whole
class is in one room on one network, plain local Ollama is simpler and you can
skip this page entirely. Reach for this recipe when students are remote, on
Colab, or on locked-down machines where installing things is painful.

## The shape

Ollama has no built-in authentication. If you expose port `11434` to the
internet, anyone who finds it can use your server. So the plan is:

1. Run Ollama, but do not expose its port publicly.
2. Put a small reverse proxy in front of it that checks an
   `Authorization: Bearer <key>` header and serves everything over HTTPS.
3. Hand students the proxy URL and the class key.

Students then set two environment variables:

- `HANDS_ON_AI_SERVER`: the public HTTPS URL of your proxy.
- `HANDS_ON_AI_API_KEY`: the shared class key.

The library sends the key as a bearer token, the proxy checks it, and only then
does the request reach Ollama.

## docker-compose.yml

This brings up two services. Ollama keeps its models in a named volume and is
only reachable on the internal Docker network. Caddy is the public face: it
terminates HTTPS (it can fetch certificates automatically for a real domain) and
enforces the bearer token.

```yaml
services:
  ollama:
    image: ollama/ollama
    restart: unless-stopped
    volumes:
      - ollama_models:/root/.ollama
    # Note: we deliberately do NOT publish 11434 to the host.
    # Only the caddy service can reach it, over the internal network.

  caddy:
    image: caddy:2
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    environment:
      - OLLAMA_DOMAIN=${OLLAMA_DOMAIN}
      - CLASS_KEY=${CLASS_KEY}
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config
    depends_on:
      - ollama

volumes:
  ollama_models:
  caddy_data:
  caddy_config:
```

Set `OLLAMA_DOMAIN` and `CLASS_KEY` in a `.env` file next to this compose file
(and keep that file out of git):

```bash
OLLAMA_DOMAIN=ollama.example.edu
CLASS_KEY=replace-with-a-long-random-string
```

## Caddyfile

The proxy logic is short: if the `Authorization` header is not exactly
`Bearer <the class key>`, respond `401`. Otherwise pass the request through to
Ollama on the internal network.

```caddyfile
{$OLLAMA_DOMAIN} {
	# Reject anything without the correct bearer token.
	@unauthorized {
		not header Authorization "Bearer {$CLASS_KEY}"
	}
	respond @unauthorized "Unauthorized" 401

	# Authorized requests go to Ollama on the internal network.
	reverse_proxy ollama:11434
}
```

A note on this: Caddy's header-matching syntax has changed between versions, and
exact bearer-token comparison can be fiddly. Treat the block above as
illustrative and verify it against the current Caddy docs for the version you are
running. Test it yourself before handing the URL to students: a misconfigured
matcher can either lock everyone out or, worse, let everyone in.

## Pull the models on the server

The container starts with no models. Pull them once on the host. RAG needs an
embedding model in addition to a chat model, so pull both:

```bash
docker compose exec ollama ollama pull llama3
docker compose exec ollama ollama pull nomic-embed-text
```

Pull any other models your assignments use the same way. They live in the named
volume, so they survive container restarts.

## What students do

Students do not install anything. They set the two environment variables to the
values you give them. In a terminal:

```bash
export HANDS_ON_AI_SERVER="https://ollama.example.edu"
export HANDS_ON_AI_API_KEY="replace-with-a-long-random-string"
```

In a Colab or Jupyter notebook, set them before importing the library. See
[Providers and configuration](providers.md) for every way to set these, and
[Using notebooks](notebooks.md) for the Colab specifics.

Then confirm the connection:

```bash
handsonai doctor
```

If `doctor` reports a healthy connection and finds the models, they are ready to
go.

## Before you do this

Be honest with yourself about what you are taking on:

- You are now running an internet-exposed service. Use a real domain with valid
  TLS, not a self-signed certificate, or notebooks and clients may reject it.
- Keep the key out of git. Put it in `.env` or a secrets store, never in a
  committed file or a shared notebook.
- Rotate the key each term, and any time it leaks. Treat it like a password,
  because that is what it is.
- Watch your sizing. One GPU shared across thirty students running at once can
  crawl. Test under realistic concurrency before assignments are due.
- If abuse is a concern, consider rate limits at the proxy, or issuing a
  per-student key instead of one shared class key, so you can revoke one without
  disrupting everyone.

For many classes, a shared local Ollama on the classroom network, or a cloud
provider API key, is simpler and perfectly fine. This recipe is specifically for
when you want a single hosted endpoint that any student, anywhere, can point at.
