# library imports
#import re
#import telegram
import logging
#import random
from telegram import Update, BotCommand, Bot, KeyboardButton
from telegram.ext import Application, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
import threading

# file imports
import yaml
from functions import start, unknown, echo, caps, show_groups, show_groups_2, show_groups_3, show_groups_4, playerID, vote, button, results, list_commands
from tasks_function import getprogressbar, updateprogressbar, killplayer

with open('config.yaml', 'r') as file:
    telebot_settings = yaml.safe_load(file)
    print(telebot_settings)

# logging.basicConfig( # Exceptions, Warnings and Logging
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.DEBUG
# )

#Availble commands
commands = [
    ('start', 'Start the bot and get a welcome message'),
    ('command', 'Show available commands'),
    ('playerID', 'Get your player ID'),
    ('game_1_groupings', 'Get your groupings for Game 1'),
    ('game_2_groupings', 'Get your groupings for Game 2'),
    ('game_3_groupings', 'Get your groupings for Game 3'),
    ('game_4_groupings', 'Get your groupings for Game 4'),
    ('getprogressbar', 'Get progress of complete tasks'),
    ('vote', 'Vote for the suspected imposters'),
    ('results', 'Check voting results for suspected imposters')
]

if __name__ == '__main__':
    application = ApplicationBuilder().token(telebot_settings['apitoken']).build()
    
    application.add_handler(CommandHandler('start', start))

    application.add_handler(CommandHandler('command', list_commands))

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo) #echo all text messages
    application.add_handler(echo_handler)

    player_handler = CommandHandler('playerID', playerID) #PlayerID
    application.add_handler(player_handler)

    showGroups_handler = CommandHandler('game_1_groupings', show_groups) #Groupings Game 1
    application.add_handler(showGroups_handler)
    
    showGroups2_handler = CommandHandler('game_2_groupings', show_groups_2) #Groupings Game 2
    application.add_handler(showGroups2_handler)

    showGroups3_handler = CommandHandler('game_3_groupings', show_groups_3) #Groupings Game 3
    application.add_handler(showGroups3_handler)

    showGroups4_handler = CommandHandler('game_4_groupings', show_groups_4) #Groupings Game 4
    application.add_handler(showGroups4_handler)

    application.add_handler(CommandHandler('vote', vote)) #Vote
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler('results', results)) #Voting results

    get_ProgressBar_handler = CommandHandler('getprogressbar', getprogressbar) # get progress bar
    application.add_handler(get_ProgressBar_handler)

    update_ProgressBar_handler = CommandHandler('updateprogressbar', updateprogressbar) # update progress bar
    application.add_handler(update_ProgressBar_handler)

    kill_player_handler = CommandHandler('killplayer', killplayer) # kill player
    application.add_handler(kill_player_handler)

    # start_handler = CommandHandler('start', start) #listen to /start commands, use a CommandHandler
    # application.add_handler(start_handler)
    unknown_handler = MessageHandler(filters.COMMAND, unknown) #send back 
    application.add_handler(unknown_handler)

    application.run_polling() #runs the bot until you hit CTRL+C