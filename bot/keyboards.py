from random import randint

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.common import cb_balls, answer_question, w_card


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


def generate_question(words, true_answer) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)

    buttons = [
        InlineKeyboardButton(
            text=str(item.translate),
            callback_data=answer_question.new(
                answer_id=true_answer.id,
                correct='1' if true_answer.translate == item.translate else '0'
            )
        ) for item in words
    ]

    kb.add(*buttons)
    return kb


def switch_word(word, into) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)

    buttons = [
        InlineKeyboardButton(
            text='🔄',
            callback_data=w_card.new(
                answer_id=word.id,
                into=into,
                type='switch',
            )
        ),
        InlineKeyboardButton(
            text='>>>',
            callback_data=w_card.new(
                answer_id=word.id,
                into=into,
                type='next_card',
            )
        )
    ]

    kb.add(*buttons)
    return kb
