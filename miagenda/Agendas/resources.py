from flask import render_template, request
from core.utils import debug

# Base

def index():
    print(request.path)
    return render_template('index.html')


def guide():
    return render_template('guide.html')


def about():
    return render_template('about.html')

def credits():
    return render_template('credits.html')

# Accounts

def login():
    return render_template('accounts/login.html')


def signup():
    return render_template('accounts/signup.html')