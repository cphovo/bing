from enum import Enum
from fastapi import Depends, FastAPI, HTTPException, Header, status
from pydantic import BaseModel
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle


REQUIRED_TOKEN = "cphovo-e1fecb424bb92b04223f5bc7ebe938d948446e9c"


async def verify_token(Authorization: str = Header()):
    if Authorization != REQUIRED_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

app = FastAPI(dependencies=[Depends(verify_token)])


class Style(str, Enum):
    creative = "creative"
    balanced = "balanced"
    precise = "precise"


class AskRequest(BaseModel):
    text: str
    style: Style = Style.creative


@app.post('/bing/ask')
async def ask(req: AskRequest):
    bot = await Chatbot.create()
    style = getattr(
        ConversationStyle,
        req.style.value,
        ConversationStyle.creative
    )
    response = await bot.ask(prompt=req.text, conversation_style=style, simplify_response=True)
    await bot.close()
    return response
