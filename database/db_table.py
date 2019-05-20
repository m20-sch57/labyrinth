class DBTable:
    def __init__(self, db):
        self.db = db
        self.connect, self.cursor = self.db.connect, self.db.cursor

    def execute(self, *args):
        cursor = self.cursor()
        cursor.execute(*args)
        self.connect.commit()
        return cursor
