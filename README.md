# eTIMS SPIM Course Scanner

A Python-based monitoring tool that continuously polls the Malaysian eTIMS training portal and sends an instant Telegram alert when the SPIM course becomes available for registration.

## Project Portfolio Summary

This repository currently contains the following runtime artifacts:

- `course_checker.py` — core polling engine and notification dispatcher
- `test_bot.py` — Telegram integration verification script
- `.env` — local secrets file for `BOT_TOKEN` and `CHAT_ID`
- `.venv/` — local Python virtual environment (Python 3.14.5)
- `coursebot.ini` — Windows shell metadata, not required for execution

### Purpose

The scanner is designed for lightweight, decoupled monitoring of a single target page and a single target notification channel. It is intentionally small so it can be migrated to a cloud-hosted instance, container, or VM with minimal refactoring.

## Architectural Data Flow

```text
User workstation / cloud instance
   ├─ load .env secrets into environment via python-dotenv
   ├─ execute course_checker.py
   │   ├─ request eTIMS URL with requests
   │   ├─ parse HTML with BeautifulSoup
   │   ├─ search for TARGET_COURSE text
   │   ├─ if found, send POST to Telegram Bot API
   │   └─ log status and repeat after CHECK_INTERVAL
   └─ optional: run test_bot.py to validate Telegram connectivity
```

### Component Breakdown

- `course_checker.py`
  - loads runtime secrets with `load_dotenv()`
  - performs a GET request against `URL`
  - parses page HTML using `BeautifulSoup`
  - performs a case-insensitive text search for `TARGET_COURSE`
  - sends Telegram alerts via the Bot API when the target text appears
  - currently executes in an indefinite polling loop until manually stopped

- `test_bot.py`
  - validates Telegram credentials using the same `.env` values
  - sends a single text message to confirm API access and delivery

- `.env`
  - local credential store, not checked into source control
  - must contain `BOT_TOKEN` and `CHAT_ID`

- `.venv/`
  - local Python environment for isolated dependency management
  - currently built against Python 3.14.5 according to `.venv/pyvenv.cfg`

## `.env` Structure

The project expects a local `.env` file in the repository root with the following keys:

```env
BOT_TOKEN=8830905143:YOUR_NEW_REGENERATED_TOKEN
CHAT_ID=6582891029
```

> Do not commit `.env` to source control. In production, replace this with cloud-managed secrets or environment variables.

## Local Dependencies

The running scripts depend on the following Python packages:

- `requests`
- `beautifulsoup4`
- `python-dotenv`

Because no `requirements.txt` is present in this repository, install packages manually or generate one from your environment.

### Recommended installation

```bash
python -m pip install requests beautifulsoup4 python-dotenv
```

## Environment Troubleshooting and Resolution Logs

### 1. Missing pip inside local virtualenv

Observed failure:

```powershell
C:\Users\Joe Y\Documents\.venv\Scripts\python.exe: No module named pip
```

Cause:
- `.venv` exists and points to Python 3.14.5, but `pip` was not installed inside that virtual environment.

Resolution:

```powershell
cd C:\Users\Joe Y\Documents
\.venv\Scripts\python.exe -m ensurepip --upgrade
\.venv\Scripts\python.exe -m pip install --upgrade pip
\.venv\Scripts\python.exe -m pip install requests beautifulsoup4 python-dotenv
```

If the environment is still broken:

```powershell
Remove-Item -Recurse -Force .venv
python -m venv .venv
\.venv\Scripts\python.exe -m pip install --upgrade pip
\.venv\Scripts\python.exe -m pip install requests beautifulsoup4 python-dotenv
```

### 2. `.env` not being found

Observed failure:

```text
ModuleNotFoundError: No module named 'dotenv'
```

or

```text
FileNotFoundError: [Errno 2] No such file or directory: '.env'
```

Resolution:
- Run the script from the repository root:
  - `cd C:\Users\Joe Y\Documents`
- Confirm `.env` exists and contains `BOT_TOKEN` and `CHAT_ID`
- Install `python-dotenv`

