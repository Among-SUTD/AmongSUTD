# library imports
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler, CallbackContext
from datetime import datetime, timedelta

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): # called every time /start command is received
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Please click /command to view the available commands")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE): #listens for regular messages
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE): #/caps argument: command that will take some text as an argument
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE): #reply to all commands that were not recognized
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

async def list_commands(update: Update, context: CallbackContext):
    from main import commands
    command_list = "\n".join([f"/{command} - {description}" for command, description in commands])
    await update.message.reply_text("Available commands:\n\n" + command_list)


imposters_assigned = 0
async def playerID(update, context): #Assign PlayerID
    from player_groups import user_to_player_mapping, generate_new_player_id, save_mappings_to_file, num_imposters, user_to_player_mapping2, available_player_ids
    response_imposters = ""
    num_imposters = 2
    global imposters_assigned
    try:
        user_id = update.message.from_user.id
        user_name = update.message.from_user.username
        if user_id in user_to_player_mapping:
            player_id = user_to_player_mapping[user_id]        
        else:
            if available_player_ids:
                player_id = generate_new_player_id()
                user_to_player_mapping[user_id] = (player_id, user_name)
                user_to_player_mapping2[user_id] = (player_id, "normal")
                if player_id is not None:
                    if imposters_assigned < num_imposters: # Check if there are imposters left to assign
                        response_imposters = "You are an imposter \nYour kill command is /killplayer (playerID). \nFor example: /killplayer 1"
                        await update.message.reply_text(response_imposters)
                        user_to_player_mapping2[user_id] = (player_id, "imposter")
                        imposters_assigned += 1
                    # if user_to_player_mapping2[user_id][1] == 'normal':
                    #     await update.message.reply_text("This is the command to type when you have been killed by the imposters: \n/gotkilledplayer (your playerID). \nFor example: /gotkilledplayer 1")
            else:
                insufficient_message ="There is sufficient team players currently. Please try again."  
                await update.message.reply_text(insufficient_message)
        save_mappings_to_file('user_to_player_mappings.txt', user_to_player_mapping) # Save the updated mappings to the file
        save_mappings_to_file('imposter.txt', user_to_player_mapping2)
        response_message = f"Your player ID is {player_id}."  
        await update.message.reply_text(response_message)
        #print("Command '/playerID' was triggered.")  # For debugging
    except Exception as e:
        print(f"Error: {e}")

#Assign Groups Game 1
async def show_groups(update, context):
    from player_groups import groups1, user_to_player_mapping
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    #player_id = user_to_player_mapping[user_id]
    player_id = user_to_player_mapping.get(user_id)
    if player_id is not None:
        player_id_string = 'Player' + str(player_id[0])
        group_assignment = None # Find the group containing the player
        group_index = None
        for i, group in enumerate(groups1):
            if player_id_string in group:
                group_assignment = group
                group_index = i
                break
        if group_assignment is not None: # Check if the player is found in any group
            game_names = ['Draw a Card','Ordering History','Celebration Chaos','Global Roots']
            group_message = f"Player {player_id[0]}, Your group assignment for game 1 is: {game_names[group_index]}"
        else:
            group_message = f"Player {player_id[0]} is not assigned to any group."
    else:
        group_message = "You are not assigned a player ID. Please use /playerID to get your player ID."
    #await context.bot.send_message(chat_id=chat_id, text=group_message)
    await update.message.reply_text(group_message)
    file_path = 'game 1 groupings.txt'
    with open(file_path, 'w') as file: # Write the groups to the text file
        for group in groups1:
            line = ', '.join(group)
            file.write(f"{line}\n")
    # if(player_id is not None):
    #     playeriddd = "Player" + str(player_id)
    #     found = False

    #     for i, group in enumerate(groups1, 1):
    #         group_message += f"Group {i}: {', '.join(map(str, group))}\n"
    #         #print("Group: ",group)
    #         if playeriddd in group:
    #             group_assignment = i
    #             #print(f'{playeriddd} is in group: {group_assignment}')
    #             group_message = f"Your group assignment for game 1 is: {group_assignment}"
    #             await context.bot.send_message(chat_id=chat_id, text=group_message)
    #             groups_mapping1[1] = (groups1)
    #             found = True  # Set the flag to indicate the player was found in a group
    #             break  # Exit the loop after finding the player in a group

   
    #print(group_message)
    #save_mappings_to_file('game 1 groupings.txt', groups1)
    # if not found:
    #     #print(f'{playeriddd} is not found in the list.')
    #     await context.bot.send_message(chat_id=chat_id, text="You do not have a group assignment.") 

#Assign Groups Game 2
async def show_groups_2(update, context):
    from player_groups import groups2, user_to_player_mapping
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    player_id = user_to_player_mapping.get(user_id)
    if player_id is not None:
        player_id_string = 'Player' + str(player_id[0])
        group_assignment = None # Find the group containing the player
        group_index = None
        for i, group in enumerate(groups2):
            if player_id_string in group:
                group_assignment = group
                group_index = i
                break
        if group_assignment is not None: # Check if the player is found in any group
            game_names = ['Draw a Card','Ordering History','Celebration Chaos','Global Roots']
            group_message = f"Player {player_id[0]}, Your group assignment for game 2 is: {game_names[group_index]}"
        else:
            group_message = f"Player {player_id[0]} is not assigned to any group."
    else:
        group_message = "You are not assigned a player ID. Please use /playerID to get your player ID."
    await update.message.reply_text(group_message)
    file_path = 'game 2 groupings.txt'
    with open(file_path, 'w') as file: # Write the groups to the text file
        for group in groups2:
            line = ', '.join(group)
            file.write(f"{line}\n")

