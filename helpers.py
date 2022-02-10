from curses.ascii import isupper
import os
import requests
import urllib.parse
import random
import string

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def validatePass(password):
    if len(password) < 8:
        return False

    conditionCheck = False
    special_characters = """'"!@  # $%^&*()-+?_=,<>/"""

    # checking for special character in password
    for character in password:
        if character in special_characters:
            conditionCheck = True

    if conditionCheck == False:
        return False

    # avoiding a condition which can lead towards browser error
    if "<?>" in password:
        return False

    conditionCheck = False

    # checking for upper case letter in password
    for character in password:
        if character.isupper() == True:
            conditionCheck = True

    if conditionCheck == False:
        return False

    conditionCheck = False
    # checking for lower case letter in password
    for character in password:
        if character.islower() == True:
            conditionCheck = True

    if conditionCheck == False:
        return False

    # checking for digit in password
    for character in password:
        if character.isdigit() == True:
            conditionCheck = True

    if conditionCheck == False:
        return False

    return True


def generatePass():

    # printing lowercase
    lowerCase = ''.join(random.choice(string.ascii_lowercase)
                        for i in range(random.randint(3, 8)))

    # printing uppercase
    upperCase = ''.join(random.choice(string.ascii_uppercase)
                        for i in range(random.randint(3, 8)))

    # printing letters
    asciiLetters = ''.join(random.choice(string.ascii_letters)
                           for i in range(random.randint(3, 8)))

    # printing digits
    digits = ''.join(random.choice(string.digits)
                     for i in range(random.randint(3, 8)))

    # printing punctuation
    punctuation = ''.join(random.choice(string.punctuation)
                          for i in range(random.randint(3, 8)))

    password = upperCase + asciiLetters + lowerCase + digits + punctuation

    l = list(password)
    random.shuffle(l)
    password = ''.join(l)

    return password