### 3. Missing runtime modules

Observed failures:

```text
ModuleNotFoundError: No module named 'requests'
ModuleNotFoundError: No module named 'bs4'
```

Resolution:

```bash
\.venv\Scripts\python.exe -m pip install requests beautifulsoup4 python-dotenv
```

### 4. Telegram delivery failure

Observed failure example:

```text
Failed to send Telegram message: 404 Client Error: Not Found for url: https://api.telegram.org/bot<token>/sendMessage
```

Resolution:
- Regenerate `BOT_TOKEN` in `@BotFather`
- Confirm `CHAT_ID` is correct using `/getUpdates`
- Ensure the bot and chat exist and the bot has permission to send messages

## Deployment-Readiness Guide

This project is structured for fast adaptation to a cloud-hosted executable instance. The recommended deployment pattern is:

1. Provision a compute environment
   - VM: AWS EC2, Azure VM, GCP Compute Engine
   - Container: Docker running on ECS, AKS, GKE, or a simple Linux VM
2. Install Python 3.14
3. Create or restore an isolated environment
   - `python -m venv .venv`
   - `source .venv/bin/activate` on Linux/macOS
   - `\.venv\Scripts\activate` on Windows
4. Install dependencies
   - `pip install requests beautifulsoup4 python-dotenv`
5. Supply secrets securely
   - Use environment variables instead of `.env` for production
   - Or inject secret values from a cloud secret manager
6. Configure runtime parameters
   - `ETIMS_URL`, `TARGET_COURSE`, `BOT_TOKEN`, `CHAT_ID`, and `CHECK_INTERVAL`
7. Run the process under a supervisor
   - Linux: `systemd`, `cron`, `supervisord`
   - Container: restart policy and health check

### Cloud-safe deployment variables

For production, the following parameters should be treated as secrets and not stored in plaintext source control:

- `BOT_TOKEN`
- `CHAT_ID`
- `ETIMS_URL`
- `TARGET_COURSE`
- `CHECK_INTERVAL`

Example environment injection for Linux container / VM:

```bash
export BOT_TOKEN="<your-token>"
export CHAT_ID="<your-chat-id>"
export ETIMS_URL="https://academy.jpj.gov.my/myetims/calendar/index?l=&b=18"
export TARGET_COURSE="Dibuka Untuk Permohonan"
export CHECK_INTERVAL=300
python course_checker.py
```

### Recommended production architecture

- Use a single worker instance
- Keep the bot token in a secret management service
- Route logs to a central log store
- Configure process restart on failure
- Monitor networking to `academy.jpj.gov.my` and `api.telegram.org`

## Runtime Notes

- `course_checker.py` currently polls indefinitely in a `while True` loop.
- When the target course is detected, the script continues running and will re-send alerts every `CHECK_INTERVAL` seconds while the page still contains the target text.
- If instead you want it to stop after the first successful notification, add a `break` after `send_telegram_message(...)` in the loop.
- `test_bot.py` is useful for validating Telegram connectivity before full deployment.

## Recommended Next Steps

- Add a `requirements.txt` or `pyproject.toml` for dependency management.
- Add `.gitignore` to keep `.env` and `.venv/` out of source control.
- Harden the runtime by separating configuration, secrets, and scheduling.
- Consider containerization for repeatable deployment.

## Current Workspace Notes

- The `.env` file is present and contains the required `BOT_TOKEN` and `CHAT_ID` values.
- The local virtual environment exists, but `pip` is not currently available in `.venv`.
- `coursebot.ini` is Windows shell metadata and does not affect script execution.
- `requirements.txt` has been added for reproducible package installation.
- A GitHub Actions workflow was added at `.github/workflows/course_monitor.yml` to run `course_checker.py` every 30 minutes on `ubuntu-latest` and securely inject `BOT_TOKEN` and `CHAT_ID` from GitHub Secrets.
- The workflow file was restored and reformatted to valid YAML with proper indentation and quoting.

---

**Last Updated:** May 29, 2026
