__author__ = 'shweta'

from flask import Blueprint, request, json, make_response, jsonify
from database import db
from server_utils.utils import Serializer
from server_utils.HTTP_status_returns import __OK__, __NOT_FOUND__
from flask.views import MethodView

client_class_type_blueprint = Blueprint("client_class_type_blueprint", __name__)

class ClientClassType(db.Model, Serializer):
    __tablename__ = 'clientclasstypes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name=""):
        self.name = name

    def __repr__(self):
        return {"Client Class": self.name}

    def __unicode__(self):
        return self.name

    def serialize(self):
        return Serializer.serialize(self)


class ClientClassTypeAPI(MethodView):
    def get(self, id):
        if id is None:
            classTypes = ClientClassType.query.all()
            message = {"results": (ClientClassType.serialize_list(classTypes))}
            return make_response(jsonify(message), 200)
        classType = ClientClassType.query.filter(ClientClassType.id==id).first()
        return make_response(json.dumps(classType.serialize()), 200)

    def post(self):
        classType = ClientClassType(request.form['name'])
        db.session.add(classType)
        db.session.commit()
        return __OK__()

    def delete(self, id):
        db.session.delete(ClientClassType.query.get(id))
        db.session.commit()
        return __OK__()

    def put(self, id):
        classType = ClientClassType.query.get(id)
        classType.name = request.form['name']
        db.session.commit()
        return __OK__()


client_class_type_view = ClientClassTypeAPI.as_view('client_class_type_api')
client_class_type_blueprint.add_url_rule('/class/types/', defaults={'id': None},
                 view_func=client_class_type_view, methods=['GET',])
client_class_type_blueprint.add_url_rule('/class/types/', view_func=client_class_type_view, methods=['POST',])
client_class_type_blueprint.add_url_rule('/class/types/<int:id>', view_func=client_class_type_view,
                 methods=['GET', 'PUT', 'DELETE'])