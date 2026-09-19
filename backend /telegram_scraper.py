import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, ChannelPrivateError
from telethon.tl.functions.channels import JoinChannelRequest

# Load env vars
load_dotenv()

print("API_ID:", os.getenv("API_ID"))
print("API_HASH:", os.getenv("API_HASH"))


API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
CHANNEL_LINKS = os.getenv("CHANNEL_LINKS", "").split(',')

client = TelegramClient("session_name", API_ID, API_HASH)

async def fetch_messages():
    await client.start()
    print("✅ Connected to Telegram!")

    for link in CHANNEL_LINKS:
        try:
            link = link.strip()
            print(f"\n📥 Fetching messages from: {link}")

            # Get entity (channel object)
            entity = await client.get_entity(link)

            # Fetch last 10 messages
            async for msg in client.iter_messages(entity, limit=10):
                if msg.message:
                    print(f"📝 {msg.date} - {msg.message[:100]}")

        except ChannelPrivateError:
            print(f"🔒 Cannot access {link}: it's private and not joined.")
        except Exception as e:
            print(f"❌ Error with {link}: {e}")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(fetch_messages())
