import os
from telebot import types

def get_teacher_menu():
    teachers = {
        "Olena Haitan": {
            "description": "📧Email: azalie@ukr.net\n📱phone: +380668075362",
            "image_path": "C:/Users/kawta/Desktop/My lessons/PFE/GAYTAN Olena.png"
        },
        "Kapiton Alla": {
            "description": "📧Email: kits_seminar@ukr.net\n📱phone: +380957065796",
            "image_path": "C:/Users/kawta/Desktop/My lessons/PFE/Alla Myroslavivna.png"
        },
        "Dvirna Olena": {
            "description": "📧Email: itm.dvirna@nupp.edu.ua\n📱phone: +380985531038",
            "image_path": "C:/Users/kawta/Desktop/My lessons/PFE/Dvirna Olena.png"
        },
        "Yanko Alina": {
            "description": "📧Email: al9_yanko@ukr.net\n📱phone: +380954238943",
            "image_path": "C:/Users/kawta/Desktop/My lessons/PFE/Yanko Alina.png"
        },
        "Vasyuta Vasyl": {
            "description": "📧Email: Vasuta_V_V@ukr.net",
            "image_path": "C:/Users/kawta/Desktop/My lessons/PFE/Vasyuta Vasyl.png"
        },
        "Skakalina Olena": {
            "description": "📧Email: wboss@i.ua",
            "image_path": "C:/Users/kawta/Desktop/My lessons/PFE/Skakalina Olena.png"
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
            "description": "📧Email: azalie@ukr.net\n📱phone: +380668075362",
            "image_path": "C:/Users/kawta/Desktop/My lessons/PFE/GAYTAN Olena.png"
        },
        "Kapiton Alla": {
            "description": "📧Email: kits_seminar@ukr.net\n📱phone: +380669440001",
            "image_path": "C:/Users/kawta/Desktop/My lessons/PFE/Alla Myroslavivna.png"
        },
        "Dvirna Olena": {
            "description": "📧Email: itm.dvirna@nupp.edu.ua\n📱phone: +380985531038",
            "image_path": "C:/Users/kawta/Desktop/My lessons/PFE/Dvirna Olena.png"
        },
        "Yanko Alina": {
            "description": "📧Email: al9_yanko@ukr.net\n📱phone: +380954238943",
            "image_path": "C:/Users/kawta/Desktop/My lessons/PFE/Yanko Alina.png"
        },
        "Zaika Svitlana":{
            "description": "📧Email: zaikasvetlana@gmail.com\n📱phone: +380689217025",
            "image_path": "C:/Users/kawta/Desktop/My lessons/PFE/Zaika Svitlana.png"

        }
        ,
        "Vasyuta Vasyl": {
            "description": "📧Email: Vasuta_V_V@ukr.net",
            "image_path": "C:/Users/kawta/Desktop/My lessons/PFE/Vasyuta Vasyl.png"
        },
        "Skakalina Olena": {
            "description": "📧Email: wboss@i.ua",
            "image_path": "C:/Users/kawta/Desktop/My lessons/PFE/Skakalina Olena.png"
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
