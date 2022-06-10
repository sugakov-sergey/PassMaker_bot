from telebot import telebot  # you must pip install pyTelegramBotApi
from string import digits, ascii_letters
from random import choice
from settings import TOKEN

token = TOKEN

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(
        message.chat.id,
        "Для работы с ботом выберите нужный пункт меню в нижнем левом углу")


@bot.message_handler(commands=['create'])
def create_bot(message):
    bot.delete_message(message.chat.id, message.message_id)
    password = _create_pass()
    message_sent = 'Ваш новый пароль: \n\n' + password
    message_sent += '\n\nКликните, чтобы скопировать'
    message_sent += '\n\n★★★★★ Надежность высокая'
    bot.send_message(
        message.chat.id,
        message_sent, parse_mode='HTML')


@bot.message_handler(commands=['check'])
def check_bot(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(
        message.chat.id,
        'Введите Ваш пароль для проверки:')
    bot.register_next_step_handler(message, check_pass)


@bot.message_handler(commands=['help'])
def help_bot(message):
    bot.delete_message(message.chat.id, message.message_id)
    with open('pass_maker_bot.txt', encoding='utf-8') as f:
        text = '<b>Как создать надежный пароль?</b>\n\n' + f.read()
    bot.send_message(message.chat.id, text, parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def check_pass(message):
    """ Проверяет пароль на сложность"""
    dct = digits + ascii_letters
    password = message.text
    msg, level, cyrilic = 'error', set(), False
    top10 = ['123456', '123456789', 'qwerty', '12345', 'password',
             '12345678', 'qwerty123', '1q2w3e', '111111', '1234567890']

    if password in top10:
        msg = '<b>' + password + '</b>'
        msg += '\n\nСерьёзно? Бросай всё и быстро меняй пароль. Он входит '
        msg += 'в ТОП-10 самых популярных паролей в мире.'
        msg += '\n\n★☆☆☆☆ Надежность минимальная'

    elif len(password) <= 6:
        msg = '<b>' + password + '</b>'
        msg += '\n\nИспользовать пароль короче 6-ти символов крайне '
        msg += 'небезопасно. Подобрать его не составит особого труда.'
        msg += '\n\n★☆☆☆☆ Надежность минимальная'
    else:
        for i in password:
            if i not in dct: cyrilic = True
            if i.isalpha() and i.islower(): level.add('lower_alpha')
            if i.isalpha() and i.isupper(): level.add('upper_alpha')
            if i.isdigit(): level.add('digit')
            if 6 < len(password) < 9:
                level.add('6-10 len')
            elif 9 <= len(password) < 12:
                level.add('1'), level.add('2')
            elif len(password) >= 14:
                level.add('3'), level.add('4'), level.add('5'),

        if len(level) and cyrilic:
            msg = '<b>' + password + '</b>'
            msg += '\n\nБольшинство сервисов не поддерживает кирилицу, пробелы '
            msg += 'и другие специальные символы. Попробуйте другой вариант.'
            msg += '\n\nНекорректный пароль'

        elif len(level) < 4 and len(level) != 0:
            msg = '<b>' + password + '</b>'
            msg += '\n\nТакой пароль нельзя назвать надежным. Использование возможно'
            msg += ' в сферах с низкой ценностью информации. Желательно сменить.'
            msg += '\n\n★★☆☆☆ Надежность низкая'

        elif len(level) < 5 and len(level) != 0:
            msg = '<b>' + password + '</b>'
            msg += '\n\nИсходя из общих рекомендаций есть комбинация нескольких '
            msg += 'параметров. Уже неплохо, но желательно сменить.'
            msg += '\n\n★★★☆☆ Надежность средняя'

        elif len(level) < 6 and len(level) != 0:
            msg = '<b>' + password + '</b>'
            msg += '\n\nУровень сложности пароля подходящий. Если не использовать'
            msg += ' для критически важной информации, то можно оставить.'
            msg += '\n\n★★★★☆ Надежность хорошая'

        elif len(level) >= 6 and len(level) != 0:
            msg = '<b>' + password + '</b>'
            msg += '\n\nОтличный пароль! Ваша информация защищена от взлома '
            msg += 'путем подбора. Злоумышленникам не хватит на это времени.'
            msg += '\n\n★★★★★ Надежность высокая'

    print(level)
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, msg, parse_mode='HTML')


def _create_pass():
    """ Генерирует пароль и возвращает его """
    dct = digits + ascii_letters
    password = '<code>'
    password += ''.join(choice(dct) for _ in range(14))
    password += '</code>'
    return password


if __name__ == "__main__":
    bot.polling(none_stop=True)
