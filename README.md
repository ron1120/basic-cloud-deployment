# ☁️ Basic Cloud Deployment

An end-to-end cloud deployment infrastructure showcasing CI/CD pipelines, containerization, infrastructure-as-code, and automated deployments.

---

## 📐 Architecture

```
┌──────────────┐       git push        ┌──────────────────┐
│   Developer   │ ────────────────────► │     GitHub        │
│   (Local)     │                       │   main branch     │
└──────────────┘                       └────────┬─────────┘
                                                │
                                       webhook / poll
                                                │
                                       ┌────────▼─────────┐
                                       │     Jenkins       │
                                       │  (Docker Host)    │
                                       │                   │
                                       │  1. Checkout      │
                                       │  2. Build Image   │
                                       │  3. Test Bot      │
                                       │  4. Deploy        │
                                       └────────┬─────────┘
                                                │
                                       docker build & run
                                                │
                                       ┌────────▼─────────┐
                                       │  Discord Bot      │
                                       │  (Container)      │
                                       └────────┬─────────┘
                                                │
                                       ┌────────▼─────────┐
                                       │   AWS EC2         │
                                       │   (Ubuntu 22.04)  │
                                       │   VPC + Subnet    │
                                       │   via Terraform   │
                                       └──────────────────┘
```

---

## 📁 Project Structure

```
basic-cloud-deployment/
├── Jenkins/
│   └── Jenkinsfile              # CI/CD pipeline definition
├── discord-bot/
│   ├── bot.py                   # Discord bot application
│   ├── Dockerfile               # Container image for the bot
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Discord token (gitignored)
├── infastructure/
│   └── terraform/
│       ├── main.tf              # AWS infrastructure (VPC, EC2, SG)
│       └── terraform.tfvars     # Variable values for Terraform
├── docker-jenkins-run           # Jenkins container bootstrap script
├── .gitignore
└── README.md
```

---

## 🔧 Components

### 1. Jenkins CI/CD Pipeline

A declarative pipeline that automates the build-test-deploy lifecycle:

- **Checkout** — Clones the `main` branch from GitHub and verifies the branch
- **Test** — Builds the Docker image, runs the bot container, verifies it stays running via `docker inspect`, then stops and cleans up
- **Deploy** — Placeholder stage for production deployment to AWS EC2

Jenkins runs inside a Docker container with the host Docker socket mounted, allowing it to build and manage containers directly.

### 2. Discord Bot (Python)

A lightweight bot built with `discord.py`:

| Command | Response |
|---------|----------|
| `!hi`   | Greets the user by name |
| `!ping` | Responds with "Pong!" |
| `!git repo` | Shows repository info (stars, forks, open issues) |
| `!git commits` | Shows the 5 most recent commits |
| `!git latest` | Shows the single latest commit with author and link |

GitHub API calls use the repo configured via `GITHUB_REPO` (defaults to `ron1120/basic-cloud-deployment`). Set `GITHUB_TOKEN` in `.env` for higher rate limits (5,000 req/hr vs 60 req/hr unauthenticated).

On startup, the bot sends a deployment notification to a designated Discord channel, confirming it's online.

### 3. Docker

The bot is containerized using a `python:3.11-slim` base image for a minimal footprint. The Dockerfile uses layer caching by copying `requirements.txt` before the application code.

### 4. AWS Infrastructure (Terraform)

Infrastructure-as-code provisioning for AWS:

| Resource | Details |
|----------|---------|
| **VPC** | `10.0.0.0/16` — isolated network |
| **Public Subnet** | `10.0.1.0/24` in `us-east-1a` |
| **Internet Gateway** | Routes public traffic to/from the VPC |
| **Route Table** | `0.0.0.0/0` → Internet Gateway |
| **Security Group** | SSH (port 22) inbound, all outbound |
| **EC2 Instance** | `t2.micro`, Ubuntu 22.04 LTS |

All values are parameterized via `terraform.tfvars` for easy configuration.

---

## 🚀 Getting Started

### Prerequisites

- Docker
- Terraform
- AWS account with IAM credentials (`~/.aws/credentials`)
- Discord bot token ([Developer Portal](https://discord.com/developers/applications))

### 1. Start Jenkins

```bash
# Run the bootstrap script
bash docker-jenkins-run
```

Jenkins will be available at `http://localhost:8080`.

### 2. Run the Discord Bot Locally

```bash
cd discord-bot
echo "DISCORD_TOKEN=your-token-here" > .env
pip install -r requirements.txt
python bot.py
```

### 3. Provision AWS Infrastructure

```bash
cd infastructure/terraform
terraform init
terraform plan
terraform apply -auto-approve
```

After apply, Terraform outputs the EC2 public IP:

```bash
terraform output instance_public_ip
```

### 4. SSH into EC2

```bash
ssh -i ~/path/to/your-key.pem ubuntu@<instance_public_ip>
```

### 5. Tear Down

```bash
terraform destroy -auto-approve
```

---

## 🛡️ Security Notes

- `.env` files are gitignored — tokens are never committed
- Terraform state files (`*.tfstate`) are gitignored — they contain sensitive resource data
- The Discord token is managed through Jenkins credentials (Username+Password type)
- SSH key permissions must be `400` (`chmod 400 your-key.pem`)

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Jenkins** | CI/CD automation |
| **Docker** | Containerization |
| **Terraform** | Infrastructure-as-code |
| **AWS EC2** | Cloud compute |
| **AWS VPC** | Network isolation |
| **Python** | Discord bot |
| **GitHub** | Source control |
