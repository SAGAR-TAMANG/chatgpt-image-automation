# utils.py

from fastapi import HTTPException, status
from jose import JWTError, jwt
from dotenv import load_dotenv
import asyncio, os

load_dotenv()

# --- Config ---
# Chrome Binary Location (Note: Mac users will have different location)
browser_1 = "C:/Program Files/Google/Chrome/Application/chrome.exe"

# User Profile of Chrome (Note: Mac users will have different location)
profile_dir = "C:/Users/TAMANG/AppData/Local/Google/Chrome/User Data"

# Your Profile Number may be different -> It can be 1 or 2 or anything. See physically in Explorer/Finder
profile_name = "Profile 27"

url = "https://chat.openai.com/"
# message = "Generate a simple image quickly with text 'SIMPLE'."

# --- JWT verification ---
def verify_jwt_token(token: str = ""):
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Can return user info or claims if needed
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

async def run_chatgpt(message: str):
    import nodriver as uc
    
    browser = await uc.start(
        headless=False,
        browser_executable_path=browser_1,
        user_data_dir=profile_dir,
        browser_args=[f"--profile-directory={profile_name}"]
    )

    try:
        print("🌐 Launching tab...")
        tab = await browser.get(url)
        await tab

        print("⌨️ Sending prompt...")
        ask_anything = await tab.select("p")
        await ask_anything.send_keys(message)

        print("🚀 Submitting...")
        send_button = await tab.find("composer-submit-button", best_match=True)
        await send_button.click()

        print("⏳ Waiting for image generation...")
        count = 0
        previous_len = 0
        src = None

        while True:
            images = await tab.query_selector_all('img[alt="Generated image"]')
            if len(images) > 0:
                if previous_len > 0:
                    if previous_len == len(images):
                        count += 1
                    else:
                        previous_len = len(images)
                        count = 0
                else:
                    previous_len = len(images)
                    count = 0

            print(f"🔍 Found {len(images)} images | Stability Count: {count + 1}")

            if count >= 6:
                latest_image = images[-1]
                attrs = latest_image.attrs
                src = attrs["src"]
                print(f"✅ Image URL: {src}")
                break

            await asyncio.sleep(10)

        return src

    finally:
        print("🧹 Cleaning up browser...")
        browser.stop()