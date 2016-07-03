from flask import Blueprint, request, json, jsonify, make_response
from database import db
from server_utils.utils import Serializer
from server_utils.HTTP_status_returns import __OK__, __NOT_FOUND__
from flask.views import MethodView
from datetime import datetime

user_blueprint = Blueprint("user_blueprint", __name__)

class User(db.Model, Serializer):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String())
    password = db.Column(db.String(), nullable=False)
    telNo1 = db.Column(db.String())
    telNo2 = db.Column(db.String())
    address = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String())
    faxNo = db.Column(db.String())
    status = db.Column(db.String())
    role = db.relationship('Role')
    roleId = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    organization = db.relationship('Organization')
    orgId = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    createDate = db.Column(db.String())

    def __init__(self, name="", username="", email="", password="", telNo1="", telNo2="", address="", city="", state="", faxNo="", status="", roleId="", orgId=""):
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.telNo1 = telNo1
        self.telNo2 = telNo2
        self.address = address
        self.city = city
        self.state = state
        self.faxNo = faxNo
        self.status = status
        self.roleId = roleId
        self.orgId = orgId
        self.createDate = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __repr__(self):
        return {"User Name": self.name}

    def __unicode__(self):
        return self.name

    def serialize(self):
        return Serializer.serialize(self)


class UserAPI(MethodView):
    def get(self, id):
        if id is None:
            users = User.query.all()
            message = {"results": (User.serialize_list(users))}
            return make_response(jsonify(message), 200)
        user = User.query.filter(User.id==id).first()
        return make_response(json.dumps(user.serialize()), 200)

    def post(self):
        #TODO: return user id after post
        user = User(
                    request.form['name'],
                    request.form['username'],
                    request.form['email'],
                    request.form['password'],
                    request.form['telNo1'],
                    request.form['telNo2'],
                    request.form['address'],
                    request.form['city'],
                    request.form['state'],
                    request.form['faxNo'],
                    request.form['status'],
                    request.form['roleId'],
                    request.form['orgId']
                )
        db.session.add(user)
        db.session.commit()
        return __OK__()

    def delete(self, id):
        db.session.delete(User.query.get(id))
        db.session.commit()
        return __OK__()

    def put(self, id):
        user = User.query.get(id)
        user.name = request.form['name']
        user.username = request.form['username']
        user.email = request.form['email']
        user.password = request.form['password']
        user.telNo1 = request.form['telNo1']
        user.telNo2 = request.form['telNo2']
        user.address = request.form['address']
        user.city = request.form['city']
        user.state = request.form['state']
        user.status = request.form['status']
        user.roleId = request.form['roleId']
        user.orgId = request.form['orgId']
        db.session.commit()
        return __OK__()

user_view = UserAPI.as_view('user_api')
user_blueprint.add_url_rule('/users/', defaults={'id': None},
                 view_func=user_view, methods=['GET',])
user_blueprint.add_url_rule('/users/', view_func=user_view, methods=['POST',])
user_blueprint.add_url_rule('/users/<int:id>', view_func=user_view,
                 methods=['GET', 'DELETE', 'PUT'])