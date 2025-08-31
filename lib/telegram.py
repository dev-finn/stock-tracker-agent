import os
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_telegram_message(message: str) -> None:
    """Send message via Telegram bot (async version)"""
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
            parse_mode='HTML'
        )
        print(f"Telegram message sent: {message}")
    except TelegramError as e:
        print(f"Failed to send Telegram message: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error sending Telegram message: {e}")
        raise

def send_telegram_message_sync(message: str) -> None:
    """Synchronous wrapper for send_telegram_message - compatible with existing SMS interface"""
    try:
        # Use a thread pool to avoid event loop conflicts
        import concurrent.futures
        import threading
        
        def run_in_thread():
            # Create a new event loop in the thread
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                new_loop.run_until_complete(send_telegram_message(message))
            finally:
                new_loop.close()
        
        # Run in a separate thread to avoid event loop conflicts
        thread = threading.Thread(target=run_in_thread)
        thread.start()
        thread.join()
        
    except Exception as e:
        print(f"Error in sync Telegram message: {e}")

# Alias for backward compatibility with existing SMS calls
send_sms = send_telegram_message_sync
