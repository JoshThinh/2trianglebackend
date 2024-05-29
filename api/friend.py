from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

from model.friends import Friend

# Change variable name and API name and prefix
friend_api = Blueprint('friend_api', __name__,
                   url_prefix='/api/friends')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(friend_api)

class FriendAPI:     
    class _CRUD(Resource):
        def post(self):
            body = request.get_json()
            uidfriend = body.get('uidfriend')
            if uidfriend is None or len(uidfriend) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 210
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 210
            friend = Friend.query.filter_by(_uid=uid, _uidfriend=uidfriend).first()
            if friend:
                return {'message': f'Processed {uid}, User ID {uidfriend} is duplicate'}, 210
            else:
                po = Friend(uidfriend=uidfriend, uid=uid)   
                friend = po.create()
                print(jsonify(friend.read()))
                if friend:
                    return jsonify(friend.read())
                return {'message': f'Processed {uid}, User ID {uidfriend} is duplicate'}, 210
          
        def get(self,uid):
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 210
            friends = Friend.query.filter_by(_uid=uid).all()   
            json_ready = [friend.read() for friend in friends]  
            return jsonify(json_ready) 
    api.add_resource(_CRUD, '/','/<string:uid>')
