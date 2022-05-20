from aiogram import types, Dispatcher
from sqlalchemy import select

from bot.db.models import PlayerScore, User, Role
from bot.keyboards import generate_balls, generate_question


async def create_role(message: types.Message, name: str, code: str):
    admin_id = message.bot.get("admin_id")

    if message.from_user.id != admin_id:
        return
    db_session = message.bot.get("db")
    query = select(Role).where(Role.code == code)
    async with db_session() as session:
        query_result = await session.execute(query)

        result = query_result.first()
        if result:
            result = await session.merge(Role(name=name, code=code))
        # pass
        await session.merge(User(id=message.from_user.id, role=result))
        await session.commit()
        return result


async def cmd_install(message: types.Message):
    admin_id = message.bot.get("admin_id")

    if message.from_user.id != admin_id:
        return
    await create_role(message, 'Admin', 'admin')
    await create_role(message, 'Premium', 'premium')
    await create_role(message, 'Subscriber', 'subscriber')

    await message.answer("ok!")


async def cmd_start(message: types.Message):
    db_session = message.bot.get("db")

    print(message.from_user.id)
    sql = select(User).where(User.id == message.from_user.id)
    # await message.answer("")
    async with db_session() as session:
        result = await session.execute(sql)
        user = result.first()

        if user:
            await message.answer(f"Hello!")
        else:
            await session.merge(User(id=message.from_user.id, role_id=1))
            await session.commit()

    await message.answer("Hi there! This is a simple clicker bot. Tap on green ball, but don't tap on red ones!\n"
                         "If you tap a red ball, you'll have to start over.\n\n"
                         "Enough talk. Just tap /play and have fun!")


async def cmd_play(message: types.Message):
    db_session = message.bot.get("db")

    async with db_session() as session:
        await session.merge(PlayerScore(user_id=message.from_user.id, score=0))
        await session.commit()

    await message.answer("Your score: 0", reply_markup=generate_balls())


async def get_card(message: types.Message):
    await message.answer("word  [transcript]", reply_markup=generate_question())


async def cmd_top(message: types.Message):
    db_session = message.bot.get("db")
    sql = select(PlayerScore).order_by(PlayerScore.score.desc()).limit(5)
    text_template = "Top 5 players:\n\n{scores}"
    async with db_session() as session:
        top_players_request = await session.execute(sql)
        players = top_players_request.scalars()

    score_entries = [f"{index + 1}. ID{item.user_id}: <b>{item.score}</b>" for index, item in enumerate(players)]
    score_entries_text = "\n".join(score_entries) \
        .replace(f"{message.from_user.id}", f"{message.from_user.id} (it's you!)")
    await message.answer(text_template.format(scores=score_entries_text), parse_mode="HTML")


def register_commands(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(cmd_install, commands="install")
    dp.register_message_handler(get_card, commands="get")
    dp.register_message_handler(cmd_play, commands="play")
    dp.register_message_handler(cmd_top, commands="top")
