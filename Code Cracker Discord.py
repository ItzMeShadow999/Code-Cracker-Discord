import discord
from discord.ext import tasks
import random

USER_TOKEN = "YOUR-USER-TOKEN-HERE"

TARGET_CHANNEL_ID = 0  # channel ID where /code is used
BOT_ID = 0             # bot ID that owns the /code command

COOLDOWN_SECONDS = 30
CORRECT_CODE = "0000"  # the code you are looking for

client = discord.Client()


def generate_code():
    return str(random.randint(1000, 9999))



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

    code = generate_code()
    print(f"[SENDER] Trying code: {code}")
    await cmd(code=str(code))

    if code == CORRECT_CODE:
        print(f"[SENDER] Found the correct code: {code} — stopping.")
        use_slash_code.stop()


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
        use_slash_code.stop()



@client.event
async def on_ready():
    print('=========================================')
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('=========================================')

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
