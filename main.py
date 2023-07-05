import json
import os
import binascii
from enum import Enum
from fastapi import Depends, FastAPI, HTTPException, Header, status
from pydantic import BaseModel
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
from starlette.requests import Request


def generate_api_token():
    return 'cphovo-' + binascii.hexlify(os.urandom(20)).decode()


REQUIRED_TOKEN = generate_api_token()
print("====" * 16)
print(f"\n\t{REQUIRED_TOKEN}\n")
print("====" * 16)


async def verify_token(Authorization: str = Header()):
    if Authorization != REQUIRED_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

app = FastAPI(dependencies=[Depends(verify_token)],
              docs_url=None, redoc_url=None, openapi_url=None)


class Style(str, Enum):
    creative = "creative"
    balanced = "balanced"
    precise = "precise"


class AskRequest(BaseModel):
    text: str
    style: Style = Style.creative


@app.post('/bing/ask')
async def ask(req: AskRequest):
    style = getattr(
        ConversationStyle,
        req.style.value,
        ConversationStyle.creative
    )
    try:
        bot = await Chatbot.create()
        response = await bot.ask(prompt=req.text, conversation_style=style, simplify_response=True)
        await bot.close()
    except Exception as e:
        # retry with cookies
        if os.path.exists("cookies.json"):
            print("Using cookies and retring...")
            cookies = json.loads(open("cookies.json", encoding="utf-8").read())
            bot = await Chatbot.create(cookies=cookies)
            response = await bot.ask(prompt=req.text, conversation_style=style, simplify_response=True)
            await bot.close()
        else:
            raise e
    return response


@app.route("/{path:path}")
async def catch_all(request: Request):
    raise HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY, detail="Bad Gateway")
