# -*- coding: utf-8 -*-
"""Module with class that gives an interface for handling attendee's data and
store it to the database.
"""

import sqlite3

UNREGISTERED = 0
REGISTERED = 1
IS_PRESENT = 2
IS_GONE = 3


def format_query_args(**kwargs):
    """Formats kwargs to string for SQL query.

    Args:
        **kwargs: arguments that will be formatted.

    Returns:
        str: string with formatted dict values.

    """
    query_str = ""
    first = True
    for key, arg in kwargs.items():
        if first:
            first = False
            query_str += "{} = '{}'".format(key, arg)
        else:
            query_str += ", {} = '{}'".format(key, arg)
    return query_str


class DBConnect:
    """Class for interacting with attendee's data in the database.

    This class presents an interface for database, that helps to store
    conference data in easy way. Creates all needed tables at initialization.

    Args:
        db_name (str): path to database file. If DB is not exists - it will be
            created.

    Attribures:
        db_connect (class 'sqlite3.Connection'): db connection object for
            interact with it.

    """

    def __init__(self, db_name):
        def dict_factory(cursor, row):
            retd = {}
            for idx, col in enumerate(cursor.description):
                retd[col[0]] = row[idx]
            return retd
        self.db_connect = sqlite3.connect(db_name)
        self.db_connect.row_factory = dict_factory
        self.create_tables()

    def __del__(self):
        self.db_connect.close()

    def create_tables(self, reset=False):
        """Creates needed tables in the used database.

        Args:
            reset (bool): If set to True existed tables will be droped before
                creation. Defaults to False.

        """
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

