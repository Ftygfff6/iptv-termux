import sqlite3

class Database:
    def __init__(self, db_name="iptv_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS favorites (
                    stream_id TEXT PRIMARY KEY,
                    name TEXT,
                    stream_type TEXT,
                    stream_icon TEXT
                )
            """)

    def add_favorite(self, stream_id, name, stream_type, icon=""):
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO favorites VALUES (?, ?, ?, ?)",
                (str(stream_id), name, stream_type, icon)
            )

    def remove_favorite(self, stream_id):
        with self.conn:
            self.conn.execute("DELETE FROM favorites WHERE stream_id = ?", (str(stream_id),))

    def get_favorites(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT stream_id, name, stream_type, stream_icon FROM favorites")
        return cursor.fetchall()

