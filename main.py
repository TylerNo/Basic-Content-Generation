from flask import Flask
from auto_content_generator.core.flask.flask_routes import initialize_routes
from auto_content_generator.core.main.main_utilities import load_config


app = Flask(__name__)
app.secret_key = 'your_secret_key'

config = load_config()

initialize_routes(app, config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