# pylint: disable=too-many-arguments
    def add_attendee(self,
                     name,
                     surname,
                     organization,
                     degree,
                     is_activated=False,
                     commit=True):
        """Adds new attendee to the database.

        Args:
            name (str): first name of attendee.
            surname (str): surname of attendee.
            organization (str): organization that attendee represents.
            degree (str): academic degree of the attendee.
            is_activated (bool): flag for attendee's entry activation.
                Defaults to False.
            commit (bool): commit database update automatically.
                Defaults to True.

        Returns:
            int: id of attendee.

        """
        query = '''INSERT INTO attendees(name,
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
        """Gets list of all existed attendees.

        Returns:
            list: return list of dicts with attendees data.

        """
        query = '''SELECT * FROM attendees'''
        cursor = self.db_connect.execute(query)
        return cursor.fetchall()

    def get_attendee(self, aid):
        """Finds in the database attendee with specified id.

        Args:
            aid (int): attendee's id.

        Returns:
            dict: dictionary with attendee's data or None if section with
                specified is does not exist.

        """
        query = '''SELECT * FROM attendees WHERE id = ?'''
        cursor = self.db_connect.execute(query, (aid,))
        return cursor.fetchone()

    def edit_attendee(self, aid, commit=True, **kwargs):
        """Edits attendee entry in the database.

        Args:
            aid (int): attendee's id.
            commit (bool): commit database update automatically.
                Defaults to True.
            **kwargs: parameters to edit.

        Returns:
            bool: True if entry edited successfuly. False otherwise.

        """
        if "is_activated" in kwargs:
            kwargs["is_activated"] = int(kwargs["is_activated"])
        query = '''UPDATE attendees
                   SET {}
                   WHERE id = ?'''.format(format_query_args(**kwargs))
        cursor = self.db_connect.execute(query, (aid,))
        if commit:
            self.db_connect.commit()
        return bool(cursor.rowcount)

    def add_section(self, name, building, room, commit=True):
        """Adds new section to the database.

        Args:
            name (str): name of section.
            building (str): buildings number of name where section is located.
            room (str): room number or name where section is located.
            commit (bool): commit changes to database automatically.
                Defaults to True.

        Returns:
            int: id of new section.

        """
        query = '''INSERT INTO sections(name, building, room)
                   VALUES (?, ?, ?)'''
        cursor = self.db_connect.execute(query, (name, building, room))
        if commit:
            self.db_connect.commit()
        return cursor.lastrowid

    def get_sections(self):
        """Gets list of all existed sections.

        Returns:
            list: return list of dicts with sections data.

        """
        query = '''SELECT * FROM sections'''
        cursor = self.db_connect.execute(query)
        return cursor.fetchall()

    def get_section(self, sid):
        """Finds in the database section with specified id.

        Args:
            sid (int): section id.

        Returns:
            dict: dictionary with section data or None if section with
                specified is does not exist.

        """
        query = '''SELECT * FROM sections WHERE id = ?'''
        cursor = self.db_connect.execute(query, (sid,))
        return cursor.fetchone()

    def edit_section(self, sid, commit=True, **kwargs):
        """Edits sections parameters in the database.

        Args:
            sid (int): id of the section.
            commit (bool): commit changes to the databe automatically.
                Defaults to True.
            **kwargs: section's parameters to edit.

        Returns:
            bool: True if section edited successfuly. False otherwise.

        """
        query = '''UPDATE sections
                   SET {}
                   WHERE id = ?'''.format(format_query_args(**kwargs))
        cursor = self.db_connect.execute(query, (sid,))
        if commit:
            self.db_connect.commit()
        return bool(cursor.rowcount)

    def get_aregs(self, aid, get_all=False):
        """Finds registrations of the attendee.

        Args:
            aid (int): attendee's id.
            get_all (bool): add hidden registration to list. Defaults to False.

        Returns:
            list: list of dicts with registrations of attendee.

        """
        query = '''SELECT sections.*, registrations.status
                   FROM sections, registrations
                   WHERE sections.id = registrations.section_id
                   AND registrations.attendee_id = ?'''
        if not get_all:
            query += ' AND registrations.status != 0'
        cursor = self.db_connect.execute(query, (aid,))
        return cursor.fetchall()

    def get_sregs(self, sid, get_all=False):
        """Finds all attendees registered to section.

        Args:
            sid (int): section's id.
            get_all (bool): add hidden registration to list. Defaults to False.

        Returns:
            list: list of dicts with registrations to the section.

        """
        query = '''SELECT attendees.*, registrations.status
                   FROM attendees, registrations
                   WHERE attendees.id = registrations.attendee_id
                   AND registrations.section_id = ?'''
        if not get_all:
            query += ' AND registrations.status != 0'
        cursor = self.db_connect.execute(query, (sid,))
        return cursor.fetchall()

    def get_reg(self, aid, sid):
        """Gets info about attendee's registration to section.

        Args:
            aid (int): attendee's id.
            sid (int): section's id.

        Returns:
            dict: dict with registration information if attendee is registered
                to this section. None otherwise.
        """
        query = '''SELECT *
                   FROM registrations
                   WHERE attendee_id = ?
                   AND section_id = ?'''
        cursor = self.db_connect.execute(query, (aid, sid))
        return cursor.fetchone()

    def add_reg(self, aid, sid, status=REGISTERED, commit=True):
        """Adds new registration to the database.

        Args:
            aid (int): attendee's id.
            sid (int): section's id.
            status (int): status of registration (see constants at top of
                module).
            commit (bool): commits database changes automatically.
                Defaults to True.

        Returns:
            int: id of new registration entry.

        """
        query = '''INSERT INTO registrations(attendee_id, section_id, status)
                   VALUES (?, ?, ?)'''
        cursor = self.db_connect.execute(query, (aid, sid, status))
        if commit:
            self.db_connect.commit()
        return cursor.lastrowid

    def set_reg_status(self, aid, sid, status, commit=True):
        """Changes status of registration.

         Args:
            aid (int): attendee's id.
            sid (int): section's id.
            status (int): status of registration (see constants at top of
                module).
            commit (bool): commits database changes automatically.
                Defaults to True.

        Returns:
            bool: True if data changed sucessfule. False otherwise.

        """
        query = '''UPDATE registrations
                   SET status = ?
                   WHERE attendee_id = ? AND section_id = ?'''
        cursor = self.db_connect.execute(query, (status, aid, sid))
        if commit:
            self.db_connect.commit()
        return bool(cursor.rowcount)

# This not work correctly now. But will be fixed later.
#   def get_nfc_status(self):
#       query = "SELECT is_busy FROM nfc_module"
#       cursor = self.db_connect.execute(query)
#       return bool(cursor.fetchone()["is_busy"])
#
#    def set_nfc_status(self, is_busy, commit=True):
#       query1 = "UPDATE nfc_module SET is_busy = ?"
#       query2 = "INSERT INTO nfc_module(is_busy) VALUES (?)"
#       cursor = self.db_connect.execute(query1, (int(is_busy),))
#       if not cursor.rowcount:
#           cursor = self.db_connect.execute(query2, (int(is_busy),))
#       if commit:
#           self.db_connect.commit()
#       return bool(cursor.rowcount)

    def commit(self):
        """Commits changes to database manualy."""
        self.db_connect.commit()

    def rollback(self):
        """Undo chages to database."""
        self.db_connect.rollback()
