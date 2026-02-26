# Paper Trail Zero

Secure evidence intake and whistleblower platform powered by AI. Upload images or PDFs, get AI-powered analysis via Venice AI (Qwen3-VL), and generate formal police reports using CrewAI agents.

## Features

- Secure file upload (JPEG, PNG, PDF)
- AI image analysis via Venice AI (Qwen3-VL)
- PDF text extraction
- Automated police report generation via CrewAI (Llama 3.3 70b)
- Admin dashboard for evidence review
- Persistent chat interface

## Prerequisites

- Python 3.12+
- A [Venice AI](https://venice.ai) API key

## Local Development

```bash
# Clone the repository
git clone https://github.com/randyfong/Whistleblower.git
cd Whistleblower

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your VENICE_API_KEY

# Run the application
python main.py
```

The app will be available at `http://localhost:8000`. The admin panel is at `http://localhost:8000/admin`.

## Docker

> Replace `<your-dockerhub-username>` below with your Docker Hub username (e.g. `johndoe`).
> If you prefer GitHub Container Registry, replace `docker.io/<your-dockerhub-username>` with `ghcr.io/<your-github-username>`.

### Build the Image

The image must target `linux/amd64` (Akash providers run on amd64). The Dockerfile already enforces this via `--platform=linux/amd64`, but if you're on Apple Silicon (M1/M2/M3) you may also pass the platform flag explicitly:

```bash
docker build --platform linux/amd64 -t <your-dockerhub-username>/whistleblower:v0.1.0 .
```

### Run Locally with Docker

```bash
docker run -d \
  -p 8000:8000 \
  -e VENICE_API_KEY=your_api_key_here \
  <your-dockerhub-username>/whistleblower:v0.1.0
```

### Push to a Container Registry

**Docker Hub:**

```bash
# Log in to Docker Hub (you'll be prompted for your password)
docker login

# Push the image
docker push <your-dockerhub-username>/whistleblower:v0.1.0
```

**GitHub Container Registry (alternative):**

```bash
# Create a personal access token at https://github.com/settings/tokens
# with the "write:packages" scope, then log in:
echo $GITHUB_TOKEN | docker login ghcr.io -u <your-github-username> --password-stdin

# Tag and push
docker tag <your-dockerhub-username>/whistleblower:v0.1.0 ghcr.io/<your-github-username>/whistleblower:v0.1.0
docker push ghcr.io/<your-github-username>/whistleblower:v0.1.0
```

## Deploy to Akash Network

This repository includes an Akash SDL file (`deploy.yaml`) for deploying to the decentralized cloud.

### Prerequisites

- [Akash CLI](https://akash.network/docs/) installed
- An Akash wallet with AKT tokens
- The Docker image pushed to GHCR (see above)

### Steps

1. **Edit `deploy.yaml`** — update the `image` to your pushed image and set your `VENICE_API_KEY`:

   ```yaml
   env:
     - "VENICE_API_KEY=your_actual_key"
   ```

2. **Create a deployment**:

   ```bash
   akash tx deployment create deploy.yaml --from your-wallet --chain-id akashnet-2
   ```

3. **Wait for bids**, then accept one:

   ```bash
   akash query market bid list --owner <your-address> --dseq <deployment-sequence>
   akash tx market lease create --from your-wallet --dseq <dseq> --gseq 1 --oseq 1 --provider <provider-address>
   ```

4. **Send the manifest**:

   ```bash
   akash provider send-manifest deploy.yaml --from your-wallet --provider <provider-address> --dseq <dseq>
   ```

Alternatively, deploy via the [Akash Console](https://console.akash.network) by uploading `deploy.yaml`.

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `VENICE_API_KEY` | API key for Venice AI services | Yes |
