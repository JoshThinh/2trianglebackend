import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required

from model.classes import Classes

classes_api = Blueprint('classes_api', __name__,
                   url_prefix='/api/classes')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(classes_api)

class ClassesAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        # @token_required
        # def post(self, current_user): # Create method
        #     ''' Read data for json body '''
        #     body = request.get_json()
            
        #     ''' Avoid garbage in, error checking '''
        #     # validate name
        #     classname = body.get('classname')
        #     if classname is None or len(classname) < 2:
        #         return {'message': f'Name is missing, or is less than 2 characters'}, 400
        #     # validate uid
        #     uid = body.get('uid')
        #     if uid is None or len(uid) < 2:
        #         return {'message': f'User ID is missing, or is less than 2 characters'}, 400
        #     # look for password and dob
        #     password = body.get('password')
        #     dob = body.get('dob')

        #     ''' #1: Key code block, setup USER OBJECT '''
        #     co = CharClass(classname=classname)
        
            
        #     ''' Additional garbage error checking '''
        #     # set password if provided
        #     if password is not None:
        #         co.set_password(password)
        #     # convert to date type
        #     if dob is not None:
        #         try:
        #             co.dob = datetime.strptime(dob, '%Y-%m-%d').date()
        #         except:
        #             return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 400
            
        #     ''' #2: Key Code block to add user to database '''
        #     # create user in database
        #     CharClass = co.create()
        #     # success returns json of user
        #     if CharClass:
        #         return jsonify(CharClass.read())
        #     # failure returns error
        #     return {'message': f'Processed {classname}, either a format error or User ID {uid} is duplicate'}, 400

        # @token_required
        def get(self): # Read Method
            CharClasses = Classes.query.all()
            json_ready = [CharClass.read() for CharClass in CharClasses]
            return jsonify(json_ready)
    
    # class _Security(Resource):
    #     def post(self):
    #         try:
    #             body = request.get_json()
    #             if not body:
    #                 return {
    #                     "message": "Please provide user details",
    #                     "data": None,
    #                     "error": "Bad request"
    #                 }, 400
    #             ''' Get Data '''
    #             uid = body.get('uid')
    #             if uid is None:
    #                 return {'message': f'User ID is missing'}, 400
    #             password = body.get('password')
                
    #             ''' Find user '''
    #             user = User.query.filter_by(_uid=uid).first()
    #             if user is None or not user.is_password(password):
    #                 return {'message': f"Invalid user id or password"}, 400
    #             if user:
    #                 try:
    #                     token = jwt.encode(
    #                         {"_uid": user._uid},
    #                         current_app.config["SECRET_KEY"],
    #                         algorithm="HS256"
    #                     )
    #                     resp = Response("Authentication for %s successful" % (user._uid))
    #                     resp.set_cookie("jwt", token,
    #                             max_age=3600,
    #                             secure=True,
    #                             httponly=True,
    #                             path='/',
    #                             samesite='None'  # This is the key part for cross-site requests

    #                             # domain="frontend.com"
    #                             )
    #                     return resp
    #                 except Exception as e:
    #                     return {
    #                         "error": "Something went wrong",
    #                         "message": str(e)
    #                     }, 500
    #             return {
    #                 "message": "Error fetching auth token!",
    #                 "data": None,
    #                 "error": "Unauthorized"
    #             }, 404
    #         except Exception as e:
    #             return {
    #                     "message": "Something went wrong!",
    #                     "error": str(e),
    #                     "data": None
    #             }, 500

            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    # api.add_resource(_Security, '/authenticate')
    