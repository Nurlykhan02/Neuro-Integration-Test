from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def build_answers(question_id: int, answers: list) -> InlineKeyboardMarkup:
    res = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(f"{answer[0] % 4 if answer[0] % 4 else 4}",
                              callback_data=f"ans:{question_id}:{answer[0]}")
         for answer in answers]
    ])

    return res


def menu() -> ReplyKeyboardMarkup:
    res = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton("Тесты"), KeyboardButton("Задать вопрос")]
    ], resize_keyboard=True)

    return res


def tests_kb() -> ReplyKeyboardMarkup:
    res = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton("Тест Бека"), KeyboardButton("Agile-компас (от Neurointegration Institute)")],
        [KeyboardButton("Тест на Орбиты ( от Neurointegration Institute)")],
        [KeyboardButton("Назад")]
    ], resize_keyboard=True)

    return res
