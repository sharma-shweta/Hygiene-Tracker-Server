__author__ = 'shweta'

from flask import Blueprint, request, json, make_response, jsonify
from database import db
from server_utils.utils import Serializer
from server_utils.HTTP_status_returns import __OK__, __NOT_FOUND__
from flask.views import MethodView

housetype_blueprint = Blueprint("housetype_blueprint", __name__)

class HouseType(db.Model, Serializer):
    __tablename__ = 'housetypes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name=""):
        self.name = name

    def __repr__(self):
        return {"House Type": self.name}

    def __unicode__(self):
        return self.name

    def serialize(self):
        return Serializer.serialize(self)


class HouseTypeAPI(MethodView):
    #TODO: Error handling for all queries (if not found)
    def get(self, id):
        if id is None:
            houseTypes = HouseType.query.all()
            message = {"results": (HouseType.serialize_list(houseTypes))}
            return make_response(jsonify(message), 200)
        houseType = HouseType.query.filter(HouseType.id==id).first()
        return make_response(json.dumps(houseType.serialize()), 200)


    def post(self):
        houseType = HouseType(request.form['name'])
        db.session.add(houseType)
        db.session.commit()
        return __OK__()

    def delete(self, id):
        db.session.delete(HouseType.query.get(id))
        db.session.commit()
        return __OK__()

    def put(self, id):
        houseType = HouseType.query.get(id)
        houseType.name = request.form['name']
        db.session.commit()
        return __OK__()


housetype_view = HouseTypeAPI.as_view('housetype_api')
housetype_blueprint.add_url_rule('/housetypes/', defaults={'id': None},
                 view_func=housetype_view, methods=['GET',])
housetype_blueprint.add_url_rule('/housetypes/', view_func=housetype_view, methods=['POST',])
housetype_blueprint.add_url_rule('/housetypes/<int:id>', view_func=housetype_view,
                 methods=['GET', 'PUT', 'DELETE'])