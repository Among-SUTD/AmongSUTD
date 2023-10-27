# library imports
import logging
from telegram import Update, BotCommand
from telegram.ext import Application, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler

# file imports
import yaml
from functions import start, unknown, echo, caps

with open('AmongSUTD\config.yaml', 'r') as file:
    telebot_settings = yaml.safe_load(file)
    print(telebot_settings)

# logging.basicConfig( # Exceptions, Warnings and Logging
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.DEBUG
# )

if __name__ == '__main__':
    application = ApplicationBuilder().token(telebot_settings['apitoken']).build()
    
    application.add_handler(CommandHandler('start', start))

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo) #echo all text messages
    application.add_handler(echo_handler)

    # start_handler = CommandHandler('start', start) #listen to /start commands, use a CommandHandler
    # application.add_handler(start_handler)
    unknown_handler = MessageHandler(filters.COMMAND, unknown) #send back 
    application.add_handler(unknown_handler)

    application.run_polling() #runs the bot until you hit CTRL+C