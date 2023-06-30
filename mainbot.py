import telebot
from telebot import types
from datetime import time
from time_helper import get_ukraine_time
from time_helper import is_weekend
import teachers
import logging
import sqlite3
from googletrans import Translator
from schedule import scrape_schedule
from RaidAlert import get_air_raid_alert
from bot_texts import text0, text2, text3 ,opt0, opt1, opt2,opt22,opt23,opt40,opt41,opt50,opt51,opt60,opt61,attacks




bot = telebot.TeleBot("Token")

translator = Translator()




@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text='📚 Education', callback_data="btn1")
    btn2 = types.InlineKeyboardButton(text='🗓️ Schedule', callback_data="btn2")
    btn3 = types.InlineKeyboardButton(text='🏫 About university', callback_data="btn3")
    btn4 = types.InlineKeyboardButton(text='☎️ University contacts', callback_data="btn4")
    btn6 = types.InlineKeyboardButton(text='🆘 Safety instructions in emergency situations', callback_data="btn6")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)
    markup.add(btn6)

    
    

    # Insert user into the database
    chat_id = message.chat.id
    username = message.chat.username
    insert_user(chat_id, username)
    

    # Send the welcome message
    welcome_message = "Welcome to National University Poltava Polytechnic Institute named after Yuri Kondratyuk 🤗. How can I help you today?"
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)
    

lecture_ranges = [
    (time(8, 0), time(9, 50)),
    (time(10, 0), time(11, 20)),
    (time(11, 30), time(12, 50)),
    (time(13, 30), time(14, 50)),
    (time(15, 0), time(16, 20)),
    (time(16, 30), time(17, 50))
]

@bot.message_handler(commands=['working_hours'])
def working_hours(message):
    ukraine_time = get_ukraine_time().time()

    if is_weekend():
        response = f"The current time in Ukraine is: {ukraine_time.strftime('%H:%M')}\n No classes available, It is weekend!😌"
    else:
        lecture_started = False
        for index, (start_time, end_time) in enumerate(lecture_ranges, start=1):
            if start_time <= ukraine_time <= end_time:
                response = f"The current time in Ukraine is: {ukraine_time.strftime('%H:%M')}\n🕣 Lecture {index} started."
                lecture_started = True
                break
        
        if not lecture_started:
            if time(18, 0) <= ukraine_time <= time(23, 59) or time(0, 0) <= ukraine_time <= time(8, 29):
                response = f"The current time in Ukraine is: {ukraine_time.strftime('%H:%M')}\n🌙 The university is closed. No classes available."
            else:
                response = f"The current time in Ukraine is: {ukraine_time.strftime('%H:%M')}\nBreak between sessions."
    
    

    menu_keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    Option1 = types.InlineKeyboardButton(text='1.🕣08:30-09:50', callback_data="Option1")
    Option2 = types.InlineKeyboardButton(text='2.🕙10:00-11:20', callback_data="Option2")
    Option3 = types.InlineKeyboardButton(text='3.🕦11:30-12:50', callback_data="Option3")
    Option4 = types.InlineKeyboardButton(text='4.🕜13:30-14:50', callback_data="Option4")
    Option5 = types.InlineKeyboardButton(text='5.🕒15:00-16:20', callback_data="Option5")
    Option6 = types.InlineKeyboardButton(text='6.🕒16:30-17:50', callback_data="Option6")
    menu_keyboard.add(Option1)
    menu_keyboard.add(Option2)
    menu_keyboard.add(Option3)
    menu_keyboard.add(Option4)
    menu_keyboard.add(Option5)
    menu_keyboard.add(Option6)
    response_message = f"{response}\n\n🗓Please see below the schedule of lectures🤗:"
    bot.send_message(message.chat.id, response_message, reply_markup=menu_keyboard)
    



