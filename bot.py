import config
import telebot
from telebot import types
from database import Database

db = Database('db.db')

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("👩🏼‍🤝‍👨🏿Пошук співрозмовника")
    markup.add(item1)

    bot.send_message(message.chat.id, 'Привіт, {0.first_name}! Ласкаво просимо до анонімного чату! Натисніть кнопку "Пошук співрозмовника".'.format(message.from_user), reply_markup=markup)

@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("👩🏼‍🤝‍👨🏿Пошук співрозмовника")
    markup.add(item1)

    bot.send_message(message.chat.id, '📄 Меню', reply_markup=markup)
    
@bot.message_handler(commands=['stop'])
def stop(message):
    chat_info = db.get_active_chat(message.chat.id)
    if chat_info != False:
        db.delete_chat(chat_info[0])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("👩🏼‍🤝‍👨🏿Пошук співрозмовника")
        markup.add(item1)
        
        bot.send_message(chat_info[1], '❌Співрозмовник покинув чат', reply_markup = markup)
        bot.send_message(message.chat.id, '❌Ви вийшли з чату', reply_markup = markup)
    else:
        bot.send_message(message.chat.id, '❌Ви не почали чат!', reply_markup = markup)
        

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        markup = None  

        if message.text == '👩🏼‍🤝‍👨🏿Пошук співрозмовника':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("❌ Зупинити пошук")
            markup.add(item1)

            chat_two = db.get_chat() # Беремо співрозмовника, який стоїть у черзі перший

            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id)
                bot.send_message(message.chat.id, '👀 Пошук співрозмовника', reply_markup=markup)
            else:
                mess = 'Співрозмовник не знайдений. Щоб припинити діалог, напишіть /stop'
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("/stop")
                markup.add(item1)
                
                bot.send_message(message.chat.id, mess, reply_markup=markup)
                bot.send_message(chat_two, mess, reply_markup=markup)

        elif message.text == "❌ Зупинити пошук":
            db.delete_queue(message.chat.id)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  
            bot.send_message(message.chat.id, '❌ Пошук припинено, напишіть /menu', reply_markup=markup)
            
        else:
            #Відправка повідомлення
            chat_info = db.get_active_chat(message.chat.id)
            bot.send_message(chat_info[1], message.text)

bot.polling(none_stop=True)
