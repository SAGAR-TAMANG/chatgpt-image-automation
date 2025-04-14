from fastapi import FastAPI
from fastapi.responses import JSONResponse
from utils import run_chatgpt
import nodriver as uc
import traceback

app = FastAPI()

@app.get("/generate-image")
async def generate_image():
    try:
        src = await run_chatgpt()  # ✅ async call is fully supported
        return {"image_url": src}
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": "Image generation failed", "details": str(e)}
        )