@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
    message = call.message
    if call.data == "btn1":
    
        main_menu = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton(text="🔗Preparatory courses", url="https://nupp.edu.ua/")
        item2 = types.InlineKeyboardButton(text="🔗Bachelor", url="https://nupp.edu.ua/")
        item3 = types.InlineKeyboardButton(text="🔗Master", url="https://nupp.edu.ua/")
        item4 = types.InlineKeyboardButton(text="🔗Disance education", url="https://dist.nupp.edu.ua/login/index.php")
        back = types.InlineKeyboardButton(text="↩️ Back", callback_data="back")
        main_menu.add(item1)
        main_menu.add(item2)
        main_menu.add(item3)
        main_menu.add(item4)
        main_menu.add(back)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='What educational level are you interested in?', reply_markup=main_menu)
    
    elif call.data == "back":
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton(text='📚 Education',callback_data="btn1")
        btn2 = types.InlineKeyboardButton(text='🗓️ Schedule',callback_data="btn2")
        btn3 = types.InlineKeyboardButton(text='🏫 About university',callback_data="btn3")
        btn4 = types.InlineKeyboardButton(text='☎️ University contacts',callback_data="btn4")
        btn6 = types.InlineKeyboardButton(text='🆘 Safety instructions in emergency situations', callback_data="btn6")
        markup.add(btn1)
        markup.add(btn2)
        markup.add(btn3)
        markup.add(btn4)
        markup.add(btn6)

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, "Please select an option", reply_markup=markup)
       
    elif call.data == 'btn4':
         markup4 = types.InlineKeyboardMarkup(row_width=2)
         details = types.InlineKeyboardButton(text="University Contacts", callback_data="details")
         institutes = types.InlineKeyboardButton(text="List of institutes", callback_data="institutes")
         DPT = types.InlineKeyboardButton(text='👨‍🏫 Department', callback_data="DPT")
         back = types.InlineKeyboardButton(text="↩️ Back", callback_data="back")
         markup4.add(details)
         markup4.add(institutes)
         markup4.add(DPT)
         markup4.add(back)
         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Please select an option:', reply_markup=markup4)


    elif call.data == "btn3":
    
        second_menu = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton(text="🔗Administration", url="https://nupp.edu.ua/page/administratsiya.html")
        item2 = types.InlineKeyboardButton(text="🔗The pride of university", url="https://nupp.edu.ua/page/gordist-universitetu.html")
        item3 = types.InlineKeyboardButton(text="🔗History of university", url="https://nupp.edu.ua/page/istoriya.html")
        item4 = types.InlineKeyboardButton(text="🔗Virtual tour", url="https://nupp.edu.ua/page/virtualniy-tur.html")
        item5 = types.InlineKeyboardButton(text="🔗official information", url="https://nupp.edu.ua/page/official-information.html")
        back = types.InlineKeyboardButton(text="↩️ Back", callback_data="back")
        second_menu.add(item1)
        second_menu.add(item2)
        second_menu.add(item3)
        second_menu.add(item4)
        second_menu.add(item5)
        second_menu.add(back)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='What would you like to know ?', reply_markup=second_menu)
    
       
    
    elif call.data == "DPT":
       
        teacher_menu = teachers.get_teacher_menu()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Please select a teacher:", reply_markup=teacher_menu)

    elif call.data.startswith("teacher_"):
        teachers.handle_teacher_callback(call, bot)


    elif call.data == 'details':
            contacts="Contacts:  "
            latitude = 49.576187656554474
            longitude = 34.56688364039407
            bot.send_location(chat_id=call.message.chat.id,latitude=latitude, longitude=longitude)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=contacts)

    elif call.data == 'institutes':
             markup0= types.InlineKeyboardMarkup(row_width=2)
             option1= types.InlineKeyboardButton(text="Institute of Architecture, Construction and Land Management", callback_data="option1")
             option2= types.InlineKeyboardButton(text="Institute of Oil and Gas", callback_data="option2")
             option3= types.InlineKeyboardButton(text="Institute of Information Technologies and Robotics", callback_data="option3")
             option4= types.InlineKeyboardButton(text="Institute of Finance, Economics, Management and Law", callback_data="option4")
             option5= types.InlineKeyboardButton(text="Faculty of Philology, Psychology and Pedagogy", callback_data="option5")
             option6= types.InlineKeyboardButton(text="Faculty of physical culture and sports", callback_data="option6")
             back = types.InlineKeyboardButton(text="↩️ Back", callback_data="back")

             markup0.add(option1)
             markup0.add(option2)
             markup0.add(option3)
             markup0.add(option4)
             markup0.add(option5)
             markup0.add(option6)
             markup0.add(back)
             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Please select an institute to get more information 🤓:', reply_markup=markup0)
    
