import telebot
import process
import units

bot_token = '1734461803:AAH_QT4-YbMxgbwjA0B2J69JTMTCrtFXmXQ'
bot = telebot.TeleBot(bot_token)


def pre_calc():
    for cls in units.Unit.__subclasses__():
        units.all_unit_types[cls.get_name()] = cls


pre_calc()
new_game = process.Process()
listOfCommands = {'/help': 'It shows this Help info',
                  '/print_units': 'It prints all your units',
                  '/attack [x]': 'You attack a generated team, if you win you get x coins',
                  '/show_coins': 'It shows you coins',
                  '/print_shop_info': 'It prints all prices in the shop',
                  '/buy [NAME]': 'You buy a [NAME] unit',
                  '/upgrade_unit [index]| [d/h]| [x]': 'Add [x] point to [index] unit [d] or [h]',
                  '/restart': 'Restart The Game'}


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, ''.join([f'{x} : {listOfCommands[x]}\n' for x in listOfCommands]))


@bot.message_handler(commands=['print_units'])
def send_print_units(message):
    bot.reply_to(message, 'Your team:\n' + new_game.team.get_info())


@bot.message_handler(commands=['attack'])
def send_attack_intro(message):
    bot.reply_to(message, 'Input level')
    bot.register_next_step_handler(message, send_attack)


@bot.message_handler(commands=['print_shop_info'])
def send_print_shop_info(message):
    res = ''
    for name in units.all_unit_types:
        res += f'{name} costs {units.all_unit_types[name].get_price()}\n'

    bot.reply_to(message, res)


def send_attack(message):
    try:
        level = int(message.text)
        if level < 0:
            raise ValueError
        bot.reply_to(message, new_game.attack(level))
    except ValueError:
        bot.reply_to(message, 'Input correct number >= 0, please')


@bot.message_handler(commands=['show_coins'])
def send_show_coins(message):
    bot.reply_to(message, new_game.show_coins())


@bot.message_handler(commands=['buy'])
def send_buy_intro(message):
    bot.reply_to(message, 'Input name')
    bot.register_next_step_handler(message, send_buy)


def send_buy(message):
    bot.reply_to(message, new_game.buy(message.text))


@bot.message_handler(commands=['upgrade_unit'])
def send_upgrade_unit_intro(message):
    bot.reply_to(message, 'Input index of unit')
    bot.register_next_step_handler(message, send_upgrade_unit_index)


last_index = 0
last_type = ''


def send_upgrade_unit_index(message):
    try:
        global last_index
        last_index = int(message.text)
        if last_index < 0 or last_index >= new_game.team.size():
            raise ValueError
        bot.reply_to(message, 'Input type of upgrade(damage / health)')
        bot.register_next_step_handler(message, send_upgrade_unit_type)
    except ValueError:
        bot.reply_to(message, 'Input correct number >= 0, please')


def send_upgrade_unit_type(message):
    if not (message.text in ['damage', 'health']):
        bot.reply_to(message, 'Incorrect type')
        return
    global last_type
    last_type = message.text
    bot.reply_to(message, 'Input the rate of change')
    bot.register_next_step_handler(message, send_upgrade_unit_value)


def send_upgrade_unit_value(message):
    try:
        value = int(message.text)
        bot.reply_to(message, new_game.upgrade_unit(last_index, last_type, value))
    except ValueError:
        bot.reply_to(message, 'Input correct number, please')


@bot.message_handler(commands=['restart'])
def send_restart_intro(message):
    bot.reply_to(message, 'Are You sure?(Yes/No)')
    bot.register_next_step_handler(message, send_restart)


def send_restart(message):
    ans = message.text.lower()
    if ans not in ['yes', 'no']:
        bot.reply_to(message, 'I think, it is "No" answer')
        return
    if ans == 'yes':
        global new_game
        new_game = process.Process()
        bot.reply_to(message, 'Done')
    else:
        bot.reply_to(message, 'OK')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'Welcome to the game, {message.from_user.first_name}!)))) \
Write the commands from below and play')
    send_help(message)


@bot.message_handler(content_types=['text'])
def start(message):
    bot.reply_to(message, 'Write commands from the list in /help')


bot.polling(True, 0)
