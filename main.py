from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import database
import asyncio
import logging

from aiogram import types, Dispatcher, Bot

import keyboard

bot = Bot("", parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class CountOfAnswers(StatesGroup):
    STARTED = State()


@dp.message_handler(text="Назад", state="*")
@dp.message_handler(commands=['start'], state="*")
async def welcome_user(msg: types.Message, state: FSMContext):
    await state.finish()
    database.registrate_user(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name,
                             msg.from_user.username)

    await msg.answer(f"Привет {msg.from_user.full_name}\n\n"
                     f"Здесь вы можете пройти три теста для стартовой диагностики до сессии с тренером НИ.\n\n Пожалуйста, пройдите три теста, выбирая по очереди в меню 'Тесты'."  ,  reply_markup=keyboard.menu())
                    
                    


@dp.message_handler(text="Задать вопрос")
async def questions(msg: types.Message):
    await msg.answer("Пожалуйста перейдите по ссылке @bberikovichh, чтобы задать свой вопрос")


@dp.message_handler(text="Тесты")
async def tests(msg: types.Message):
    await msg.answer("Выберите нужный тест", reply_markup=keyboard.tests_kb())


@dp.message_handler(text="Тест Бека", state="*")
@dp.message_handler(text="Agile-компас (от Neurointegration Institute)", state="*")
@dp.message_handler(text="Тест на Орбиты ( от Neurointegration Institute)", state="*")
async def start_first_pool(msg: types.Message, state: FSMContext):
    
    await state.finish()

    question = database.get_question(test_id=msg.text)
    answers = database.get_answers_by_question(question[0])
    msg_text = str()

    for answer in answers:
        msg_text += f"{answer[0] % 5}. {answer[1]}\n"

    await msg.answer(f"{question[1]}\n\n{msg_text}",
                     reply_markup=keyboard.build_answers(question[0], answers))
    await CountOfAnswers.STARTED.set()
    await state.update_data(cnt=0, test_id=msg.text)


@dp.callback_query_handler(text_startswith="ans:", state=CountOfAnswers)
async def count_answers(c: types.CallbackQuery, state: FSMContext):
    _, question_id, answer_id = c.data.split(":")
    question_id = int(question_id)
    answer_id = int(answer_id)
    points = (await state.get_data()).get("cnt")
    test_id = (await state.get_data()).get("test_id")
    await state.update_data({"cnt": points + ((answer_id % 4) - 1) if answer_id % 4 else points + 3})

    question = database.get_question(q_id=question_id + 1, test_id=test_id)

    if question:
        answers = database.get_answers_by_question(question[0])
        msg_text = str()

        for answer in answers:
            msg_text += f"{answer[0] % 4 if answer[0] % 4 else 4}. {answer[1]}\n"

        await c.message.edit_text(f"{question[1]}\n\n{msg_text}",
                                  reply_markup=keyboard.build_answers(question[0], answers))
    else:
        points = (await state.get_data()).get("cnt")
        await c.message.edit_text(f"{c.from_user.full_name} вы набрали {points} баллов.")
        database.save_results(c.from_user.id, c.from_user.full_name, points)
        await state.finish()


async def main():
    logging.info("Bot started.")

    database.users_table()
    database.questions_table()
    database.answers_table()
    database.results_table()
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
