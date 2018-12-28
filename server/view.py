from bottle import get, abort, template, redirect, static_file
from db import DBConnect

dbc = DBConnect("conference_data.db")


@get("/<file:re:.*\.(css|js)>")
def static_files(file):
    return static_file(file, "static")


@get("/<file:re:.*\.svg>")
def static_files(file):
    return static_file(file, "images")


@get("/")
def main_index():
    redirect("/attendees")


@get("/attendees")
def attendee_index():
    write_modal_tpl = template("templates/write_modal.tpl")
    body_tpl = template("templates/attendee_table.tpl",
                        write_modal=write_modal_tpl)
    return template("templates/index.tpl",
                    title="Attendees",
                    body=body_tpl,
                    show_searchbox=False)


@get("/attendees/<id>")
def attendee_info_index(id):
    pass


@get("/attendees/<id>/edit")
def edit_attendee_index(id):
    sections = dbc.get_sections()
    write_modal_tpl = template("templates/write_modal.tpl")
    body_tpl = template("templates/attendee_form.tpl",
                        write_modal=write_modal_tpl,
                        sections=sorted(sections, key=lambda k: k["name"]),
                        id=id)
    return template("templates/index.tpl",
                    title="Edit attendee",
                    body=body_tpl,
                    show_searchbox=False)


@get("/attendees/add")
def add_attendee_index():
    sections = dbc.get_sections()
    write_modal_tpl = template("templates/write_modal.tpl")
    body_tpl = template("templates/attendee_form.tpl",
                        write_modal=write_modal_tpl,
                        sections=sorted(sections, key=lambda k: k["name"]),
                        id=None)
    return template("templates/index.tpl",
                    title="Add attendee",
                    body=body_tpl,
                    show_searchbox=False)


@get("/sections")
def sections_index():
    body_tpl = template("templates/section_table.tpl")
    return template("templates/index.tpl",
                    title="Sections",
                    body=body_tpl,
                    show_searchbox=False)


@get("/sections/<id>")
def sections_regs_index(id):
    section = dbc.get_section(id)
    if not section:
        abort(404)
    body_tpl = template("templates/regs_table.tpl", section=section)
    return template("templates/index.tpl",
                    title="Sections",
                    body=body_tpl,
                    show_searchbox=False)


@get("/sections/add")
def add_section_index():
    body_tpl = template("templates/section_form.tpl", id=None)
    return template("templates/index.tpl",
                    title="Add section",
                    body=body_tpl,
                    show_searchbox=False)


@get("/sections/<id>/edit")
def edit_section_index(id):
    body_tpl = template("templates/section_form.tpl", id=id)
    return template("templates/index.tpl",
                    title="Edit section",
                    body=body_tpl,
                    show_searchbox=False)
