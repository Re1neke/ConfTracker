#/usr/bin/env python3

from pirc522 import RFID

BLKSIZE = 16

SECT_ST = 4
AID_BLOCK = 4
NAME_BLOCK = 5
SURNAME_BLOCK = 6

def strtoblk(string):
    blk = list(bytes(string.encode('ascii')))
    while len(blk) < BLKSIZE:
        blk += [0]
    return blk


def inttoblk(num):
    return (num).to_bytes(BLKSIZE, 'little') 


class CardHandler(RFID):

    def __del__(self):
        self.cleanup()

    def _interact_card(self):
        self.wait_for_tag()
        error, tag_type = self.request()
        if error:
            return False
        error, uid = self.anticoll()
        if error:
            return False
        if self.select_tag(uid):
            return False
        if not self.card_auth(self.auth_a, SECT_ST, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], uid):
            return True

    def read_card(self):
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

    def write_card(self, aid, sname, fname):
        if not self._interact_card():
            return False
        if self.write(AID_BLOCK, inttoblk(aid)):
            return False
        if self.write(NAME_BLOCK, strtoblk(sname)):
            return False
        if self.write(SURNAME_BLOCK, strtoblk(fname)):
            return False
        return True
