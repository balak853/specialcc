import httpx
import time
import asyncio
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from FUNC.defs import *
from TOOLS.check_all_func import *
from TOOLS.getbin import *
from .response import *
from .gate import *


import json
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Function to fetch card details from API
def check_card(card_number):
    url = f"https://darkboy-b3.onrender.com/key=dark/cc={card_number}"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.text
        else:
            return f"⚠️ API Error: {response.status_code} - {response.reason}"
    
    except requests.exceptions.RequestException as e:
        return f"❌ Request Failed: {e}"

# Handler for 'tn <card_number>' command
def tn_handler(update: Update, context: CallbackContext):
    message = update.message.text
    parts = message.split()

    # Validate command format
    if len(parts) != 2 or not parts[1].isdigit() or not (13 <= len(parts[1]) <= 19):
        update.message.reply_text("❌ Invalid format. Use: tn <card_number>")
        return
    
    card_number = parts[1]
    
    update.message.reply_text(f"🔍 Checking card `{card_number}`... Please wait.", parse_mode="Markdown")

    # Fetch response from API
    response = check_card(card_number)

    # Send response to user
    update.message.reply_text(f"📡 **Response:**\n{response}", parse_mode="Markdown")

# Main function to start the bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add message handler for 'tn <card_number>' command
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.regex(r'^tn \d{13,19}$'), tn_handler))

    # Start the bot
    updater.start_polling()
    updater.idle()
