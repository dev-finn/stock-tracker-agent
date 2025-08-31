import os
import html
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import Response
from lib.tracker import track_stocks
from lib.agent import handle_incoming_message, run_research_pipeline
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from lib.stock_checker import get_stock_price
from lib.telegram import send_telegram_message, send_telegram_message_sync
import sys
import json
from telegram import Update, Bot
from telegram.error import TelegramError
from dotenv import load_dotenv
load_dotenv()

# FASTAPI Configuration

app = FastAPI()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET", "your_secret_token")

@app.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    """Handle incoming Telegram messages"""
    try:
        # Verify webhook secret token if provided
        telegram_secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if TELEGRAM_WEBHOOK_SECRET and telegram_secret != TELEGRAM_WEBHOOK_SECRET:
            print(f"Invalid webhook secret: {telegram_secret}")
            return Response(content="Unauthorized", status_code=403)
        
        # Parse Telegram update
        update_data = await request.json()
        
        # Create Update object
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        update = Update.de_json(update_data, bot)
        
        # Only process text messages from authorized user
        if update.message and update.message.text:
            chat_id = str(update.message.chat.id)
            
            # Verify it's from authorized chat
            if chat_id != TELEGRAM_CHAT_ID:
                print(f"Unauthorized chat ID: {chat_id}")
                return Response(content="Unauthorized chat", status_code=403)
            
            message_text = update.message.text
            
            # Escape HTML in message
            safe_message = html.escape(message_text)
            
            print(f"Received Telegram message: {safe_message}")
            
            # Process the message
            response_text = await handle_incoming_message(safe_message)
            
            print(f"Response: {response_text}")
            
            # Send response back via Telegram
            await send_telegram_message(response_text)
            
            return Response(content="OK", status_code=200)
        else:
            print("No text message found in update")
            return Response(content="No message", status_code=200)
            
    except TelegramError as e:
        print(f"Telegram error: {e}")
        return Response(content="Telegram error", status_code=500)
    except Exception as e:
        print(f"Error processing Telegram webhook: {e}")
        return Response(content="Error", status_code=500) 

# For testing purposes only

async def chat_terminal():
  print("Chat mode activated. Type 'exit' to quit.")
  while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
      print("Exiting chat.")
      break
    response = await handle_incoming_message(user_input)
    print(f"Bot: {response}")

# Run the project

if __name__ == "__main__":

  # Check to make sure the alert_history.json and tracker_list.json exist, otherwise create them

  if not os.path.exists("resources"):
    os.makedirs("resources")

  if not os.path.exists("resources/alert_history.json"):
    with open("resources/alert_history.json", "w") as f:
      json.dump({}, f)

  if not os.path.exists("resources/tracker_list.json"):
    with open("resources/tracker_list.json", "w") as f:
      json.dump([], f)

  if "-test" in sys.argv:
    if "-research" in sys.argv:
      stock_symbol = sys.argv[sys.argv.index("-research") + 1]

      stock_price = get_stock_price(stock_symbol)

      asyncio.run(run_research_pipeline(stock_symbol, stock_price.current_price, stock_price.previous_close))
    else:
      # CRON Job for tracking stock prices

      scheduler = BackgroundScheduler()
      scheduler.add_job(track_stocks, 'interval', minutes=1)
      scheduler.start()

      asyncio.run(chat_terminal())
  else:
    # CRON Job for tracking stock prices

    scheduler = BackgroundScheduler()
    scheduler.add_job(track_stocks, 'interval', hours=1)
    scheduler.start()

    # Run with: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    uvicorn.run(
      "main:app",
      host=os.getenv("HOST", "0.0.0.0"),
      port=int(os.getenv("PORT", "8000")),
      reload=True,
    )
