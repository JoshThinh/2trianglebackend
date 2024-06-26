import threading

# import "packages" from flask
from flask import render_template,request  # import render_template from "public" flask libraries
from flask.cli import AppGroup


# import "packages" from "this" project
from __init__ import app, db, cors  # Definitions initialization


# setup APIs
from api.user import user_api # Blueprint import api definition
from api.chat import chat_api
from api.player import player_api
from api.food import food_api
from api.friend import friend_api
from api.CharClass import classes_api
from api.CurrentChar import currentchar_api
# from api.tbftML import tbftmodel_api
# database migrations
from model.users import initUsers
from model.players import initPlayers
from model.foods import initFoods
from model.friends import initFriends
from model.classes import initCharClasses
from model.CurrentChars import initCurrentChars
# from model.tbftMLs import initTBFTModel

# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition


# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)

# register URIs
app.register_blueprint(user_api) # register api routes
app.register_blueprint(chat_api)
app.register_blueprint(player_api)
app.register_blueprint(food_api)
app.register_blueprint(friend_api)
app.register_blueprint(classes_api)
app.register_blueprint(currentchar_api)
# app.register_blueprint(tbftmodel_api)
app.register_blueprint(app_projects) # register app pages

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")


@app.route('/api/players', methods=['OPTIONS'])
def options():
    return '', 204

@app.route('/api/foods', methods=['OPTIONS'])
def options4():
    return '', 204

@app.route('/api/friends', methods=['OPTIONS'])
def options2():
    return '', 204

@app.route('/table/')  # connects /stub/ URL to stub() function
def table():
    return render_template("table.html")

@app.before_request
def before_request():
    # Check if the request came from a specific origin
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://localhost:4700', 'http://127.0.0.1:4700', "https://nighthawkcoders.github.io"]:
        cors._origins = allowed_origin

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')


# Define a command to generate data
@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initPlayers()
    initFoods()
    initFriends()
    initCharClasses()
    initCurrentChars()
    # initTBFTModel()

# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)
        
# this runs the application on the development server
if __name__ == "__main__":
    # change name for testing
    app.run(debug=True, host="0.0.0.0", port="8918")
