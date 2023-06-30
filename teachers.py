import os
from telebot import types

def get_teacher_menu():
    teachers = {
        "Olena Haitan": {
            "description": "📧Email: \n📱phone: ",
            "image_path": "GAYTAN Olena.png"
        },
        "Kapiton Alla": {
            "description": "📧Email: \n📱phone: ",
            "image_path": "Alla Myroslavivna.png"
        },
        "Dvirna Olena": {
            "description": "📧Email: \n📱phone:",
            "image_path": "Dvirna Olena.png"
        },
        "Yanko Alina": {
            "description": "📧Email:\n📱phone:",
            "image_path": "/Yanko Alina.png"
        },
        "Vasyuta Vasyl": {
            "description": "📧Email:",
            "image_path": "Vasyuta Vasyl.png"
        },
        "Skakalina Olena": {
            "description": "📧Email:",
            "image_path": "Skakalina Olena.png"
        }
    }

    teacher_menu = types.InlineKeyboardMarkup(row_width=1)
    back_button = types.InlineKeyboardButton(text="↩️ Back", callback_data="back")
    teacher_menu.add(back_button)

    for teacher, info in teachers.items():
        teacher_button = types.InlineKeyboardButton(text=f"👨‍🏫 {teacher}", callback_data=f"teacher_{teacher}")
        teacher_menu.add(teacher_button)

    return teacher_menu

def handle_teacher_callback(call, bot):
    teacher_name = call.data.split("_", 1)[1]
    teachers = {
        "Olena Haitan": {
            "description": "📧Email: \n📱phone: ",
            "image_path": "GAYTAN Olena.png"
        },
        "Kapiton Alla": {
            "description": "📧Email: \n📱phone: ",
            "image_path": "Alla Myroslavivna.png"
        },
        "Dvirna Olena": {
            "description": "📧Email: \n📱phone:",
            "image_path": "Dvirna Olena.png"
        },
        "Yanko Alina": {
            "description": "📧Email:\n📱phone:",
            "image_path": "/Yanko Alina.png"
        },
        "Vasyuta Vasyl": {
            "description": "📧Email:",
            "image_path": "Vasyuta Vasyl.png"
        },
        "Skakalina Olena": {
            "description": "📧Email:",
            "image_path": "Skakalina Olena.png"
        }
    }

    if teacher_name in teachers:
        teacher_info = teachers[teacher_name]
        description = teacher_info["description"]
        image_path = teacher_info["image_path"]

        # Check if the image file exists
        if os.path.isfile(image_path):
            # Send the image along with the description
            with open(image_path, "rb") as image_file:
                bot.send_photo(chat_id=call.message.chat.id, photo=image_file, caption=f"👨‍🏫 {teacher_name}\n{description}")
        else:
            response = f"👨‍🏫 {teacher_name}\n{description}\nImage not found."
            bot.send_message(chat_id=call.message.chat.id, text=response)
    else:
        response = "Teacher not found."
        bot.send_message(chat_id=call.message.chat.id, text=response)
