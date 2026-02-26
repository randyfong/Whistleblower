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

This repository includes an Akash SDL file (`deploy.yaml`) for deploying to the [Akash Network](https://akash.network) — a decentralized cloud. No CLI or terminal needed. Everything below is done through a web browser.

### What You'll Need

1. **Your Docker image pushed to a registry** — Follow the [Docker](#docker) section above first. You need the image name (e.g. `yourname/whistleblower:v0.1.0`)
2. **Your Venice AI API key** — Get one at [https://venice.ai](https://venice.ai)

That's it. Akash Console offers a **free trial with a managed wallet** — no crypto, no browser extensions, no tokens to buy.

### Step-by-Step Deployment

#### 1. Sign Up for Akash Console

- Go to **[https://console.akash.network](https://console.akash.network)**
- Click **"Sign In"** in the top right
- Sign in with your **GitHub** or **Google** account
- You'll automatically get a **managed wallet** with free trial credits — no setup needed

#### 2. Start a New Deployment

- Click the **"Deploy"** button
- Select **"Upload SDL"** (you will paste your own configuration)

#### 3. Edit the SDL Before Pasting

Open the `deploy.yaml` file from this repo and make two changes before pasting it:

**a) Set your Docker image** — Replace the `image` line with your actual image:

```yaml
image: <your-dockerhub-username>/whistleblower:v0.1.0
```

**b) Set your Venice API key** — Fill in the value:

```yaml
env:
  - "VENICE_API_KEY=your_actual_api_key_here"
```

Then paste the full edited SDL into the Console editor.

#### 4. Create the Deployment

- Click **"Create Deployment"**
- If prompted, approve the transaction (this reserves a small deposit for your deployment)

#### 5. Pick a Provider

- After a few seconds, you'll see a list of **bids** from providers (these are servers that want to host your app)
- Each bid shows a **price per month** — pick one that looks good (cheaper is fine, they all work)
- Click **"Accept Bid"**

#### 6. Wait for It to Start

- The Console will show your deployment status
- Once it says **"Active"**, your app is running
- You'll see a **URL** assigned to your deployment (something like `*.provider.akash.network`) — click it to open your app

#### 7. Check Logs (If Something Goes Wrong)

- On your deployment page, click the **"Logs"** tab
- This shows what the container is printing — useful for debugging

### Updating Your Deployment

If you push a new Docker image version (e.g. `v0.1.2`):

1. Go to your deployment in the Console
2. Click **"Update"**
3. Change the `image` tag in the SDL to the new version
4. Click **"Update Deployment"**

### Closing Your Deployment

When you're done and want to stop hosting:

1. Go to your deployment in the Console
2. Click **"Close"**
3. Your remaining deposit will be refunded

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `VENICE_API_KEY` | API key for Venice AI services | Yes |
