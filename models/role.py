from flask import Blueprint, request, json, jsonify, make_response
from database import db
from server_utils.utils import Serializer
from server_utils.HTTP_status_returns import __OK__, __NOT_FOUND__
from flask.views import MethodView

role_blueprint = Blueprint("role_blueprint", __name__)

class Role(db.Model, Serializer):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name=""):
        self.name = name

    def __repr__(self):
        return {"Role": self.name}

    def __unicode__(self):
        return self.name

    def serialize(self):
        return Serializer.serialize(self)

class RoleAPI(MethodView):
    def get(self, id):
        if id is None:
            roles = Role.query.all()
            message = {"results": (Role.serialize_list(roles))}
            return make_response(jsonify(message), 200)
        role = Role.query.filter(Role.id==id).first()
        return make_response(json.dumps(role.serialize()), 200)

    def post(self):
        role = Role(request.form["name"])
        db.session.add(role)
        db.session.commit()
        return __OK__()

    def delete(self, id):
        db.session.delete(Role.query.get(id))
        db.session.commit()
        return __OK__()

    def put(self, id):
        role = Role.query.get(id)
        role.name = request.form["name"]
        db.session.commit()
        return __OK__()


role_view = RoleAPI.as_view('role_api')
role_blueprint.add_url_rule('/roles/', defaults={'id': None},
                 view_func=role_view, methods=['GET',])
role_blueprint.add_url_rule('/roles/', view_func=role_view, methods=['POST',])
role_blueprint.add_url_rule('/roles/<int:id>', view_func=role_view,
                 methods=['GET', 'PUT', 'DELETE'])