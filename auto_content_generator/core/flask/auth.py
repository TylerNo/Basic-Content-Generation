from flask import session, request
from auto_content_generator.core.main.main_utilities import load_config


def authenticate(request):
    print("Authenticate function called.")
    if request.method == 'POST':
        password_field = request.form['Password-Field-02']
        config = load_config()
        correct_password = config["auth"]["password"]
        print(correct_password)
        if password_field == correct_password:
            session['logged_in'] = True
            return True
    return False

def check_authentication():
    return 'logged_in' in session
