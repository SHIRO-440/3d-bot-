# pip install pytelegrambotapi

import telebot

TOKEN = '8542194250:AAE2LA4HTiY-avgtJHCK8OCeIh2u0QtSOpA'
bot = telebot.TeleBot(TOKEN)

# --- Постоянные значения ---
PRICE_PER_GRAM = 3       # ₽ за 1 грамм пластика
ELECTRICITY_PER_HOUR = 10   # ₽ за час работы принтера
PACKAGING_COST = 50        # ₽ упаковка
AMORTIZATION = 20          # ₽ амортизация

# Хранилище данных пользователей
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id

    user_data[chat_id] = {}

    bot.send_message(
        chat_id,
        "🤙 What's up my nigga!\n"
        "Я помогу рассчитать стоимость 3D-печати.\n\n"
        "Введите вес модели в граммах:"
    )

    bot.register_next_step_handler(message, get_weight)


def get_weight(message):
    chat_id = message.chat.id

    try:
        weight = float(message.text)
        user_data[chat_id]['weight'] = weight

        bot.send_message(
            chat_id,
            "⏱ Теперь введите время печати в часах:"
        )

        bot.register_next_step_handler(message, get_time)

    except:
        bot.send_message(chat_id, "❌ Введите число.")
        bot.register_next_step_handler(message, get_weight)


def get_time(message):
    chat_id = message.chat.id

    try:
        time_hours = float(message.text)
        user_data[chat_id]['time'] = time_hours

        calculate(chat_id)

    except:
        bot.send_message(chat_id, "❌ Введите число.")
        bot.register_next_step_handler(message, get_time)


def calculate(chat_id):
    weight = user_data[chat_id]['weight']
    time_hours = user_data[chat_id]['time']

    # Расчёты
    material_cost = weight * PRICE_PER_GRAM
    electricity_cost = time_hours * ELECTRICITY_PER_HOUR

    total = (
        material_cost
        + electricity_cost
        + PACKAGING_COST
        + AMORTIZATION
    )

    result = (
        f"📊 Расчёт стоимости:\n\n"
        f"🧵 Материал: {material_cost:.2f} ₽\n"
        f"⚡ Электричество: {electricity_cost:.2f} ₽\n"
        f"📦 Упаковка: {PACKAGING_COST} ₽\n"
        f"🔧 Амортизация: {AMORTIZATION} ₽\n\n"
        f"💰 Итоговая стоимость: {total:.2f} ₽"
    )

    bot.send_message(chat_id, result)


print("Бот запущен...")
bot.infinity_polling()