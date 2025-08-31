# 🚀 Telegram Setup Guide

## Quick Start Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Add these to your `.env` file:
```env
# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
TELEGRAM_CHAT_ID=your_chat_id_number
TELEGRAM_WEBHOOK_SECRET=your_random_secret_string

# Keep your existing OpenAI key
OPENAI_API_KEY=your-openai-api-key
```

### 3. Test the Bot Locally
```bash
# Test in chat mode (no webhook needed)
python main.py -test

# Test research pipeline
python main.py -test -research AAPL
```

### 4. Set Up Webhook for Production
```bash
# First deploy your app, then run:
python setup_telegram_webhook.py

# Or set manually:
# Choose option 1 and enter your public URL
```

## 📱 How to Use

### Bot Commands (same as before):
- `Start tracking AAPL` - Add a stock to tracker
- `Stop tracking MSFT` - Remove a stock from tracker  
- `What stocks am I tracking?` - List all tracked stocks
- `What is the price of AAPL?` - Get current stock price

### Alerts:
- Automatic alerts when stocks move >1% from previous close
- AI-powered news research and summaries
- Sent directly to your Telegram chat

## 🔧 Troubleshooting

### Common Issues:

**"Import could not be resolved" warnings:**
- These are normal - run `pip install -r requirements.txt`

**Bot not responding:**
1. Check your `TELEGRAM_BOT_TOKEN` is correct
2. Verify `TELEGRAM_CHAT_ID` matches your chat
3. Ensure webhook is set correctly (use setup script)

**Webhook errors:**
1. Make sure your server is publicly accessible
2. Use HTTPS (required by Telegram)
3. Check webhook URL includes `/telegram-webhook` endpoint

**Permission errors:**
1. Make sure you've started a conversation with your bot
2. Send `/start` to your bot first
3. Verify the chat ID is correct

### Testing Commands:
```bash
# Test bot connectivity
python setup_telegram_webhook.py
# Choose option 3 (Test bot)

# View webhook status
curl -X GET "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

## 🔒 Security Notes

- Keep your bot token secret
- Use the webhook secret for additional security
- Only your specific chat ID can control the bot
- All other messages are rejected

## 🎯 What Changed from Twilio

| Feature | Twilio SMS | Telegram |
|---------|------------|----------|
| **Cost** | Pay per SMS | Completely free |
| **Setup** | Phone number needed | Just create a bot |
| **Message Length** | 160 characters | 4096 characters |
| **Rich Content** | Text only | Text, formatting, buttons |
| **Global** | Region restrictions | Works worldwide |
| **Webhook** | Signature validation | Secret token validation |

## ✅ Verification Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Environment variables set in `.env`
- [ ] Bot created via @BotFather  
- [ ] Chat ID obtained and verified
- [ ] Local testing works (`python main.py -test`)
- [ ] Webhook set for production
- [ ] Can send/receive messages via Telegram
- [ ] Stock tracking alerts working
- [ ] All commands respond correctly

Your Stock Tracker Agent is now powered by Telegram! 🎉
