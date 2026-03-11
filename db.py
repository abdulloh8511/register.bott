import sqlite3

conn = sqlite3.Connection('register.db')
cur = conn.cursor()


def jadval_yaratish():
    komanda = """CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ism TEXT,
        familiya TEXT,
        yosh TEXT,
        telefon TEXT
        )"""
    cur.execute(komanda)
    conn.commit()
    
    
def add_user(ism, familiya, yosh, telefon):
    komanda = f"""
        INSERT INTO users(ism, familiya, yosh, telefon)
        VALUES ('{ism}', '{familiya}', '{yosh}', '{telefon}');
    """
    cur.execute(komanda)
    conn.commit()
