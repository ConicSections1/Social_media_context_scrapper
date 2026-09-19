from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import asyncio
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, ChannelPrivateError
from pydantic import BaseModel
import re

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
CHANNEL_LINKS = os.getenv("CHANNEL_LINKS", "").split(',')

client = TelegramClient("session_name", API_ID, API_HASH)

class PhoneRequest(BaseModel):
    phone: str

class SecurityCodeRequest(BaseModel):
    phone: str
    security_code: str

# Normalizer
def normalize_text(text: str) -> str:
    return (
        text.replace('–', '-')
            .replace('—', '-')
            .replace('->', ':')
            .replace('→', ':')
            .replace('–>', ':')
    )

# Parser
def parse_job_message(text: str) -> dict:
    text = normalize_text(text)
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    job_data = {
        "type": "N/A",
        "company": "N/A",
        "position": "N/A",
        "qualification": "refer to link",
        "batch": "refer to link",
        "experience": "refer to link",
        "location": "N/A",
        "mode": "N/A",
        "stipend": "N/A",
        "apply_link": "N/A"
    }

    # Try to detect company and position from header line
    for line in lines:
        if "hiring" in line.lower():
            match = re.search(r"(.*?)\s+hiring\s+(.*)", line, re.IGNORECASE)
            if match:
                job_data["company"] = match.group(1).strip()
                job_data["position"] = match.group(2).strip()
            continue

        # Try alternative formats
        if line.lower().startswith("company name"):
            job_data["company"] = line.split(":", 1)[-1].strip()
        if line.lower().startswith("position") or "role" in line.lower():
            job_data["position"] = line.split(":", 1)[-1].strip()
        if "intern" in line.lower() and job_data["type"] == "refer to link":
            job_data["type"] = "Intern"
        elif ("full-time" in line.lower()):
            job_data["type"] = "Full-Time"
        elif "part-time" in line.lower():
            job_data["type"] = "Part-Time"
        else :
            job_data["type"] = "Full-Time or refer to link"

        if "qualification" in line.lower() or "qualifications" in line.lower():
            job_data["qualification"] = line.split(":", 1)[-1].strip()
        if "batch" in line.lower():
            job_data["batch"] = line.split(":", 1)[-1].strip()
        if "experience" in line.lower():
            job_data["experience"] = line.split(":", 1)[-1].strip()
        if "location" in line.lower():
            job_data["location"] = line.split(":", 1)[-1].strip()
        if "salary" in line.lower() or "stipend" in line.lower() or "package" in line.lower() or "ctc" in line.lower():
            job_data["stipend"] = line.split(":", 1)[-1].strip()

        if "remote" in line.lower():
            job_data["mode"] = "Remote"
        elif "hybrid" in line.lower():
            job_data["mode"] = "Hybrid"
        elif "onsite" in line.lower():
            job_data["mode"] = "Onsite"
        else :
            job_data["mode"] = "refer to link"
        # Catch apply link
        if "apply" in line.lower() and "http" in line:
            urls = re.findall(r"https?://\S+", line)
            if urls:
                job_data["apply_link"] = urls[0].strip()

    print("\n📩 Raw Message:\n", text)
    print("📄 Parsed Output:\n", job_data)
    return job_data


@app.post("/scrape")
async def scrape_messages(request: SecurityCodeRequest):
    phone = request.phone
    security_code = request.security_code

    try:
        await client.connect()

        if not await client.is_user_authorized():
            await client.sign_in(phone, security_code)

        result = []
        for link in CHANNEL_LINKS:
            link = link.strip()
            print(f"\n📥 Fetching messages from: {link}")

            try:
                entity = await client.get_entity(link)
                messages = []
                async for msg in client.iter_messages(entity, limit=50):
                    if msg.message:
                        parsed = parse_job_message(msg.message)
                        messages.append(parsed)

                result.append({"channel": link, "messages": messages})

            except ChannelPrivateError:
                result.append({"channel": link, "error": "Private channel or not joined."})
            except Exception as e:
                result.append({"channel": link, "error": f"Error: {str(e)}"})

    except SessionPasswordNeededError:
        raise HTTPException(status_code=400, detail="Password required for the account.")
    finally:
        await client.disconnect()

    return {"status": "success", "result": result}

@app.post("/scrape_without_code")
async def scrape_without_code(request: PhoneRequest):
    phone = request.phone

    try:
        await client.connect()

        if not await client.is_user_authorized():
            raise HTTPException(status_code=401, detail="User not authorized. Please provide the security code.")

        result = []
        for link in CHANNEL_LINKS:
            link = link.strip()
            print(f"\n📥 Fetching messages from: {link}")

            try:
                entity = await client.get_entity(link)
                messages = []
                async for msg in client.iter_messages(entity, limit=50):
                    if msg.message:
                        parsed = parse_job_message(msg.message)
                        messages.append(parsed)

                result.append({"channel": link, "messages": messages})

            except ChannelPrivateError:
                result.append({"channel": link, "error": "Private channel or not joined."})
            except Exception as e:
                result.append({"channel": link, "error": f"Error: {str(e)}"})

        print("Backend Scraped Data:", result)  # Log scraped data

    except SessionPasswordNeededError:
        raise HTTPException(status_code=400, detail="Password required for the account.")
    finally:
        await client.disconnect()

    return {"status": "success", "result": result}