#listof instutes items
    elif call.data == "option1":
         bot.send_photo(chat_id=call.message.chat.id, photo='photo url', caption=opt0)
         bot.send_photo(chat_id=call.message.chat.id, photo='photo url', caption=opt1)
         bot.send_message(chat_id=call.message.chat.id, text=opt2)
    
    elif call.data == "option2":
         bot.send_photo(chat_id=call.message.chat.id, photo='photo url', caption=opt22)      
         bot.send_message(chat_id=call.message.chat.id, text=opt23)
    
    elif call.data == "option3":
         bot.send_photo(chat_id=call.message.chat.id, photo='photo url', caption=text0)
         bot.send_photo(chat_id=call.message.chat.id, photo='photo url', caption=text2)
         bot.send_message(chat_id=call.message.chat.id, text=text3)

    elif call.data == "option4":
         bot.send_photo(chat_id=call.message.chat.id, photo='photo url', caption=opt40)      
         bot.send_message(chat_id=call.message.chat.id, text=opt41)

    elif call.data == "option5":
         bot.send_photo(chat_id=call.message.chat.id, photo='photo url', caption=opt50)      
         bot.send_message(chat_id=call.message.chat.id, text=opt51)
    elif call.data == "option6":
         bot.send_photo(chat_id=call.message.chat.id, photo='photo url', caption=opt60)      
         bot.send_message(chat_id=call.message.chat.id, text=opt61)
  
#🆘 Safety instructions in emergency situations
    elif call.data == "btn6":
        markup5 = types.InlineKeyboardMarkup(row_width=2)
        itm1 = types.InlineKeyboardButton(text='⛑️First medical aid',callback_data="itm1")
        itm2 = types.InlineKeyboardButton(text='⚠️Mine danger',callback_data="itm2")
        itm3 = types.InlineKeyboardButton(text='💥Actions in case of shelling',callback_data="itm3")
        itm4 = types.InlineKeyboardButton(text='🚀Actions in case of rocket attack',callback_data="itm4")
        back = types.InlineKeyboardButton(text='↩️ Back', callback_data="back")
        markup5.add(itm1)
        markup5.add(itm2)
        markup5.add(itm3)
        markup5.add(itm4)
        markup5.add(back)

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, "Please kindly take a look at the safety instructions below 🤗: ", reply_markup=markup5)        
    

    elif call.data == "itm2":
            text=""" Please take a look at the following posters,
they contain important information and instructions regarding mine danger.
Stay Safe!😊"""
            bot.send_message(call.message.chat.id, text=text)
            picture_urls = [
        'photo url',
        'photo url'
        ]
            
            for url in picture_urls:
             bot.send_photo(chat_id=call.message.chat.id, photo=url )
    elif call.data == "itm3":
    
        
            picture_urls = [
        'https://mybotpics.s3.eu-west-2.amazonaws.com/shelling.png',
        'https://mybotpics.s3.eu-west-2.amazonaws.com/emergency.png'
        ]
            bot.send_message(call.message.chat.id, "Please read carefully the following instructions!")
            for url in picture_urls:
             
             bot.send_photo(chat_id=call.message.chat.id, photo=url)
    elif call.data == "itm4":
        bot.send_photo(chat_id=call.message.chat.id, photo="photo url" )
        bot.send_message(call.message.chat.id, text=attacks)
    ##
    elif call.data == "btn2":
            
    
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      btn1 = types.KeyboardButton('Today')
      btn2 = types.KeyboardButton('This week')
      btn3 = types.KeyboardButton('Next week')
      markup.add(btn1, btn2, btn3)
      bot.send_message(call.message.chat.id,'please select an option from the keyboard:', reply_markup=markup)

    
    

    
    elif call.data =="itm1":
                text1 = """ 
In the case of war or any emergency situation,
it is important to have some knowledge of first aid
to provide immediate medical assistance to those in need.
receiving proper medical training and assistance from professionals
should always be sought as soon as possible. 
In war or conflict situations, it is crucial to prioritize safety and
evacuation to a medical facility whenever feasible.
In a situation of socio-economic instability, 
an essential component of human security is training the population in first aid skills.
URCS First Aid Training Programs are certified by the Global Reference Center of the International Federation of Red Cross and Red Crescent Societies, so the certificates issued as a result of the training are recognized in 192 countries worldwide.
RCS First Aid Training has three certified 6, 12 and 48-hour programs, consisting of separate modules and containing 60% of the time for practical training of first aid skills.
If you want to get more information you may visit:
https://www.redcross.org/take-a-class/first-aid
https://redcross.org.ua/en/fat/
"""
                bot.send_photo(chat_id=call.message.chat.id, photo='https://mybotpics.s3.eu-west-2.amazonaws.com/first+Aid.png')
                bot.send_message(call.message.chat.id, text=text1)
