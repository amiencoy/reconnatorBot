---
# Reconnator: Cloud-Native DevSecOps ChatOps Bot

**Reconnator** is a lightweight, cloud-native reconnaissance bot designed for modern bug hunters and security engineers. Transitioning from a passive script to a fully interactive DevSecOps assistant, it orchestrates vulnerability scanning and seamlessly integrates into modern infrastructure (Docker/Kubernetes).

Unlike traditional scripts, Reconnator is built with resilience in mind, featuring built-in retry mechanisms, an interactive ChatOps wizard, and a fully containerized attack architecture.

## Key Features & v1.0.1 Updates

- **Interactive ChatOps Wizard (v1.0.1)**: Operates as a 24/7 daemon using `aiogram` with a Telegram Inline Keyboard UI for weapon selection and scan management.
- **Ephemeral Docker Workers (v1.0.1)**: Attack engines (like Nuclei) are executed inside disposable Docker containers (`--rm`) to prevent dependency conflicts and ensure a clean execution environment.
- **Session Lock & Anti-Exhaustion (v1.0.1)**: Built-in locking mechanism to prevent server resource exhaustion from concurrent scan requests, complete with user cancellation options.
- **Automated Subdomain & Live Asset Probing**: Fetches transparent certificate logs via `crt.sh` and OTX, immediately filtering for live HTTP assets before launching a strike.
- **Resilient Engine**: Built-in timeout handling and automatic retries to bypass API gateway errors (HTTP 502/503/504).
---

## Quick Start

You can run Reconnator in different ways depending on your environment.

### Option 1: Running Locally (Daemon Mode)

Ensure you have Python 3.10+ installed and Docker Engine running in the background for the attack modules.

```bash
# Clone the repository
git clone [https://github.com/yourusername/reconnator.git](https://github.com/yourusername/reconnator.git)
cd reconnator

# Setup Virtual Environment
python3 -m venv venv
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

# Setup Environment Variables
export TELEGRAM_BOT_TOKEN="your_bot_token"

# Run the Bot 24/7
python src/bot.py

```

*Once running, open your Telegram bot and type `/scan <target.com>` to trigger the interactive menu.*

### Option 2: Kubernetes & Helm (Continuous Recon - Legacy Mode)

Deploy Reconnator as a scheduled CronJob in your Kubernetes cluster (e.g., K3s, Minikube, or EKS/GKE).

```bash
# Navigate to the Helm directory
cd deploy/helm

# Install the chart (Runs daily by default)
helm install recon-bot . --set targetDomain="example.com" \
  --set telegram.botToken="your_bot_token"

```

---

## 📂 Project Structure

```text
.
├── .github/workflows/    # CI/CD pipelines
├── deploy/helm/          # Kubernetes Helm Chart
├── src/                  # Core Python modules
│   ├── modules/          # Fetchers, HTTP Prober, and Attack Engines
│   ├── utils/            # Loggers
│   ├── main.py           # Legacy CLI Entrypoint
│   └── bot.py            # ChatOps Daemon Entrypoint (v1.0.1)
├── Dockerfile            # Alpine-based container blueprint
└── requirements.txt      # Python dependencies

```

## Roadmap

* NMap integration for non-HTTP port mapping.
* Ffuf integration for deep directory fuzzing.
* **Layer 3 AI Analysis:** AI-powered alert filtering to reduce false positives.
* Automated report generation (PDF, JSON, HTML).

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

*Built with code and coffee by amiencoy*