#Assign Groups Game 3
async def show_groups_3(update, context):
    from player_groups import groups3, user_to_player_mapping, groups_mapping3, save_mappings_to_file
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    player_id = user_to_player_mapping.get(user_id)
    if player_id is not None:
        player_id_string = 'Player' + str(player_id[0])
        group_assignment = None # Find the group containing the player
        group_index = None
        for i, group in enumerate(groups3):
            if player_id_string in group:
                group_assignment = group
                group_index = i
                break
        if group_assignment is not None: # Check if the player is found in any group
            game_names = ['Draw a Card','Ordering History','Celebration Chaos','Global Roots']
            group_message = f"Player {player_id[0]}, Your group assignment for game 3 is: {game_names[group_index]}"
        else:
            group_message = f"Player {player_id[0]} is not assigned to any group."
    else:
        group_message = "You are not assigned a player ID. Please use /playerID to get your player ID."
    #await context.bot.send_message(chat_id=chat_id, text=group_message)
    await update.message.reply_text(group_message)
    file_path = 'game 3 groupings.txt'
    with open(file_path, 'w') as file: # Write the groups to the text file
        for group in groups3:
            line = ', '.join(group)
            file.write(f"{line}\n")

#Assign Groups Game 4
async def show_groups_4(update, context):
    from player_groups import groups4, user_to_player_mapping, groups_mapping4, save_mappings_to_file
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    player_id = user_to_player_mapping.get(user_id)
    if player_id is not None:
        player_id_string = 'Player' + str(player_id[0])
        group_assignment = None # Find the group containing the player
        group_index = None
        for i, group in enumerate(groups4):
            if player_id_string in group:
                group_assignment = group
                group_index = i
                break
        if group_assignment is not None: # Check if the player is found in any group
            game_names = ['Draw a Card','Ordering History','Celebration Chaos','Global Roots']
            group_message = f"Player {player_id[0]}, Your group assignment for game 4 is: {game_names[group_index]}"
        else:
            group_message = f"Player {player_id[0]} is not assigned to any group."
    else:
        group_message = "You are not assigned a player ID. Please use /playerID to get your player ID."
    #await context.bot.send_message(chat_id=chat_id, text=group_message)
    await update.message.reply_text(group_message)
    file_path = 'game 4 groupings.txt'
    with open(file_path, 'w') as file: # Write the groups to the text file
        for group in groups4:
            line = ', '.join(group)
            file.write(f"{line}\n")

#Voting
async def vote(update: Update, context: CallbackContext) -> None: #Function to handle voting
    from player_groups import votes
    user_id = update.message.from_user.id
    if user_id in context.user_data and context.user_data[user_id]['votes_left'] <= 0: # Initialize user_data if not present
        await update.message.reply_text("You have already used all your votes.")
        return 
    context.user_data[user_id] = {'votes_left': 2} # Reset user_data for the user 
    await show_player_keyboard(update, context) # Show player keyboard

async def show_player_keyboard(update: Update, context: CallbackContext) -> None: # Show the player keyboard with checkboxes
    from player_groups import user_to_player_mapping
    user = update.effective_user
    user_id = update.effective_user.id
    player_id = user_to_player_mapping.get(user_id)
    if player_id is not None:
    #player_id_string = 'Player' + str(player_id[0])
        # with open('gotkilled_players.txt', 'r') as file:
        #         playerIDs = file.readlines()
        #         if str(playerID) in player_id:
        #             print("True")
        #         else:
        buttons = [ # Create a list of InlineKeyboardButtons with two buttons per row
            [
                InlineKeyboardButton(f'Player {i}', callback_data=f'vote_{i}'),
                InlineKeyboardButton(f'Player {i + 1}', callback_data=f'vote_{i + 1}')
            ] for i in range(1, 25, 2)  # Incrementing by 2 to get two players per row
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        if 'votes_left' not in context.user_data[user_id] or context.user_data[user_id]['votes_left'] == 2: # Check if the user has already started voting
            await update.message.reply_text(f'Hello, Player {str(player_id[0])}! Select 2 players to vote for:', reply_markup=reply_markup)
    else:
        await update.message.reply_text("You are not assigned a player ID. Please use /playerID to get your player ID.")

async def button(update: Update, context: CallbackContext) -> None: # Callback handler for button presses
    from player_groups import votes
    query = update.callback_query
    if query is None:
        return
    user_id = query.from_user.id
    if 'votes_left' not in context.user_data[user_id] or context.user_data[user_id]['votes_left'] <= 0: # Check if the user has used all their votes
        await query.answer(text="You have already used all your votes.")
        return
    player_number = int(query.data.split('_')[1])
    player_key = f'Player {player_number}'
    if player_key not in votes:
        await query.answer(text=f"Invalid player number: {player_number}")
        return
    votes[player_key] += 1
    context.user_data[user_id]['votes_left'] -= 1
    if context.user_data[user_id]['votes_left'] <= 0: # Check if the user has used all their votes after the current vote
        await query.answer(text="You have used all your votes.")
    else:
        await query.answer(text=f"Vote for {player_key} recorded. {context.user_data[user_id]['votes_left']} votes left.")
        await show_player_keyboard(update, context)

async def results(update: Update, context: CallbackContext) -> None: # Display results
    from player_groups import votes
    result_text = "\n".join([f"{player}: {count} votes" for player, count in votes.items()])
    await update.message.reply_text(f"Current Vote Counts:\n{result_text}")