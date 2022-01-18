import sqlite3

conn = sqlite3.connect(':memory:')  #:memory: чтобы сохранить БД в RAM
sql = conn.cursor()

# Создание таблиц

sql.execute("""CREATE TABLE IF NOT EXISTS words
                  (id integer PRIMARY KEY, word text NOT NULL)
                  WITHOUT ROWID;
               """)

sql.execute("""CREATE TABLE IF NOT EXISTS synonyms
                  (word_id integer, synonym text NOT NULL)
               """)

# тестовые данные
words = [('1', 'car'), ('2', 'phone'), ('3', 'animal')]
synonyms = [('1', 'machine'), ('1', 'automobile'),
            ('2', 'cellphone'), ('2', 'mobile phone'),
            ('3', 'creature'), ('3', 'living thing')]
# заполняем таблицы данными
sql.executemany("INSERT INTO words VALUES(?,?)", words)
sql.executemany("INSERT INTO synonyms VALUES(?,?)", synonyms)

# подтверждаем изменения
conn.commit()

import tkinter as tk

# Создать главное окно
root = tk.Tk()


# функция для кноки Найти синонимы
def find_synonyms():
    s = ent.get()
    sql.execute("""SELECT synonym FROM synonyms WHERE word_id =
     (SELECT id FROM words WHERE word = ?)
    """, (s,))
    r = sql.fetchall()
    if len(r) == 0:
        sql.execute("""SELECT word FROM words WHERE id =
             (SELECT word_id FROM synonyms WHERE synonym = ?)
            """, (s,))
        r = sql.fetchall()
        sql.execute("""SELECT synonym FROM synonyms WHERE word_id =
                     (SELECT word_id FROM synonyms WHERE synonym = ?) 
                     AND synonym != ?
                    """, (s, s))
        r += sql.fetchall()

    res = ' '.join(map((lambda x: x[0]), r))
    res = res if len(res) > 0 else "Синонимов не найдено"
    lab['text'] = res


# функция для кноки  Добавить слово
def add_word():
    s = ent.get()
    sql.execute("""SELECT COUNT(*) FROM words WHERE word = ?""", (s,))
    count = sql.fetchone()[0]
    if (count > 0):
        lab['text'] = "Такое слово уже есть в БД"
    else:
        sql.execute("""SELECT COUNT(*) FROM words""")
        count = sql.fetchone()[0]
        sql.execute("INSERT INTO words VALUES(?,?)", (count + 1, s))
        lab['text'] = "Успешно"


# функция для кноки Добавить синоним
def add_synonym():
    s = ent.get()
    s = s.split('->')
    word = s[0]

    sql.execute("""SELECT COUNT(*) FROM words WHERE word = ?""", (word,))
    count = sql.fetchone()[0]

    if (count == 0):
        sql.execute("""SELECT COUNT(*) FROM words""")
        count = sql.fetchone()
        sql.execute("INSERT INTO words VALUES(?,?)", (count[0] + 1, word))
    else:
        sql.execute("""SELECT id FROM words WHERE word = ?""", (word,))
        id = sql.fetchone()[0]
        synonym = s[1]
        sql.execute("INSERT INTO synonyms VALUES(?,?)", (id, synonym))
        lab['text'] = "Успешно"


# Создать компоненты на форме
ent = tk.Entry(width=50)
but = tk.Button(text="Найти синонимы", command=find_synonyms)
but2 = tk.Button(text="Добавить слово", command=add_word)
but3 = tk.Button(text="Добавить синоним", command=add_synonym)
lab = tk.Label(width=50, bg='black', fg='white')

# Разместить компоненты на форме
ent.pack()
but.pack()
but2.pack()
but3.pack()
lab.pack()
root.mainloop()
