from flask import jsonify, session, render_template, request, redirect, url_for
from threading import Thread
from auto_content_generator.core.main.main_utilities import start_generator, load_config, save_config, update_code_from_git
from auto_content_generator.core.flask.auth import check_authentication, authenticate
from auto_content_generator.core.flask.log_manager import LogManager

log_manager = LogManager()

def initialize_routes(app, config):
    @app.route('/logs', methods=['GET'])
    def get_logs():
        if check_authentication():
            return jsonify({"logs": log_manager.app_logs}), 200
        else:
            return jsonify({"message": "Unauthorized"}), 401


    @app.route('/start', methods=['POST'])
    def start():
        if check_authentication():
            log_manager.MAX_LOG_ENTRIES = config["main"]["max_log_entries"]
            log_manager.set_stop_signal(False)
            t = Thread(target=start_generator, args=(log_manager,))
            t.start()
            return jsonify({"message": "Started"}), 200
        else:
            return jsonify({"message": "Unauthorized"}), 401

    @app.route('/stop', methods=['POST'])
    def stop():
        if check_authentication():
            log_manager.set_stop_signal(True)
            log_message = "Stopping after current process..."
            log_manager.append_log(log_message)
            return jsonify({"message": "Stopping"}), 200
        else:
            return jsonify({"message": "Unauthorized"}), 401

    @app.route('/settings')
    def settings():
        if check_authentication():
            return render_template('settings.html')
        else:
            return redirect(url_for('index'))

    @app.route('/', methods=['GET', 'POST'])
    def index():
        print("Index function called.")
        if request.method == 'POST':
            if authenticate(request):
                return redirect(url_for('main_page'))
        return render_template('index.html')

    @app.route('/main_page')
    def main_page():
        if check_authentication():
            return render_template('main.html')
        else:
            return redirect(url_for('index'))

    @app.route('/get_config', methods=['GET'])
    def get_config():
        if check_authentication():

            return jsonify({"config": config}), 200
        else:
            return jsonify({"message": "Unauthorized"}), 401

    @app.route('/save_config', methods=['POST'])
    def save_config_endpoint():
        if check_authentication():
            new_config = request.json.get('config')
            save_config(new_config)
            return jsonify({"message": "Saved successfully"}), 200
        else:
            return jsonify({"message": "Unauthorized"}), 401

    @app.route('/update_code', methods=['POST'])
    def update_code():
        if check_authentication():
            if update_code_from_git():
                return jsonify({"message": "Code updated successfully"}), 200
            else:
                return jsonify({"message": "Code update failed"}), 500
        else:
            return jsonify({"message": "Unauthorized"}), 401
