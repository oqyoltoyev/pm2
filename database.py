import sqlite3

conn = sqlite3.connect('database.db',
                       check_same_thread=False,
                       isolation_level=None)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,chat_id INTIGER UNIQUE)")

cursor.execute("CREATE TABLE IF NOT EXISTS serial(id INTEGER PRIMARY KEY,name TEXT,file_id TEXT)")

cursor.execute("CREATE TABLE IF NOT EXISTS movies(id INTEGER PRIMARY KEY,file_id TEXT,caption TEXT,serial TEXT)")

cursor.execute("CREATE TABLE IF NOT EXISTS kino(id INTEGER PRIMARY KEY,file_id TEXT,caption TEXT)")

cursor.execute('''CREATE TABLE IF NOT EXISTS announcements (
    id INTEGER PRIMARY KEY,
    photo_url TEXT,
    text TEXT,
    button_name TEXT,
    button_url TEXT,
    date_added TEXT,
    views INTEGER DEFAULT 0,
    loves INTEGER DEFAULT 0,
    fires INTEGER DEFAULT 0,
    lightnings INTEGER DEFAULT 0,
    flowers INTEGER DEFAULT 0
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS user_reactions (
    user_id INTEGER,
    announcement_id INTEGER,
    reaction TEXT,
    PRIMARY KEY (user_id, announcement_id)
)''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL
        )
    ''')

conn.commit()



def get_channels():
    cursor.execute('SELECT * FROM channels')
    return cursor.fetchall()

def add_channel(name, url):
    try:
        cursor.execute('INSERT INTO channels (name, url) VALUES (?, ?)', (name, url))
        conn.commit()  # O'zgarishlarni saqlash
    except sqlite3.IntegrityError as e:
        print(f"Xato: {e}")
        raise ValueError("Kanalni qo'shishda xato yuz berdi.")
    
def delete_channel(channel_id):

    cursor.execute('DELETE FROM channels WHERE id = ?', (channel_id,))
    conn.commit()
    
    
