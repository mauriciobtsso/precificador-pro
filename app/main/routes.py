from flask import render_template, redirect, url_for
from flask_login import login_required
from . import main

@main.route("/")
@login_required
def dashboard():
    # Por enquanto, apenas uma página de boas-vindas
    return "<h1>Dashboard - Bem-vindo!</h1>"

@main.route("/login")
def login():
    # No futuro, aqui teremos o formulário de login
    return render_template("login.html")