import sqlite3

def create_table():
    dbase = sqlite3.connect('Data/DataBase.db', check_same_thread=False)
    db = dbase.cursor()
    db.execute(''' CREATE TABLE IF NOT EXISTS auser_language_target(
        ID INT PRIMARY KEY NOT NULL,
        USERNAME TEXT,
        FIRSTNAME TEXT NOT NULL,
        LASTNAME TEXT, 
        TARGET TEXT NOT NULL) ''')
    dbase.commit()
    dbase.close()

def insert(chat_id, username, firstname, lastname, target):
    dbase = sqlite3.connect('Data/DataBase.db', check_same_thread=False)
    db = dbase.cursor()
    if get_data(chat_id) is None:
        db.execute('''INSERT INTO auser_language_target(ID,USERNAME, FIRSTNAME, LASTNAME, TARGET)
               VALUES(?,?,?,?,?)''', (chat_id, username, firstname, lastname, target))
        print('inserted')
    else:
        db.execute('''UPDATE auser_language_target set TARGET= ?  WHERE ID=?''', (target, chat_id))
        print('updated')

    dbase.commit()
    dbase.close()

def get_data(chat_id):
    dbase = sqlite3.connect('Data/DataBase.db', check_same_thread=False)
    db = dbase.cursor()
    db.execute('''SELECT TARGET FROM auser_language_target WHERE ID= ?''', (chat_id,))
    target = db.fetchone()
    dbase.close()
    if target is not None:
        return target[0]
    else:
        return None
