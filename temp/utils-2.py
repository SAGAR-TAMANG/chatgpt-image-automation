"""Full Non-Selenium Integration"""

import nodriver as uc
import asyncio

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

    print("finding the input field...")
    ask_anything = await tab.select("p")
    await ask_anything.send_keys("Generate a simple image quickly with text 'SIMPLE'.")

    print("clicking the send button...")
    send_button = await tab.find("composer-submit-button", best_match=True)
    await send_button.click()

    print("waiting for image...")
    image_src = None
    count = 0
    previous_len = 0

    while True:
        try:
            # images = await tab.select_all('img[alt="Generated image"]')
            images = await tab.query_selector_all('img[alt="Generated image"]')
            print(f"Found {len(images)} images - Image count {count + 1} - Previous len {previous_len}")

            # print(images)
            
            for img in images:
                style = await img.get_attribute("style")
                if style and "opacity: 1" in style:
                    image_src = await img.get_attribute("src")
                    break
        except Exception as e:
            print(f"⚠️ Still waiting... {e}")

        if image_src:
            print("✅ Image found!")
            print(f"🖼️ Image URL: {image_src}")
            break
        
        if (len(images) > 0):
            if previous_len > 0:
                if previous_len == len(images):
                    count += 1
                else:
                    previous_len = len(images)
                    count = 0
            else:
                previous_len = len(images)
                count = 0
        
        if count == 3:
            image = images[-1]
            print(f"Our image is: {image}")
            print("✅ Image found!")
            image_src = await image.attrs('src')
            print(f"🖼️ Image URL: {image_src}")
            break
        
        await asyncio.sleep(10)

    browser.stop()

if __name__ == "__main__":
    uc.loop().run_until_complete(main())