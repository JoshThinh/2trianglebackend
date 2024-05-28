from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

from model.foods import Food

# Change variable name and API name and prefix
food_api = Blueprint('food_api', __name__,
                   url_prefix='/api/foods')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(food_api)

class FoodAPI:     
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
            food = Food.query.get(uid) 
            if(food):
                food = food.updateToken(data)
                return jsonify(food.read())
            
            po = Food(name=name, 
                        uid=uid,
                        tokens=tokens)
                     
            food = po.create()
            print(jsonify(food.read()))
            if food:
                return jsonify(food.read())
            return {'message': f'Processed {name}, User ID {uid} is duplicate'}, 210
        def get(self):
            foods = Food.query.order_by(Food._tokens.desc()).all()  
            json_ready = [food.read() for food in foods] 
            return jsonify(json_ready)  
        
        
        
        def put(self):
            body = request.get_json() # get the body of the request
            uid = body.get('uid') # get the UID (Know what to reference)
            data = body.get('data')
            food = Food.query.get(uid) # get the food (using the uid in this case)
            if(food):
                food.update(data)
                return f"{food.read()} Updated"
            else:
                return {
                    "error": "Error fetching food",
                }, 404
          
        def delete(self):
            body = request.get_json()
            uid = body.get('uid')
            food = Food.query.get(uid)
            food.delete()
            return f"{food.read()} Has been deleted"


    # building RESTapi endpoint, method distinguishes action
    api.add_resource(_CRUD, '/')
