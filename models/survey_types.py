__author__ = 'shweta'

from flask import Blueprint, request, json, make_response, jsonify
from database import db
from server_utils.utils import Serializer
from server_utils.HTTP_status_returns import __OK__, __NOT_FOUND__
from flask.views import MethodView

survey_type_blueprint = Blueprint("survey_type_blueprint", __name__)

class SurveyType(db.Model, Serializer):
    __tablename__ = 'surveytypes'

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


class SurveyTypeAPI(MethodView):
    #TODO: Error handling for all queries (if not found)
    def get(self, id):
        if id is None:
            surveyTypes = SurveyType.query.all()
            message = {"results": (SurveyType.serialize_list(surveyTypes))}
            return make_response(jsonify(message), 200)
        surveyType = SurveyType.query.filter(SurveyType.id==id).first()
        return make_response(json.dumps(surveyType.serialize()), 200)

    def post(self):
        surveyType = SurveyType(request.form['name'])
        db.session.add(surveyType)
        db.session.commit()
        return __OK__()

    def delete(self, id):
        db.session.delete(SurveyType.query.get(id))
        db.session.commit()
        return __OK__()

    def put(self, id):
        surveyType = SurveyType.query.get(id)
        surveyType.name = request.form['name']
        db.session.commit()
        return __OK__()


survey_type_view = SurveyTypeAPI.as_view('survey_type_api')
survey_type_blueprint.add_url_rule('/survey/types/', defaults={'id': None},
                 view_func=survey_type_view, methods=['GET',])
survey_type_blueprint.add_url_rule('/survey/types/', view_func=survey_type_view, methods=['POST',])
survey_type_blueprint.add_url_rule('/survey/types/<int:id>', view_func=survey_type_view,
                 methods=['GET', 'PUT', 'DELETE'])