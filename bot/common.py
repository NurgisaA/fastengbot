from aiogram.utils.callback_data import CallbackData

cb_balls: CallbackData = CallbackData("ball", "color")
answer_question: CallbackData = CallbackData("question", "answer_id", "correct")
w_card: CallbackData = CallbackData("w_card", "answer_id", "into", 'type')
