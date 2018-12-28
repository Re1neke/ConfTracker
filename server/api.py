from signal import signal, alarm, SIGALRM
from time import sleep
from json import dumps
from bottle import get, post, put, abort, request, response
from db import DBConnect
from card import CardHandler

CARD_TIMEOUT = 10

dbc = DBConnect("conference_data.db")


@get("/api/attendees")
def get_attendees():
    attendees = dbc.get_attendees()
    return dumps(attendees)


@get("/api/attendees/<id>")
def get_attendee(id):
    attendee = dbc.get_attendee(id)
    return dumps(attendee)


@post("/api/attendees")
def add_attendee():
    response.set_header("Content-Type", "application/json")
    if "name" not in request.json or "surname" not in request.json:
        response.status = 400
        return dumps(dict(error="Required parameters are missing"))
    if len(request.json["name"]) == 0 or len(request.json["surname"]) == 0:
        response.status = 400
        return dumps(dict(error="Required parameters can't be empty"))
    aid = dbc.add_attendee(request.json["name"],
                              request.json["surname"],
                              request.json["organization"] if "organization" in request.json else "",
                              request.json["degree"] if "degree" in request.json else "",
                              request.json["is_activated"] if "is_activated" in request.json else False,
                              commit=False)
    if aid is None:
        response.status = 500
        return dumps(dict(error="Error during attendee creation"))
    if "sections" in request.json:
        for sid in request.json["sections"]:
            rid = dbc.add_reg(aid, sid, commit=False)
            if rid is None:
                dbc.rollback()
                response.status = 500
                return dumps(dict(error="Error during registration to sections"))
    dbc.commit()
    return dumps(dict(id=aid, uri="/attendees/{}/edit".format(aid))) # TODO: change uri


@put("/api/attendees/<id>")
def edit_attendee(id):
    response.set_header("Content-Type", "application/json")
    if len(request.json["name"]) == 0 or len(request.json["surname"]) == 0:
        response.status = 400
        return dumps(dict(error="Required parameters can't be empty"))
    attendee = dict()
    for key, value in request.json.items():
        if key in ["name", "surname", "organization", "degree", "is_activated"]:
            attendee[key] = value
    old_attendee = dbc.get_attendee(id)
    if (("name" in attendee or "surname" in attendee)
        and (attendee["name"] != old_attendee["name"] 
             or attendee["surname"] != old_attendee["surname"])):
        attendee["card_written"] = 0
    if not dbc.edit_attendee(id, commit=False, **attendee):
        response.status = 500
        return dumps(dict(error="Error during attendee editing"))
    if "sections" in request.json:
        sections = dbc.get_aregs(id, all=True)
        request_sections = list(map(int, request.json["sections"]))
        for section in sections:
            if (section["id"] in request_sections
                and section["status"] == 0):
                dbc.set_reg_status(id, section["id"], 1, commit=False)
            elif section["id"] not in request_sections:
                dbc.set_reg_status(id, section["id"], 0, commit=False)
        sections_id = [section["id"] for section in sections]
        for section in request_sections:
            if section not in sections_id:
                dbc.add_reg(id, section, commit=False)
    dbc.commit()
    return dumps(dict(id=id, uri="/attendees/{}/edit".format(id))) # TODO: change uri


@post("/api/attendees/<id>/card")
def write_attendee_card(id):
    def handler(signum, frame):
        raise TimeoutError()
    response.set_header("Content-Type", "application/json")
    #if dbc.get_nfc_status():
    #    response.status = 500
    #    return dumps(dict(id=id, status="ERROR: NFC module is busy"))
    # dbc.set_nfc_status(False)
    attendee = dbc.get_attendee(id)
    ch = CardHandler()
    old = signal(SIGALRM, handler)
    alarm(CARD_TIMEOUT)
    timeout = False
    write_status = False
    try:
        write_status = ch.write_card(attendee["id"], attendee["name"], attendee["surname"])
    except TimeoutError:
        timeout = True
    finally:
        ch.cleanup()
        alarm(0)
        signal(SIGALRM, old)
        # dbc.set_nfc_status(False)
    if write_status:
        dbc.edit_attendee(id, card_written=1)
        return dumps(dict(id=id, status="Card successfuly written"))
    elif timeout:
        response.status = 500
        return dumps(dict(id=id, status="ERROR: NFC module timeout"))
    else:
        response.status = 500
        return dumps(dict(id=id, status="Some problems occured. Try again."))


@get("/api/attendees/<id>/sections")
def get_attendee_regs(id):
    sections = dbc.get_aregs(id)
    response.set_header("Content-Type", "application/json")
    return dumps(sections)


@get("/api/sections")
def get_sections():
    sections = dbc.get_sections()
    return dumps(sections)


@get("/api/sections/<id>")
def get_section(id):
    section = dbc.get_section(id)
    return dumps(section)


@post("/api/sections")
def add_section():
    response.set_header("Content-Type", "application/json")
    if "name" not in request.json or "building" not in request.json or "room" not in request.json:
        response.status = 400
        return dumps(dict(error="Required parameters are missing"))
    if len(request.json["name"]) == 0 or len(request.json["building"]) == 0 or len(request.json["room"]) == 0:
        response.status = 400
        return dumps(dict(error="Required parameters can't be empty"))
    id = dbc.add_section(request.json["name"],
                         request.json["building"],
                         request.json["room"])
    if id is not None:
        return dumps(dict(id=id, uri="/sections/{}".format(id)))
    else:
        response.status = 500
        return dumps(dict(error="Error during section creation"))


@put("/api/sections/<id>")
def edit_section(id):
    response.set_header("Content-Type", "application/json")
    if len(request.json["name"]) == 0 or len(request.json["building"]) == 0 or len(request.json["room"]) == 0:
        response.status = 400
        return dumps(dict(error="Required parameters can't be empty"))
    section = dict()
    for key, value in request.json.items():
        if key in ["name", "building", "room"]:
            section[key] = value
    if dbc.edit_section(id, **section):
        return dumps(dict(id=id, uri="/sections/{}".format(id)))
    else:
        response.status = 500
        return dumps(dict(error="Error during section editing"))


@get("/api/sections/<id>/attendees")
def get_section_regs(id):
    attendees = dbc.get_sregs(id)
    response.set_header("Content-Type", "application/json")
    return dumps(attendees)


@put("/api/sections/<sid>/track")
def track_attendee(sid):
    reg = dbc.get_reg(request.json["attendee"]["id"], sid)
    if reg is None or reg["status"] == 0:
        response.status = 400
        return dumps(dict(error="No such registration"))
    regs = dbc.get_aregs(request.json["attendee"]["id"])
    for areg in regs:
        if areg["status"] == 2 and areg["id"] != sid:
            dbc.set_reg_status(request.json["attendee"]["id"], areg["id"], 3, commit=False)
    if reg["status"] == 1:
        status = 2
    elif reg["status"] == 2:
        status = 3
    elif reg["status"] == 3:
        status = 2
    dbc.set_reg_status(request.json["attendee"]["id"], sid, status, commit=False)
    dbc.commit()
    response.set_header("Content-Type", "application/json")
    return dumps(dict(status=status))
