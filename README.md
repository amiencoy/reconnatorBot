
# 🕵️‍♂️ Reconnator: Cloud-Native Reconnaissance Bot

**Reconnator** is a lightweight, cloud-native reconnaissance bot designed for modern bug hunters and security engineers. It automates the process of discovering subdomains and seamlessly integrates into modern infrastructure (Docker/Kubernetes) to provide continuous monitoring and alerting.

Unlike traditional scripts, Reconnator is built with resilience in mind, featuring built-in retry mechanisms for unstable external APIs and a fully containerized architecture.

## ✨ Key Features

- **Automated Subdomain Enumeration**: Fetches transparent certificate logs via `crt.sh` to uncover hidden assets.
- **Resilient Engine**: Built-in timeout handling and automatic retries to bypass API gateway errors (HTTP 502/503/504).
- **Agentic Notifications**: Native support for Telegram Webhooks to alert you immediately when new assets are discovered.
- **Cloud-Native Ready**: Fully Dockerized with an Alpine-based footprint.
- **Kubernetes Native**: Comes with a ready-to-deploy Helm Chart to run as a scheduled `CronJob` in any K8s cluster.

---

## 🚀 Quick Start

You can run Reconnator in three different ways depending on your environment.

### Option 1: Running Locally (Python)

Ensure you have Python 3.11+ installed. It is highly recommended to use a virtual environment.

```bash
# Clone the repository
git clone [https://github.com/yourusername/reconnator.git](https://github.com/yourusername/reconnator.git)
cd reconnator

# Setup Virtual Environment
python3 -m venv venv
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

# Run the Bot
python src/main.py --target example.com

```

### Option 2: Running via Docker

No Python required. Just build and run the container.

```bash
# Build the Docker image
docker build -t reconnator:v1 .

# Run the container (it will automatically be removed after execution)
docker run --rm reconnator:v1 --target example.com

```

### Option 3: Kubernetes & Helm (Continuous Recon)

Deploy Reconnator as a scheduled CronJob in your Kubernetes cluster (e.g., K3s, Minikube, or EKS/GKE).

```bash
# Navigate to the Helm directory
cd deploy/helm

# Install the chart (Runs daily by default)
helm install recon-bot . --set targetDomain="example.com"

```

*Note: You can easily modify the cron schedule and target domain by editing `deploy/helm/values.yaml`.*

---

## 🔔 Setting Up Telegram Alerts

To receive automated alerts directly to your phone, set the following environment variables before running the script:

**Locally:**

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
python src/main.py --target example.com

```

**Via Helm:**
Update your `values.yaml` or inject them during deployment:

```bash
helm install recon-bot . \
  --set targetDomain="example.com" \
  --set telegram.botToken="your_bot_token" \
  --set telegram.chatId="your_chat_id"

```

---

## 📂 Project Structure

```text
.
├── .github/workflows/    # CI/CD pipelines
├── deploy/helm/          # Kubernetes Helm Chart
├── src/                  # Core Python modules
│   ├── modules/          # Fetchers and Notifiers
│   ├── utils/            # Loggers
│   └── main.py           # Application Entrypoint
├── Dockerfile            # Alpine-based container blueprint
└── requirements.txt      # Python dependencies

```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

*Built with code and coffee by amiencoy*
