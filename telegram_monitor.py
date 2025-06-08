from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession
import os
import requests

# Replace with your actual environment variables or hardcode for testing
api_id = 20295619
api_hash = "1f7150b62cc6f2cf1c38f0855719272c"
string_session = os.getenv("STRING_SESSION")
channel_username = "@PocketSignalsM1"
webhook_url = os.getenv("WEBHOOK_URL", "https://marisbriedis.app.n8n.cloud/webhook/accada36-9029-4db0-88d6-23b02bec865d")

client = TelegramClient(StringSession(string_session), api_id, api_hash)
sequence = []

async def main():
    print("📡 Listening for messages on M1...")

    @client.on(events.NewMessage(chats=channel_username))
    async def handler(event):
        global sequence

        message_text = event.message.message.strip()
        print(f"📨 New message: {message_text}")

        if message_text == "WIN ✅":
            sequence.append("win")
            print("✅ Detected: WIN")
        else:
            sequence.append("call")
            print("📈 Detected: SIGNAL CALL")

        # Keep only the last 18 messages
        if len(sequence) > 18:
            sequence.pop(0)

        # Check for 9 consecutive SIGNAL → WIN pairs
        if sequence == [
            "call", "win",
            "call", "win",
            "call", "win",
            "call", "win",
            "call", "win",
            "call", "win",
            "call", "win",
            "call", "win",
            "call", "win"
        ]:
            print("🔥 Detected 9 consecutive SIGNAL → WIN pairs. Sending webhook...")
            try:
                requests.post(webhook_url, json={"message": "9 consecutive trading wins detected on M1!"})
                print("✅ Webhook sent.")
            except Exception as e:
                print("❌ Webhook failed:", str(e))
            sequence = []  # Reset after trigger

    await client.start()
    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
