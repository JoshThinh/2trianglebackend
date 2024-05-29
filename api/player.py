from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

from model.players import Player

# Change variable name and API name and prefix
player_api = Blueprint('player_api', __name__,
                   url_prefix='/api/players')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(player_api)

class PlayerAPI:     
    class _CRUD(Resource):
        
        
        def post(self):
            body = request.get_json()
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'less than 2 characters'}, 210
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'less than 2 characters'}, 210
            tokens = body.get('tokens')
            data = body.get('data')
            player = Player.query.get(uid) 
            if(player):
                player = player.updateToken(data)
                return jsonify(player.read())
            
            po = Player(name=name, 
                        uid=uid,
                        tokens=tokens)
                     
            player = po.create()
            print(jsonify(player.read()))
            if player:
                return jsonify(player.read())
            return {'message': f'Processed {name}, User ID {uid} is duplicate'}, 210
        def get(self):
            players = Player.query.order_by(Player._tokens.desc()).all()  
            json_ready = [player.read() for player in players] 
            return jsonify(json_ready)  
        
        
        
        def put(self):
            body = request.get_json() # get the body of the request
            uid = body.get('uid') # get the UID (Know what to reference)
            data = body.get('data')
            player = Player.query.get(uid) # get the player (using the uid in this case)
            if(player):
                player.update(data)
                return f"{player.read()} Updated"
            else:
                return {
                    "error": "Error fetching player",
                }, 404
          
        def delete(self):
            body = request.get_json()
            uid = body.get('uid')
            player = Player.query.get(uid)
            player.delete()
            return f"{player.read()} Has been deleted"


    # building RESTapi endpoint, method distinguishes action
    api.add_resource(_CRUD, '/')
