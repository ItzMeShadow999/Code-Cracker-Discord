<div align="center">

<img src="https://i.ibb.co/6cd8NfjC/image.png" width="220" />

# Code Cracker Discord (CCD)

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![discord.py-self](https://img.shields.io/badge/discord.py--self-latest-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://pypi.org/project/discord.py-self/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)
[![ToS Warning](https://img.shields.io/badge/Discord%20ToS-Violation-red?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/terms)

A Discord selfbot that automatically brute-forces slash command codes by cycling through random 4-digit codes every 34 seconds until the correct one is found. Logs every attempt to `log.json` and skips codes it has already tried.

</div>

---



## Features

- Automatically invokes `/code code:XXXX` as a real slash command (not a text message)
- 34 second cooldown between attempts to respect server limits
- Skips codes already tried  won't repeat itself across restarts
- Logs every attempt to `log.json` with timestamps and a total count
- Stops automatically when the bot confirms the correct code
- Filters the correct slash command by bot ID to avoid false matches
- Handles Discord timeouts gracefully without crashing

---

## Requirements

- Python 3.11+
- `discord.py-self`

### If you have discord.py already installed, uninstall it first

`discord.py` and `discord.py-self` conflict with each other. Run this before installing:

```bash
pip uninstall discord.py discord
```

Then install `discord.py-self`:

```bash
pip install discord.py-self
```

To verify the right one is installed:

```bash
pip show discord.py-self
```

---

## Setup

1. **Clone or download** the script.

2. **Fill in your config** at the top of `Code Cracker Discord.py`  see the Editing the Config section below.

3. **Run it:**

```bash
python 'Code Cracker Discord.py'
```

---

## Editing the Config

Open `Code Cracker Discord.py` and find this section at the top:

```python
USER_TOKEN = "your-user-token-here"

TARGET_CHANNEL_ID = 0  # channel ID where /code is used
SERVER_ID = 0          # server ID
BOT_ID = 0             # bot ID that owns the /code command

COOLDOWN_SECONDS = 34
```

### USER_TOKEN

Your Discord account token. See "How to Get Your User Token" below.

```python
USER_TOKEN = "NzQ4OTI0NTY4NzQ4OTI0NTY."  # paste your token here
```

### TARGET_CHANNEL_ID

The ID of the channel where the `/code` command is used. To get it: enable Developer Mode in Discord settings, right-click the channel, click Copy ID.

```python
TARGET_CHANNEL_ID = 1234567890123456789
```

### SERVER_ID

The ID of the server. Right-click the server icon and click Copy ID.

```python
SERVER_ID = 1234567890123456789
```

### BOT_ID

The ID of the bot that owns the `/code` command. Right-click the bot in the server and click Copy ID.

```python
BOT_ID = 1234567890123456789
```

### COOLDOWN_SECONDS

How long to wait between each attempt. The server's cooldown is 30 seconds so do not set this lower or commands will be blocked.

```python
COOLDOWN_SECONDS = 34
```

---

## log.json

Every run appends to `log.json` in the same folder. It tracks:

- `session_start`  when the script started
- `total_tried`  total codes attempted across all runs
- `correct_code`  filled in when the code is found
- `found_at`  timestamp of when it was found
- `codes_tried`  full list of every code sent with its timestamp

Codes in `log.json` are automatically skipped on future runs so you never send the same code twice.

---

## How to Get Your User Token

1. Open Discord in your browser
2. Press `F12` and go to the Network tab
3. Filter for `api/v9`
4. Click any request and look for `Authorization` in the request headers
5. Copy the value  that is your token

---

## How It Works

```
Bot starts
  └── Every 34 seconds:
        ├── Fetches all slash commands in the channel
        ├── Finds /code from the target bot by application ID
        ├── Generates a random 4-digit code not yet in log.json
        ├── Invokes /code code:XXXX as a real slash command
        ├── Appends the attempt to log.json
        └── If bot responds with "correct" or checkmark -> stops
```

---

## Changing the Slash Command

By default CCD uses `/code` with an option called `code`. If the server uses a different slash command you can change it in `Code Cracker Discord.py`.

### Changing the command name

Find this line:

```python
(c for c in all_commands if c.name == "code" and c.application_id == BOT_ID),
```

Change `"code"` to whatever the command is called. For example if the command is `/crack`:

```python
(c for c in all_commands if c.name == "crack" and c.application_id == BOT_ID),
```

### Changing the option name

Find this line:

```python
await cmd(code=str(code))
```

Change `code=` to match the option name the command uses. For example if the option is called `input`:

```python
await cmd(input=str(code))
```

To find the correct option name, type the slash command in Discord and look at what the input field is labelled.

---

## Disclaimer

Using a selfbot (user token automation) violates [Discord's Terms of Service](https://discord.com/terms). Use at your own risk. This project is for **educational purposes only**.

---
