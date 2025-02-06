import sqlite3


class ManagementEvent:
    def __init__(self, db_name):
        self.db_name =  db_name
        self.connect = sqlite3.connect(self.db_name)
        self.cursor = self.connect.cursor()
        self.cursor.execute("""
            GREATE TABLE IF NOT EXISTS Events(
            id INTEGER PRIMARY KEY,
            event TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
            )
        """)
        self.connect.commit()

    def add_event(self, id_user, event,date, time):
        self.cursor.execute("INSERT INTO Events (id, event, date, time) VALUES (?,?,?,?)", (int(id_user), event, date, time))
        self.connect.commit()

    def show_event(self, id_user):
        self.cursor.execute("SELECT * FROM Events WHERE id = ?", (id_user,))
        self.cursor.fetchall()


db = ManagementEvent('telegram_event.db')