###########################################
@bot.message_handler(commands=['time_raidalert'])
def time_raidalert(message):
    alert_message, formatted_last_update, formatted_date_now, duration = get_air_raid_alert()

    if alert_message == '🔕 POLTAVA REGION - NO AIR RAID ALERT IN ALL DIRECTIONS!😌':
        response = f'{alert_message}\n\n' \
                   f'Ukrainian time: {formatted_date_now}\n'
    else:
        duration_str = str(duration).split('.')[0]
        response = f'{alert_message}\n\n' \
                   f'Alert started: {formatted_last_update}\n' \
                   f'Ukrainian time: {formatted_date_now}\n' \
                   f'Duration: {duration_str}\n'
    bot.send_message(message.chat.id, response)

###########################################
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'today' or message.text.lower() == 'this week' or message.text.lower() == 'next week' or message.text.lower() == 'tomorrow':
        # Ask user for username and password
        bot.send_message(message.chat.id, "Please enter your username:")
        bot.register_next_step_handler(message, process_username, message.text.lower())

def process_username(message, request_type):
    username = message.text
    bot.send_message(message.chat.id, "Please enter your password:")
    bot.register_next_step_handler(message, process_password, request_type, username)

def process_password(message, request_type, username):
    password = message.text

    # Call the scrape_schedule function with the provided username, password, and request_type
    schedule = scrape_schedule(username, password, request_type)

    # Check if the schedule is a list of lessons or an error message
    if isinstance(schedule, list):
        # Convert the list of lessons to a string for sending in a message
        schedule_text = '\n'.join(schedule)
        bot.send_message(message.chat.id, schedule_text)
    else:
        bot.send_message(message.chat.id, schedule)




###########################################



