# pip install discord.py-self

import discord
from discord.ext import tasks
import random
import json
import os
from datetime import datetime, timezone

USER_TOKEN = "your-user-token-here"

TARGET_CHANNEL_ID = 0  # channel ID where /code is used
SERVER_ID = 0          # server ID
BOT_ID = 0             # bot ID that owns the /code command

COOLDOWN_SECONDS = 34

LOG_FILE = "log.json"

client = discord.Client()

def generate_code():
    return str(random.randint(1000, 9999))

def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return {
        "session_start": None,
        "total_tried": 0,
        "correct_code": None,
        "found_at": None,
        "codes_tried": []
    }

def save_log(data: dict):
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def now_iso():
    return datetime.now(timezone.utc).isoformat()

log = load_log()

@tasks.loop(seconds=COOLDOWN_SECONDS)
async def use_slash_code():
    channel = client.get_channel(TARGET_CHANNEL_ID)
    if channel is None:
        print(f"[SENDER] Channel {TARGET_CHANNEL_ID} not found.")
        return

    all_commands = await channel.application_commands()
    cmd = next(
        (c for c in all_commands if c.name == "code" and c.application_id == BOT_ID),
        None
    )

    if cmd is None:
        print("[SENDER] /code command not found.")
        return

    already_tried = {entry["code"] for entry in log["codes_tried"]}
    while True:
        code = generate_code()
        if code not in already_tried:
            break

    print(f"[SENDER] Trying code: {code}  (total tried: {log['total_tried'] + 1})")

    try:
        await cmd(code=str(code))
    except discord.errors.InvalidData:
        print(f"[SENDER] Discord timed out responding to /code — will retry next loop.")
        return
    except Exception as e:
        print(f"[SENDER] Unexpected error sending command: {e}")
        return

    # --- Update log ---
    log["total_tried"] += 1
    log["codes_tried"].append({
        "code": code,
        "timestamp": now_iso()
    })
    save_log(log)


@use_slash_code.before_loop
async def before_loop():
    await client.wait_until_ready()

@client.event
async def on_message(message):
    if message.channel.id != TARGET_CHANNEL_ID:
        return
    if message.author.id != BOT_ID:
        return

    content = message.content.lower()
    if "correct" in content or "✅" in content:
        print(f"[DETECTOR] Bot confirmed correct code! Stopping.")
        log["found_at"] = now_iso()
        save_log(log)
        use_slash_code.stop()

@client.event
async def on_ready():
    print('=========================================')
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('=========================================')

    log["session_start"] = now_iso()
    save_log(log)

    if not use_slash_code.is_running():
        use_slash_code.start()
        print(f"Brute forcing /code every {COOLDOWN_SECONDS}s.")

if __name__ == "__main__":
    print("[INIT] Starting...")
    try:
        client.run(USER_TOKEN)
    except discord.errors.LoginFailure:
        print("\nLoginFailure: token is invalid.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
