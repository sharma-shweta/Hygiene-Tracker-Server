__author__ = 'shweta'

from flask import Blueprint, request, jsonify, make_response, json
from database import db
from server_utils.utils import Serializer
from server_utils.HTTP_status_returns import __OK__, __NOT_FOUND__
from flask.views import MethodView

occupation_blueprint = Blueprint("occupation_blueprint", __name__)

class Occupation(db.Model, Serializer):
    __tablename__ = 'occupations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name=""):
        self.name = name

    def __repr__(self):
        return {"Occupation": self.name}
        #return "{"Occupation": %s}" % self.name

    def __unicode__(self):
        return self.name

    def serialize(self):
        return Serializer.serialize(self)


class OccupationAPI(MethodView):
    def get(self, id):
        if id is None:
            occupations = Occupation.query.all()
            message = {"results": (Occupation.serialize_list(occupations))}
            return make_response(jsonify(message), 200)
        occupation = Occupation.query.filter(Occupation.id==id).first()
        return make_response(json.dumps(occupation.serialize()), 200)
        #return '{\'results\': %s }' % json.dumps(occupation.serialize())

    def post(self):
        occupation = Occupation(request.form['name'])
        db.session.add(occupation)
        db.session.commit()
        return __OK__()

    def delete(self, id):
        db.session.delete(Occupation.query.get(id))
        db.session.commit()
        return __OK__()

    def put(self, id):
        occupation = Occupation.query.get(id)
        occupation.name = request.form['name']
        db.session.commit()
        return __OK__()


occupation_view = OccupationAPI.as_view('occupation_api')
occupation_blueprint.add_url_rule('/occupations/', defaults={'id': None},
                 view_func=occupation_view, methods=['GET',])
occupation_blueprint.add_url_rule('/occupations/', view_func=occupation_view, methods=['POST',])
occupation_blueprint.add_url_rule('/occupations/<int:id>', view_func=occupation_view,
                 methods=['GET', 'PUT', 'DELETE'])