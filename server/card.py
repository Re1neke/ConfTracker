# -*- coding: utf-8 -*-
"""This modude contains class for interacting with RFID tag reader and some
helper functions for it.
"""

from pirc522 import RFID

BLKSIZE = 16        # Size of one block in bytes

# Default key for getting access to card section
DEF_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

SECT_ST = 4         # Number of first block of the used section
AID_BLOCK = 4       # Number of block where attendee's id is stored
NAME_BLOCK = 5      # And block for attendee's name
SURNAME_BLOCK = 6   # And one for surname


def strtoblk(string):
    """Converts string to bytearray of block size lenth
    and zeroes rest of block.

    Args:
        string (str): string that will be converted.

    Returns:
        list: list with raw byte values.

    """
    blk = list(bytes(string.encode('ascii')))
    while len(blk) < BLKSIZE:
        blk += [0]
    return blk


def inttoblk(num):
    """Converts number to bytearray block.

    Args:
        num (int): number to convert.

    Returns:
        bytes: bytearray with little-endian int value.

    """
    return (num).to_bytes(BLKSIZE, 'little')


class CardHandler(RFID):
    """Class for writing and reading attendee's data with RFID tags.
    """

    def __del__(self):
        self.cleanup()

    def _interact_card(self):
        """Prepares card for interacting.

        Returns:
            bool: True if card reary for interaction. False otherwise.

        """
        self.wait_for_tag()
        error, _ = self.request()
        if error:
            return False
        error, uid = self.anticoll()
        if error:
            return False
        if self.select_tag(uid):
            return False
        if self.card_auth(self.auth_a, SECT_ST, DEF_KEY, uid):
            return False
        return True

    def read_card(self):
        """Reads data from card and returs tuple of attendee's id, name and
        surname.

        Returns:
            tuple: tuple with id, name and surname of attendee or None if some
                error occurs.

        """
        if not self._interact_card():
            return None
        error, aid_list = self.read(AID_BLOCK)
        if error:
            return None
        error, sname_list = self.read(NAME_BLOCK)
        if error:
            return None
        error, fname_list = self.read(SURNAME_BLOCK)
        if error:
            return None
        aid = int.from_bytes(bytes(aid_list), 'little')
        sname = bytes(sname_list).decode('ascii').rstrip('\0')
        fname = bytes(fname_list).decode('ascii').rstrip('\0')
        self.stop_crypto()
        return aid, sname, fname

    def write_card(self, aid, name, sname):
        """Writes attendee's data to card.

        Args:
            aid (int): id of attendee.
            name (str): attendee's name.
            sname (str): attendee's surname.

        Returns:
            bool: returns True if data is written successfuly, False otherwise.

        """
        if not self._interact_card():
            return False
        if self.write(AID_BLOCK, inttoblk(aid)):
            return False
        if self.write(NAME_BLOCK, strtoblk(name)):
            return False
        if self.write(SURNAME_BLOCK, strtoblk(sname)):
            return False
        return True
