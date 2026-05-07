import telebot

# ВСТАВЬ СЮДА СВОЙ ТОКЕН
TOKEN = '8542194250:AAE2LA4HTiY-avgtJHCK8OCeIh2u0QtSOpA'

bot = telebot.TeleBot(TOKEN)

# ----------------------------
# ПОСТОЯННЫЕ РАСХОДЫ
# ----------------------------

PRICE_PER_GRAM = 3       # ₽ за 1 грамм пластика
ELECTRICITY_PER_HOUR = 10   # ₽ за час работы принтера
PACKAGING_COST = 50        # ₽ упаковка
AMORTIZATION = 20          # ₽ амортизация

# ----------------------------
# ХРАНЕНИЕ ДАННЫХ
# ----------------------------

user_data = {}

# ----------------------------
# СТАРТ
# ----------------------------

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id

    user_data[chat_id] = {}

    bot.send_message(
        chat_id,
        "🤙 What's up my nigga!\n\n"
        "Я помогу рассчитать стоимость 3D-печати.\n\n"
        "🧵 Введите вес модели в граммах:"
    )

    bot.register_next_step_handler(message, get_weight)


# ----------------------------
# ВЕС МОДЕЛИ
# ----------------------------

def get_weight(message):
    chat_id = message.chat.id

    try:
        weight = float(message.text.replace(",", "."))

        if weight <= 0:
            raise ValueError

        user_data[chat_id]['weight'] = weight

        bot.send_message(
            chat_id,
            "⏱ Теперь введите время печати в часах:"
        )

        bot.register_next_step_handler(message, get_time)

    except:
        bot.send_message(
            chat_id,
            "❌ Введите корректный вес.\n"
            "Например: 45 или 45.5"
        )

        bot.register_next_step_handler(message, get_weight)


# ----------------------------
# ВРЕМЯ ПЕЧАТИ
# ----------------------------

def get_time(message):
    chat_id = message.chat.id

    try:
        time_hours = float(message.text.replace(",", "."))

        if time_hours <= 0:
            raise ValueError

        user_data[chat_id]['time'] = time_hours

        calculate(chat_id)

    except:
        bot.send_message(
            chat_id,
            "❌ Введите корректное время.\n"
            "Например: 3 или 3.5"
        )

        bot.register_next_step_handler(message, get_time)


# ----------------------------
# РАСЧЁТ
# ----------------------------

def calculate(chat_id):
    weight = user_data[chat_id]['weight']
    time_hours = user_data[chat_id]['time']

    # Материал
    material_cost = weight * PRICE_PER_GRAM

    # Электричество
    electricity_cost = time_hours * ELECTRICITY_PER_HOUR

    # Итог
    total = (
        material_cost
        + electricity_cost
        + PACKAGING_COST
        + AMORTIZATION
    )

    result = (
        f"📊 Расчёт стоимости:\n\n"
        f"🧵 Вес модели: {weight} г\n"
        f"⏱ Время печати: {time_hours} ч\n\n"
        f"🧵 Материал: {material_cost:.2f} ₽\n"
        f"⚡ Электричество: {electricity_cost:.2f} ₽\n"
        f"📦 Упаковка: {PACKAGING_COST} ₽\n"
        f"🔧 Амортизация: {AMORTIZATION} ₽\n\n"
        f"💰 Итоговая стоимость:\n"
        f"{total:.2f} ₽"
    )

    bot.send_message(chat_id, result)


# ----------------------------
# ЗАПУСК БОТА
# ----------------------------

print("Бот запущен...")

bot.infinity_polling(
    timeout=60,
    long_polling_timeout=60
)