# Create the users table if it doesn't exist
def create_users_table():
    # Database connection
    connect = sqlite3.connect('mybotdata.db')
    cursor = connect.cursor()

    # Create the users table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER,
                        group_id INTEGER
                    )''')

    connect.commit()
    cursor.close()
    connect.close()

# Insert a user into the table
def insert_user(chat_id, group_id):
    # Database connection
    connect = sqlite3.connect('mybotdata.db')
    cursor = connect.cursor()

    # Check if the user ID already exists in the table
    sql = "SELECT * FROM users WHERE id = ?"
    cursor.execute(sql, (chat_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        print(f"User with ID {chat_id} already exists in the database.")
    else:
        user = (chat_id, group_id)
        sql = "INSERT INTO users (id, group_id) VALUES (?, ?);"
        cursor.execute(sql, user)
        connect.commit()
        print(f"User with ID {chat_id} inserted into the database.")

    cursor.close()
    connect.close()

# Retrieve all users from the table
def retrieve_users():
    # Database connection
    connect = sqlite3.connect('mybotdata.db')
    cursor = connect.cursor()

    # Retrieve all users
    sql = "SELECT * FROM users"
    cursor.execute(sql)
    users = cursor.fetchall()

    cursor.close()
    connect.close()
    return users

# Example function to send a broadcast message to all users
def send_broadcast_message_to_all_users(message_text):
    # Database connection
    connect = sqlite3.connect('mybotdata.db')
    cursor = connect.cursor()

    # Retrieve all users
    users = retrieve_users()

    for user in users:
        chat_id = user[0]
        try:
            bot.send_message(chat_id, message_text)
            print(f"Message sent to user {chat_id}")
        except Exception as e:
            print(f"Failed to send message to user {chat_id}: {e}")

    cursor.close()
    connect.close()

logging.basicConfig(filename='error.log', level=logging.ERROR)

# Example function to send a message to users in a specific group
def send_message_to_group(group_name, message_text):
    # Database connection
    connect = sqlite3.connect('mybotdata.db')
    cursor = connect.cursor()

    # Decode the group name from bytes to string
    group_name = group_name.decode('utf-8')

    try:
        # Retrieve group ID based on the group name
        sql = "SELECT id FROM groups WHERE group_name = ?"
        cursor.execute(sql, (group_name,))
        group_id = cursor.fetchone()

        if group_id:
            group_id = group_id[0]
            # Retrieve users in the specified group
            sql = "SELECT id FROM users WHERE group_id = ?"
            cursor.execute(sql, (group_id,))
            group_users = cursor.fetchall()

            if group_users:
                for user in group_users:
                    chat_id = user[0]
                    try:
                        bot.send_message(chat_id, message_text)
                        print(f"Message sent to user {chat_id} in group {group_name}")
                    except Exception as e:
                        error_message = f"Failed to send message to user {chat_id} in group {group_name}: {e}"
                        encoded_error_message = error_message.encode('utf-8', 'ignore').decode('utf-8')
                        logging.error(encoded_error_message)
            else:
                print(f"No users found in the group {group_name}")
        else:
            error_message = f"No group found with the name {group_name}"
            encoded_error_message = error_message.encode('utf-8', 'ignore').decode('utf-8')
            logging.error(encoded_error_message)
    except Exception as e:
        error_message = f"An error occurred while sending the message to group {group_name}: {e}"
        encoded_error_message = error_message.encode('utf-8', 'ignore').decode('utf-8')
        logging.error(encoded_error_message)

    cursor.close()
    connect.close()

# Create the admin table if it doesn't exist
def create_admin_table():
    # Database connection
    connect = sqlite3.connect('mybotdata.db')
    cursor = connect.cursor()

    # Create the admin table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS admin (
                        id_admin INTEGER,
                        admin_name TEXT
                    )''')

    connect.commit()
    cursor.close()
    connect.close()

# Insert an admin into the table
def insert_admin(id_admin, admin_name):
    # Database connection
    connect = sqlite3.connect('mybotdata.db')
    cursor = connect.cursor()

    # Check if the admin ID already exists in the table
    sql = "SELECT * FROM admin WHERE id_admin = ?"
    cursor.execute(sql, (id_admin,))
    existing_admin = cursor.fetchone()

    if existing_admin:
        print(f"Admin with ID {id_admin} already exists in the database.")
    else:
        admin = (id_admin, admin_name)
        sql = "INSERT INTO admin (id_admin, admin_name) VALUES (?, ?);"
        cursor.execute(sql, admin)
        connect.commit()
        print(f"Admin {admin_name} inserted into the database.")

    cursor.close()
    connect.close()

# Check if a user is an admin
def is_admin(chat_id):
    # Database connection
    connect = sqlite3.connect('mybotdata.db')
    cursor = connect.cursor()

    # Check if the admin ID exists in the admin table
    sql = "SELECT * FROM admin WHERE id_admin = ?"
    cursor.execute(sql, (chat_id,))
    admin = cursor.fetchone()

    cursor.close()
    connect.close()
    return admin is not None

