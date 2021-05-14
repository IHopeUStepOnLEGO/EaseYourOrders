from flask import render_template


def return_template(__template__):

    return str(render_template(__template__))