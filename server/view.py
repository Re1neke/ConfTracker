# -*- coding: utf-8 -*-
"""This module describes functions for generating and returning html pages of
the web interface of system.
"""

from bottle import get, abort, template, redirect, static_file
from db import DBConnect

dbc = DBConnect("conference_data.db")


@get(r"/<file:re:.*\.(css|js)>")
def static_files(file):
    """Gets statis files as css and js."""
    return static_file(file, "static")


@get(r"/<file:re:.*\.svg>")
def images(file):
    """Gets images"""
    return static_file(file, "images")


@get("/")
def main_index():
    """Redirection from root"""
    redirect("/attendees")


@get("/attendees")
def attendee_index():
    """Table with all attendees"""
    write_modal_tpl = template("templates/write_modal.tpl")
    body_tpl = template("templates/attendee_table.tpl",
                        write_modal=write_modal_tpl)
    return template("templates/index.tpl",
                    title="Attendees",
                    body=body_tpl,
                    show_searchbox=False)


# TODO: add page with attendee's info
@get("/attendees/<aid>")
def attendee_info_index(aid):
    """Page with detailed info of attendee."""
    pass


@get("/attendees/<aid>/edit")
def edit_attendee_index(aid):
    """Page for editing attendee's info."""
    sections = dbc.get_sections()
    write_modal_tpl = template("templates/write_modal.tpl")
    body_tpl = template("templates/attendee_form.tpl",
                        write_modal=write_modal_tpl,
                        sections=sorted(sections, key=lambda k: k["name"]),
                        id=aid)
    return template("templates/index.tpl",
                    title="Edit attendee",
                    body=body_tpl,
                    show_searchbox=False)


@get("/attendees/add")
def add_attendee_index():
    """Page for creation of new attendee."""
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
    """Page with list of all sections."""
    body_tpl = template("templates/section_table.tpl")
    return template("templates/index.tpl",
                    title="Sections",
                    body=body_tpl,
                    show_searchbox=False)


@get("/sections/<sid>")
def sections_regs_index(sid):
    """Page with list of attendees witch is registered to the section."""
    section = dbc.get_section(sid)
    if not section:
        abort(404)
    body_tpl = template("templates/regs_table.tpl", section=section)
    return template("templates/index.tpl",
                    title="Sections",
                    body=body_tpl,
                    show_searchbox=False)


@get("/sections/add")
def add_section_index():
    """Page for creation of new section."""
    body_tpl = template("templates/section_form.tpl", id=None)
    return template("templates/index.tpl",
                    title="Add section",
                    body=body_tpl,
                    show_searchbox=False)


@get("/sections/<sid>/edit")
def edit_section_index(sid):
    """Page for edit section data."""
    body_tpl = template("templates/section_form.tpl", id=sid)
    return template("templates/index.tpl",
                    title="Edit section",
                    body=body_tpl,
                    show_searchbox=False)
