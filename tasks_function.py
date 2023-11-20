# library imports
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import time
global shuffled_check

progress_bar = [0,100] #current progress, final progress

async def getprogressbar(update, context):
    response_message = f"The progress of the tasks is currently at {progress_bar[0]}%"  
    await update.message.reply_text(response_message)

async def updateprogressbar(update, context):  #command only for admins
    args = float(''.join(context.args))
    progress_bar[0] = progress_bar[0] + args
    response_message = f"The progress of the tasks has been updated to {progress_bar[0]}%"  
    await update.message.reply_text(response_message)

async def killplayer(update, context):
    playerID = int(''.join(context.args))
    with open('kill_players.txt', 'a') as file:
        file.write(f"{playerID}\n")
        file.close()
    response_message = f"You have killed player {playerID}"  
    await update.message.reply_text(response_message)
    response_message = f"Your 30 seconds kill cooldown timer starts now."  
    await update.message.reply_text(response_message)
    time.sleep(10)
    response_message = f"The cooldown timer will end in 20 seconds."  
    await update.message.reply_text(response_message)
    time.sleep(10)
    response_message = f"The cooldown timer will end in 10 seconds."  
    await update.message.reply_text(response_message)
    time.sleep(10)
    response_message = f"Your 30 seconds kill cooldown timer is over. "  
    await update.message.reply_text(response_message)

# async def killplayer(update, context):
#     playerID = int(''.join(context.args))
#     with open('kill_players.txt', 'a') as file:
#         file.write(f"{playerID}\n")
#         file.close()
#     response_message = f"You have killed player {playerID}"  
#     await update.message.reply_text(response_message)
#     check_playergotkilled = False
#     while(not check_playergotkilled):
#         with open('gotkilled_players.txt', 'r') as file:
#             playerIDs = file.readlines()
#         if str(playerID) in playerIDs:
#             print("True")
#             response_message = f"Your 30 seconds kill cooldown timer starts now."  
#             await update.message.reply_text(response_message)
#             time.sleep(10)
#             response_message = f"The cooldown timer will end in 20 seconds."  
#             await update.message.reply_text(response_message)
#             time.sleep(10)
#             response_message = f"The cooldown timer will end in 10 seconds."  
#             await update.message.reply_text(response_message)
#             time.sleep(10)
#             response_message = f"Your 30 seconds kill cooldown timer is over. "  
#             await update.message.reply_text(response_message)
#             check_playergotkilled = True
    
# async def gotkilledplayer(update, context):
#     playerID = int(''.join(context.args))
#     print(playerID)
#     with open('gotkilled_players.txt', 'a') as file:
#         file.write(f"{playerID}")
#         file.close()
#     response_message = f"You have been killed."  
#     await update.message.reply_text(response_message)