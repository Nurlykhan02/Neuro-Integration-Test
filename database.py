import logging
import sqlite3


# Connect to db
def post_sql_query(sql_query: str, data: tuple = None):
    with sqlite3.connect('bot.db') as connection:
        cursor = connection.cursor()
        try:
            if data:
                cursor.execute(sql_query, data)
            else:
                cursor.execute(sql_query)
        except Exception as e:
            logging.warning(e)

        result = cursor.fetchall()

        return result


def users_table():
    sql = """CREATE TABLE IF NOT EXISTS users(
        id                  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        user_id             INTEGER UNIQUE,
        first_name          TEXT,
        last_name           TEXT,
        username            TEXT,
        reg_date            DATETIME DEFAULT CURRENT_DATE
    )"""
    post_sql_query(sql)


def questions_table():
    sql = """CREATE TABLE IF NOT EXISTS questions(
        id                  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        question            TEXT,
        test_number         INTEGER
    )"""
    post_sql_query(sql)


def answers_table():
    sql = """CREATE TABLE IF NOT EXISTS answers(
        id                  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        answer              TEXT,
        question_id         INTEGER
    )"""
    post_sql_query(sql)


def results_table():
    sql = """CREATE TABLE IF NOT EXISTS results(
        id                  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        user                INTEGER,
        full_name           TEXT,
        points              INTEGER,
        pass_date           DATETIME DEFAULT CURRENT_DATE
    )"""
    post_sql_query(sql)


def registrate_user(user_id, first, last, user):
    sql = "SELECT id FROM users WHERE user_id = ?"
    data = (user_id,)

    if not post_sql_query(sql, data):
        sql = "INSERT INTO users(user_id, first_name, last_name, username) VALUES (?, ?, ?, ?)"
        data = (user_id, first, last, user)

        post_sql_query(sql, data)


def _test_id(s: str):
    data = {
        "Тест Бека": 1,
        "Agile-компас (от Neurointegration Institute)": 2,
        "Тест на Орбиты ( от Neurointegration Institute)": 3,
    }
    return data.get(s)


def get_question(q_id: int = 1, test_id: str = "Тест Бека") -> list:
    sql = "SELECT * FROM questions WHERE test_number = ? AND id = ?"
    test_id = _test_id(test_id)
    data = (test_id, q_id)

    res = post_sql_query(sql, data)

    return res[0] if res else None


def get_answers_by_question(question: int) -> list:
    sql = "SELECT id, answer FROM answers WHERE question_id = ? ORDER BY id"
    data = (question, )

    return post_sql_query(sql, data)


def save_results(u_id: int, user: str, points: int):
    sql = "INSERT INTO results(user, full_name, points) VALUES (?, ?, ?)"
    data = (u_id, user, points)

    post_sql_query(sql, data)
