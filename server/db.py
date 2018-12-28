import sqlite3

def format_query_args(**kwargs):
    s = ""
    first = True
    for key, arg in kwargs.items():
        if first:
            first = False
            s += "{} = '{}'".format(key, arg)
        else:
            s += ", {} = '{}'".format(key, arg)
    return s


class DBConnect:

    def __init__(self, db_name):
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        self.db_connect = sqlite3.connect(db_name)
        self.db_connect.row_factory = dict_factory
        self.create_tables()

    def __del__(self):
        self.db_connect.close()

    def create_tables(self, reset=False):
        tables = {}
        tables["attendees"] = '''CREATE TABLE IF NOT EXISTS attendees(
                                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                                     name TEXT,
                                     surname TEXT NOT NULL,
                                     organization TEXT,
                                     degree TEXT,
                                     is_activated INTEGER NOT NULL DEFAULT 0,
                                     card_written INTEGER NOT NULL DEFAULT 0
                                 );'''
        tables["sections"] = '''CREATE TABLE IF NOT EXISTS sections(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT NOT NULL,
                                    building TEXT NOT NULL,
                                    room TEXT NOT NULL
                                );'''
        tables["registrations"] = '''CREATE TABLE IF NOT EXISTS registrations(
                                         attendee_id INTEGER NOT NULL,
                                         section_id INTEGER NOT NULL,
                                         status INTEGER NOT NULL DEFAULT 1,
                                         FOREIGN KEY (attendee_id) REFERENCES attendees(id),
                                         FOREIGN KEY (section_id) REFERENCES sections(id),
                                         PRIMARY KEY (attendee_id, section_id)
                                     );'''
        tables["nfc_module"] = '''CREATE TABLE IF NOT EXISTS nfc_module(
                                      is_busy INTEGER NOT NULL DEFAULT 0
                                  );'''
        drop_query = "DROP TABLE IF EXISTS {}"
        for table_name, create_query in tables.items():
            if reset:
                self.db_connect.execute(drop_query.format(table_name))
            self.db_connect.execute(create_query)
        self.db_connect.commit()

    def add_attendee(self,
                     name,
                     surname,
                     organization,
                     degree,
                     is_activated=False,
                     commit=True):
        query =  '''INSERT INTO attendees(name,
                                          surname,
                                          organization,
                                          degree,
                                          is_activated)
                    VALUES (?, ?, ?, ?, ?)'''
        cursor = self.db_connect.execute(query,
                                         (name,
                                          surname,
                                          organization,
                                          degree,
                                          is_activated))
        if commit:
            self.db_connect.commit()
        return cursor.lastrowid

    def get_attendees(self):
        query = '''SELECT * FROM attendees'''
        cursor = self.db_connect.execute(query)
        return cursor.fetchall()

    def get_attendee(self, id):
        query = '''SELECT * FROM attendees WHERE id = ?'''
        cursor = self.db_connect.execute(query, (id,))
        return cursor.fetchone()

    def edit_attendee(self, id, commit=True, **kwargs):
        if "is_activated" in kwargs:
            kwargs["is_activated"] = int(kwargs["is_activated"])
        query = '''UPDATE attendees
                   SET {}
                   WHERE id = ?'''.format(format_query_args(**kwargs))
        cursor = self.db_connect.execute(query, (id,))
        if commit:
            self.db_connect.commit()
        return bool(cursor.rowcount)

    def add_section(self, name, building, room, commit=True):
        query = '''INSERT INTO sections(name, building, room)
                   VALUES (?, ?, ?)'''
        cursor = self.db_connect.execute(query, (name, building, room))
        if commit:
            self.db_connect.commit()
        return cursor.lastrowid

    def get_sections(self):
        query = '''SELECT * FROM sections'''
        cursor = self.db_connect.execute(query)
        return cursor.fetchall()

    def get_section(self, id):
        query = '''SELECT * FROM sections WHERE id = ?'''
        cursor = self.db_connect.execute(query, (id,))
        return cursor.fetchone()

    def edit_section(self, id, commit=True, **kwargs):
        query = '''UPDATE sections
                   SET {}
                   WHERE id = ?'''.format(format_query_args(**kwargs))
        cursor = self.db_connect.execute(query, (id,))
        if commit:
            self.db_connect.commit()
        return bool(cursor.rowcount)

    def get_aregs(self, aid, all=False):
        query = '''SELECT sections.*, registrations.status
                   FROM sections, registrations
                   WHERE sections.id = registrations.section_id
                   AND registrations.attendee_id = ?'''
        if not all:
            query += ' AND registrations.status != 0'
        cursor = self.db_connect.execute(query, (aid,))
        return cursor.fetchall()

    def get_sregs(self, sid, all=False):
        query = '''SELECT attendees.*, registrations.status
                   FROM attendees, registrations
                   WHERE attendees.id = registrations.attendee_id
                   AND registrations.section_id = ?'''
        if not all:
            query += ' AND registrations.status != 0'
        cursor = self.db_connect.execute(query, (sid,))
        return cursor.fetchall()

    def get_reg(self, aid, sid):
        query = '''SELECT *
                   FROM registrations
                   WHERE attendee_id = ?
                   AND section_id = ?'''
        cursor = self.db_connect.execute(query, (aid, sid))
        return cursor.fetchone()

    def add_reg(self, aid, sid, status=1, commit=True):
        query = '''INSERT INTO registrations(attendee_id, section_id, status)
                   VALUES (?, ?, ?)'''
        cursor = self.db_connect.execute(query, (aid, sid, status))
        if commit:
            self.db_connect.commit()
        return cursor.lastrowid

    def set_reg_status(self, aid, sid, status, commit=True):
        query = '''UPDATE registrations
                   SET status = ?
                   WHERE attendee_id = ? AND section_id = ?'''
        cursor = self.db_connect.execute(query, (status, aid, sid))
        if commit:
            self.db_connect.commit()
        return bool(cursor.rowcount)

    def get_nfc_status(self):
        query = "SELECT is_busy FROM nfc_module"
        cursor = self.db_connect.execute(query)
        return bool(cursor.fetchone()["is_busy"])

    def set_nfc_status(self, is_busy, commit=True):
        query1 = "UPDATE nfc_module SET is_busy = ?"
        query2 = "INSERT INTO nfc_module(is_busy) VALUES (?)"
        cursor = self.db_connect.execute(query1, (int(is_busy),))
        if not cursor.rowcount:
            cursor = self.db_connect.execute(query2, (int(is_busy),))
        if commit:
            self.db_connect.commit()
        return bool(cursor.rowcount)

    def commit(self):
        self.db_connect.commit()

    def rollback(self):
        self.db_connect.commit()
