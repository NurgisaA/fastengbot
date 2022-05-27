from contextlib import suppress

from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.utils.exceptions import MessageNotModified
from sqlalchemy import select

from bot.common import answer_question, w_card
from bot.db.models import PlayerScore, Word
from bot.keyboards import generate_balls, switch_word


async def miss(call: types.CallbackQuery):
    """
    Invoked on red ball tap

    :param call: CallbackQuery from Telegram
    """
    db_session = call.bot.get("db")

    async with db_session() as session:
        await session.merge(PlayerScore(user_id=call.from_user.id, score=0))
        await session.commit()

    with suppress(MessageNotModified):
        await call.message.edit_text("Your score: 0", reply_markup=generate_balls())
    await call.answer()


async def hit(call: types.CallbackQuery):
    """
    Invoked on green ball tap

    :param call:CallbackQuery from Telegram
    """
    db_session = call.bot.get("db")

    async with db_session() as session:
        player: PlayerScore = await session.get(PlayerScore, call.from_user.id)
        # Note: we're incrementing client-side, not server-side
        player.score += 1
        await session.commit()

    # Since we have "expire_on_commit=False", we can use player instance here
    with suppress(MessageNotModified):
        await call.message.edit_text(f"Your score: {player.score}", reply_markup=generate_balls())
    await call.answer()


async def correct_answer(call: types.CallbackQuery):
    """
    Invoked on green ball tap

    :param call:CallbackQuery from Telegram
    """
    db_session = call.bot.get("db")

    data = call.data.split(':')
    print(data)
    async with db_session() as s:
        request = await s.execute(select(Word).filter_by(id=int(data[1])))
        word = request.scalars().first()
    # Since we have "expire_on_commit=False", we can use player instance here
    with suppress(MessageNotModified):
        await call.message.edit_text(f"Верно", reply_markup=switch_word(word, 'ru'))
    await call.answer()


async def incorrect_answer(call: types.CallbackQuery):
    """
    Invoked on green ball tap

    :param call:CallbackQuery from Telegram
    """
    db_session = call.bot.get("db")

    data = call.data.split(':')
    print(data)
    async with db_session() as s:
        request = await s.execute(select(Word).filter_by(id=int(data[1])))
        word = request.scalars().first()
    print(word)
    # Since we have "expire_on_commit=False", we can use player instance here
    with suppress(MessageNotModified):
        await call.message.edit_text(f"Неверно!\n", reply_markup=switch_word(word, 'ru'))
    await call.answer()


async def switch_card(call: types.CallbackQuery):
    """
    Invoked on green ball tap

    :param call:CallbackQuery from Telegram
    """
    db_session = call.bot.get("db")

    data = call.data.split(':')
    print(data)
    async with db_session() as s:
        request = await s.execute(select(Word).filter_by(id=int(data[1])))
        word = request.scalars().first()
    print(word)
    if not word:
        return
    if data[2] == 'en':
        into = 'ru'
        text = f"{word.original} {word.transcription}"
    else:
        into = 'en'
        text = word.translate
    # Since we have "expire_on_commit=False", we can use player instance here
    with suppress(MessageNotModified):
        await call.message.edit_text(f"{text}", reply_markup=switch_word(word, into))
    await call.answer()


def register_callbacks(dp: Dispatcher):
    # dp.register_callback_query_handler(miss, cb_balls.filter(color="red"))
    # dp.register_callback_query_handler(hit, cb_balls.filter(color="green"))
    dp.register_callback_query_handler(incorrect_answer, answer_question.filter(correct="0"))
    dp.register_callback_query_handler(correct_answer, answer_question.filter(correct="1"))
    dp.register_callback_query_handler(switch_card, w_card.filter(into="ru"))
    dp.register_callback_query_handler(switch_card, w_card.filter(into="en"))
