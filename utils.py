"""utils.py — Half-Selenium Integration (Improved)"""

# from bs4 import BeautifulSoup
import nodriver as uc
import asyncio

# --- Config ---
browser_1 = "C:/Program Files/Google/Chrome/Application/chrome.exe"
profile_dir = "C:/Users/TAMANG/AppData/Local/Google/Chrome/User Data"
profile_name = "Profile 27"
url = "https://chat.openai.com/"
message = "Generate a simple image quickly with text 'SIMPLE'."


async def run_chatgpt():
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

            if count >= 3:
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

if __name__ == "__main__":
    # Do nothing here for production usage with FastAPI
    import nodriver as uc
    uc.loop().run_until_complete(run_chatgpt())