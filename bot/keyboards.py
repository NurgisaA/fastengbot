from random import randint

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.common import cb_balls


def generate_balls() -> InlineKeyboardMarkup:
    balls_mask = [False] * 9
    balls_mask[randint(0, 8)] = True
    balls = ["🔴", "🟢"]
    data = ["red", "green"]
    kb = InlineKeyboardMarkup(row_width=3)
    buttons = [
        InlineKeyboardButton(
            text=balls[item],
            callback_data=cb_balls.new(color=data[item])
        ) for item in balls_mask
    ]
    kb.add(*buttons)
    return kb


def generate_question() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=4)
    buttons = [
        InlineKeyboardButton(
            text=str(item),
            callback_data='false'
        ) for item in range(3)
    ]
    buttons.insert(randint(0, 3),
                   InlineKeyboardButton(
                       text='true',
                       callback_data='true'
                   ))
    kb.add(*buttons)
    return kb
