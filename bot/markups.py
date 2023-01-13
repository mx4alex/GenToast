from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_button1 = KeyboardButton("Информация о боте🤖")
main_button2 = KeyboardButton("Сгенерировать тост🥂")

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(main_button1).add(main_button2)

button1 = KeyboardButton('Новый год🎄')
button2 = KeyboardButton('День рождения🎂')
button3 = KeyboardButton('23 февраля🪖')
button4 = KeyboardButton('8 марта🌷')
button5 = KeyboardButton('Свадьба💍')

celebration_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    button1).add(button2).add(button3).add(button4).add(button5)