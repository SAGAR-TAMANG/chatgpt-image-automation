"""Full Selenium Integration"""

import nodriver as uc
import asyncio
from bs4 import BeautifulSoup

browser_1 = "C:/Program Files/Google/Chrome/Application/chrome.exe"

url_list = [
    "https://chat.openai.com/",
]

async def main():
    browser = await uc.start(
        headless=False,
        browser_executable_path=browser_1,
        user_data_dir="C:/Users/TAMANG/AppData/Local/Google/Chrome/User Data",
        browser_args=["--profile-directory=Profile 27"]
    )

    print(browser.info)
    
    tab = await browser.get(url_list[0])
    await tab

    print("⌨️ Typing prompt...")
    ask_anything = await tab.select("p")
    await ask_anything.send_keys("Generate a simple image quickly with text 'SIMPLE'.")

    print("🚀 Sending prompt...")
    send_button = await tab.find("composer-submit-button", best_match=True)
    await send_button.click()

    print("🔎 Waiting for image...")
    image_src = None
    count = 0
    previous_len = 0

    while True:
        try:
            html = await tab.get_content()
            soup = BeautifulSoup(html, "html.parser")
            images = soup.find_all("img", alt="Generated image")

            if images:
                print(f"Found {len(images)} images - Image count {count + 1} - Previous len {previous_len}")
            else:
                print(f"Not Found Images - Image count {count + 1} - Previous len {previous_len}")

            # Find one with opacity: 1 or just pick last
            chosen_img = None
            for img in images:
                style = img.get("style", "")
                if "opacity: 1" in style:
                    chosen_img = img
                    break

            if not chosen_img and len(images) > 0:
                chosen_img = images[-1]

            if chosen_img:
                image_src = chosen_img.get("src")
                if image_src:
                    print("✅ Image found via BeautifulSoup!")
                    print(f"🖼️ Image URL: {image_src}")
                    break

            # Retry logic
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

            if count == 3 and len(images) > 0:
                fallback_img = images[-1]
                image_src = fallback_img.get("src")
                print("✅ Fallback triggered. Using last image.")
                print(f"🖼️ Image URL: {image_src}")
                break

        except Exception as e:
            print(f"⚠️ Still waiting... {e}")


        await asyncio.sleep(10)

    browser.stop()

if __name__ == "__main__":
    uc.loop().run_until_complete(main())