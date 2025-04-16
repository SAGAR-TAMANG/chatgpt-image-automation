# 🤖 chatgpt-image-automation

Automate ChatGPT to generate images through browser interaction — programmatically send prompts and extract image URLs, all using Python + FastAPI + Chrome automation.

---

## 📸 What This Project Does

This tool launches a browser instance (using your own Chrome profile), sends an image generation prompt to [chat.openai.com](https://chat.openai.com), waits for the image to render, and returns the image URL via an API endpoint.

You can plug this into creative tools, marketing pipelines, or AI-enhanced image workflows — all with a single API call.

---

## 🚀 Features

- ⚡ One-click API to trigger image generation on ChatGPT  
- 🔐 JWT-authenticated `/generate-image` endpoint  
- 🌐 Chrome browser automation (via [nodriver](https://github.com/shinya7y/nodriver))  
- 📤 Returns the generated image URL directly  
- 🛡️ Uses your local Chrome profile (no repeated logins)  

---

## 🛠️ Quick Setup

### 1. Clone the Repo
```bash
git clone https://github.com/SAGAR-TAMANG/chatgpt-image-automation.git
cd chatgpt-image-automation
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY="uQ3r8Kz!qkY8M7zX@bT9PfVvL2aR#cX1"
ALGORITHM="HS256"
```

---

## ⚙️ Configure Chrome (Windows Example)

In `utils.py`, update these:

```python
browser_1 = "C:/Program Files/Google/Chrome/Application/chrome.exe"
profile_dir = "C:/Users/YOUR_USERNAME/AppData/Local/Google/Chrome/User Data"
profile_name = "Profile 1"  # Use your logged-in Chrome profile
```

💡 *Don’t want to reuse sessions? Leave profile_dir/profile_name blank to launch a temporary browser.*

---

## ▶️ Run the Server

```bash
uvicorn app:app --reload
```

---

## 🔐 Sample JWT Auth & API Call

Here’s a simple example using `curl`:

```bash
curl --location 'http://localhost:8000/generate-image' \
--header 'Content-Type: application/json' \
--data '{
  "auth_token": "your_jwt_token_here",
  "message": "generate an image of a futuristic city at sunset"
}'
```

Returns:

```json
{
  "image_url": "https://files.chat.openai.com/..."
}
```

---

## 🧠 How It Works

1. FastAPI endpoint accepts a `message` + JWT `auth_token`  
2. Chrome launches using `nodriver` with your profile  
3. Prompt is typed into ChatGPT and submitted  
4. Bot waits until a generated image stabilizes in the DOM  
5. Returns the `src` URL of the image  

---

## 📦 Dependencies

- `FastAPI`  
- `python-dotenv`  
- `python-jose` (JWT handling)  
- `nodriver` (async Chrome automation)  
- `asyncio`, `uvicorn`  

---

## 📈 Use Cases

- Creative automation tools  
- Content generation workflows  
- Internal bots for visual assets  
- Custom creative UI powered by ChatGPT  

---

## 🚧 Roadmap

- [ ] Headless support  
- [ ] Retry if image fails to load  
- [ ] Support for downloading + saving image  
- [ ] Web UI for prompt testing  

---

## 🔒 Auth Note

JWT tokens must be signed with the same `SECRET_KEY` and use the algorithm specified in `.env`. Example payload:

```json
{
  "sub": "your_user_id"
}
```

---

## 📄 License

MIT

---

## 🌍 Keywords for Search (GitHub Topics)

```
chatgpt • image-generator • automation • fastapi • chrome-bot • nodriver • jwt-auth • openai • ai-creative • image-url • prompt-engineering • web-scraper • gpt4free • ghibli image • ghibli generator in ChatGPT
```