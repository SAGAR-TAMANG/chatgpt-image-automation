import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

print(f"🚀 Running with Python {sys.version}")

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import traceback
from utils import run_chatgpt, verify_jwt_token

from fastapi.middleware.cors import CORSMiddleware


class GenerateImage(BaseModel):
    auth_token: str
    message: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to specific frontend domain
    allow_credentials=True,
    allow_methods=["*"],  # Or ["POST"] if you want to restrict
    allow_headers=["*"],  # Or ["Content-Type", "Authorization"] etc.
)

@app.post("/generate-image")
async def generate_image(request: GenerateImage):
    verify_jwt_token(request.auth_token)
    try:
        src = await asyncio.wait_for(run_chatgpt(message=request.message), timeout=300)
        return {"image_url": src}
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": "Image generation failed", "details": str(e)}
        )