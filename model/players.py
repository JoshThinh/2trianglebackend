""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

class Player(db.Model):
    __tablename__ = 'players'  # table name is plural, class name is singular

    # Define the Player schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=False, nullable=False)
    _tokens = db.Column(db.Integer)    

    # constructor of a Player object, initializes the instance variables within object (self)
    def __init__(self, name, uid, tokens):
        self._name = name    # variables with self prefix become part of the object, 
        self._uid = uid
        self._tokens = tokens

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts email from object
    @property
    def uid(self):
        return self._uid
    
    # a setter function, allows name to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid
    
    
    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def tokens(self):
        return self._tokens
    
    # dob should be have verification for type date
    @tokens.setter
    def tokens(self, tokens):
        self._tokens = tokens
    
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a player object from Player(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "name": self.name,
            "uid": self.uid,
            "tokens": self.tokens
        }

    def update(self, dictionary):
        for key in dictionary:
            if key == "name":
                self.name = dictionary[key]
            if key == "uid":
                self.uid = dictionary[key]
            if key == "tokens":
                self.tokens = dictionary[key]
        db.session.commit()
        return self


    def updateToken(self, dictionary):
        namefound = False;
        uidfound = False;
        
        for key in dictionary:
            if key == "name":
                if self.name == dictionary[key]:
                    namefound = True;
            if key == "uid":
                self.uid = dictionary[key]
            if key == "tokens":
                self.tokens = dictionary[key]
        db.session.commit()
        return self
    
    # CRUD delete: remove self
    # return self
    def delete(self):
        player = self
        db.session.delete(self)
        db.session.commit()
        return player


"""Database Creation and Testing """


# Builds working data for testing
def initPlayers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester records for table"""
        players = [
            Player(name='Josh Williams', uid='joshW', tokens=1),
            Player(name='John Mortensen', uid='johnM', tokens=1)
        ]

        """Builds sample user/note(s) data"""
        for player in players:
            try:
                player.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {player.uid}")