# Example command in your Telegram bot to send a broadcast message to all users
@bot.message_handler(commands=['broadcast'])
def handle_broadcast_command(message):
    chat_id = message.chat.id  # Get the chat ID of the sender
    admin_id = 745603189  # Your admin ID

    if is_admin(chat_id):
        # Admin is allowed to send a broadcast message
        bot.reply_to(message, "Please enter the message you want to send:")
        bot.register_next_step_handler(message, process_broadcast_message)
    else:
        # User is not authorized to use this function
        bot.reply_to(message, "You are not allowed to use this function.")

# Process the broadcast message entered by the admin
def process_broadcast_message(message):
    message_text = message.text.encode('utf-8')
    send_broadcast_message_to_all_users(message_text)
    bot.reply_to(message, "Broadcast message sent successfully.")

# Example command in your Telegram bot to send a message to a specific group
@bot.message_handler(commands=['send'])
def handle_send_command(message):
    chat_id = message.chat.id  # Get the chat ID of the sender
    admin_id = 745603189  # Your admin ID

    if is_admin(chat_id):
        # Admin is allowed to send a message
        bot.reply_to(message, "Please enter the group name:")
        bot.register_next_step_handler(message, process_group_name)
    else:
        # User is not authorized to use this function
        bot.reply_to(message, "You are not allowed to use this function.")

# Process the group name entered by the admin
def process_group_name(message):
    group_name = message.text.encode('utf-8')
    bot.reply_to(message, "Please enter the message you want to send:")
    bot.register_next_step_handler(message, process_send_message, group_name)

# Process the message entered by the admin and the group name
def process_send_message(message, group_name):
    message_text = message.text.encode('utf-8') 
    send_message_to_group(group_name, message_text)
    bot.reply_to(message, "Message sent successfully.")
#############################################
# Check if a user is already registered to a group
def is_user_registered(chat_id):
    connect = sqlite3.connect('mybotdata.db')
    cursor = connect.cursor()
    sql = "SELECT group_id FROM users WHERE id = ?"
    cursor.execute(sql, (chat_id,))
    group_id = cursor.fetchone()[0]
    cursor.close()
    connect.close()
    return group_id is not None

# Handle the /register command
@bot.message_handler(commands=['register'])
def handle_register_command(message):
    chat_id = message.chat.id
    if not is_user_registered(chat_id):
        bot.reply_to(message, "Please enter the group name:")
        bot.register_next_step_handler(message, process_group_name_registration)
    else:
        bot.reply_to(message, "You are already registered to a group.")

# Process the group name entered for registration
def process_group_name_registration(message):
    group_name = message.text
    chat_id = message.chat.id

    if is_group_exists(group_name):
        group_id = get_group_id(group_name)
        update_user_group(chat_id, group_id)
        bot.reply_to(message, f"You have been registered to the group {group_name}.")
    else:
        bot.reply_to(message, f"No group found with the name {group_name}.")

# Check if a group exists in the groups table
def is_group_exists(group_name):
    connect = sqlite3.connect('mybotdata.db')
    cursor = connect.cursor()
    sql = "SELECT * FROM groups WHERE group_name = ?"
    cursor.execute(sql, (group_name,))
    group = cursor.fetchone()
    cursor.close()
    connect.close()
    return group is not None

# Get the group ID for a given group name
def get_group_id(group_name):
    connect = sqlite3.connect('mybotdata.db')
    cursor = connect.cursor()
    sql = "SELECT id FROM groups WHERE group_name = ?"
    cursor.execute(sql, (group_name,))
    group_id = cursor.fetchone()[0]
    cursor.close()
    connect.close()
    return group_id

# Update the user's group in the users table
def update_user_group(chat_id, group_id):
    connect = sqlite3.connect('mybotdata.db')
    cursor = connect.cursor()
    sql = "UPDATE users SET group_id = ? WHERE id = ?"
    cursor.execute(sql, (group_id, chat_id))
    connect.commit()
    cursor.close()
    connect.close()

###########################################

if __name__ == '__main__':
 


        
 bot.polling(none_stop=True, interval=0)
