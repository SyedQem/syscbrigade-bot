# Free AI Discord Bot

A Discord bot powered by Google Gemini Flash — completely free, no credit card required.

---

## Features
- Responds when @mentioned in any channel
- Responds in DMs
- Remembers conversation context per channel (last 10 exchanges)
- `/ask` slash command for quick one-off questions
- `/clear` slash command to reset memory for a channel

---

## Setup (15 minutes)

### Step 1 — Get your Discord Bot Token
1. Go to https://discord.com/developers/applications
2. Click **New Application** → give it a name
3. Go to **Bot** tab → click **Add Bot**
4. Under **Token**, click **Reset Token** and copy it
5. Scroll down and enable:
   - ✅ Message Content Intent
   - ✅ Server Members Intent
6. Go to **OAuth2 → URL Generator**
   - Scopes: `bot`, `applications.commands`
   - Bot Permissions: `Send Messages`, `Read Messages/View Channels`, `Read Message History`
7. Copy the generated URL and open it to invite the bot to your server

### Step 2 — Get your Free Gemini API Key
1. Go to https://aistudio.google.com/app/apikey
2. Click **Create API Key**
3. Copy it — no credit card needed!

### Step 3 — Configure the bot
```bash
cp .env.example .env
```
Open `.env` and fill in both values:
```
DISCORD_TOKEN=your_token_here
GEMINI_API_KEY=your_key_here
```

### Step 4 — Install and run
```bash
pip install -r requirements.txt
python bot.py
```

You should see:
```
✅ Logged in as YourBotName#1234
✅ Slash commands synced
```

---

## Usage
| How | Example |
|---|---|
| Mention in server | `@Aria what's the meaning of life?` |
| DM the bot | Just type directly |
| Slash command | `/ask question: explain black holes` |
| Clear memory | `/clear` |

---

## Free Tier Limits (Gemini Flash)
- **15 requests per minute**
- **1,500 requests per day**
- **1 million tokens per minute**
- No cost, no credit card, ever (at these limits)

More than enough for a personal Discord server.

---

## ☁️ Optional: Keep it always-on for free
Deploy to **Railway** (https://railway.app):
1. Push this project to a GitHub repo
2. Connect Railway to the repo
3. Add your `.env` values as environment variables in Railway
4. Deploy — it runs 24/7 on their free tier

---

## Customization
- Change the bot's name/personality: edit `BOT_NAME` and `system_instruction` in `bot.py`
- Change which channels it responds in: add a channel allowlist check in `on_message`
- Add more slash commands: duplicate the `/ask` pattern
