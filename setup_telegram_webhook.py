#!/usr/bin/env python3
"""
Script to set up Telegram webhook for the Stock Tracker Agent
Run this after deploying your application to set the webhook URL
"""

import os
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET", "your_secret_token")

async def setup_webhook(webhook_url: str):
    """Set up the Telegram webhook"""
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        # Set webhook
        await bot.set_webhook(
            url=f"{webhook_url}/telegram-webhook",
            secret_token=TELEGRAM_WEBHOOK_SECRET
        )
        
        print(f"✅ Webhook set successfully to: {webhook_url}/telegram-webhook")
        
        # Get webhook info to verify
        webhook_info = await bot.get_webhook_info()
        print(f"📡 Current webhook: {webhook_info.url}")
        print(f"🔒 Has secret token: {'Yes' if webhook_info.has_secret_token else 'No'}")
        print(f"📋 Pending updates: {webhook_info.pending_update_count}")
        
    except TelegramError as e:
        print(f"❌ Error setting webhook: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

async def remove_webhook():
    """Remove the current webhook"""
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.delete_webhook()
        print("✅ Webhook removed successfully")
    except Exception as e:
        print(f"❌ Error removing webhook: {e}")

async def test_bot():
    """Test basic bot functionality"""
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        bot_info = await bot.get_me()
        print(f"🤖 Bot info: @{bot_info.username} ({bot_info.first_name})")
        print(f"📊 Bot ID: {bot_info.id}")
        
        # Test message sending if chat ID is available
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if chat_id:
            await bot.send_message(
                chat_id=chat_id,
                text="🚀 Stock Tracker Agent - Telegram integration test successful!"
            )
            print(f"✅ Test message sent to chat ID: {chat_id}")
        else:
            print("⚠️  TELEGRAM_CHAT_ID not set - skipping message test")
            
    except Exception as e:
        print(f"❌ Error testing bot: {e}")

if __name__ == "__main__":
    if not TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not found in environment variables")
        exit(1)
    
    print("🔧 Telegram Bot Setup Tool")
    print("=" * 40)
    
    action = input("Choose action:\n1. Set webhook\n2. Remove webhook\n3. Test bot\n4. Exit\nEnter choice (1-4): ")
    
    if action == "1":
        webhook_url = input("Enter your webhook URL (e.g., https://yourdomain.com): ").strip()
        if webhook_url:
            asyncio.run(setup_webhook(webhook_url))
        else:
            print("❌ No URL provided")
    
    elif action == "2":
        asyncio.run(remove_webhook())
    
    elif action == "3":
        asyncio.run(test_bot())
    
    elif action == "4":
        print("👋 Goodbye!")
    
    else:
        print("❌ Invalid choice")
