__author__ = 'shweta'

from flask import Blueprint, request, json, make_response, jsonify
from database import db
from server_utils.utils import Serializer
from server_utils.HTTP_status_returns import __OK__, __NOT_FOUND__
from flask.views import MethodView

surveyq_category_blueprint = Blueprint("surveyq_category_blueprint", __name__)

class SurveyQCategory(db.Model, Serializer):
    __tablename__ = 'surveyq_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)

    def __init__(self, name=""):
        self.name = name

    def __repr__(self):
        return {"Survey Question Category": self.name}

    def __unicode__(self):
        return self.name

    def serialize(self):
        return Serializer.serialize(self)

class SurveyQCategoryAPI(MethodView):
    def get(self, id):
        if id is None:
            categories = SurveyQCategory.query.all()
            message = {"results": (SurveyQCategory.serialize_list(categories))}
            return make_response(jsonify(message), 200)
        category = SurveyQCategory.query.filter(SurveyQCategory.id==id).first()
        return make_response(json.dumps(category.serialize()), 200)

    def post(self):
        category = SurveyQCategory(request.form['name'])
        db.session.add(category)
        db.session.commit()
        return __OK__()

    def delete(self, id):
        db.session.delete(SurveyQCategory.query.get(id))
        db.session.commit()
        return __OK__()

    def put(self, id):
        category = SurveyQCategory.query.get(id)
        category.name = request.form['name']
        db.session.commit()
        return __OK__()


surveyq_category_view = SurveyQCategoryAPI.as_view('survey_category_api')
surveyq_category_blueprint.add_url_rule('/survey/q/category/', defaults={'id': None},
                 view_func=surveyq_category_view, methods=['GET',])
surveyq_category_blueprint.add_url_rule('/survey/q/category/', view_func=surveyq_category_view, methods=['POST',])
surveyq_category_blueprint.add_url_rule('/survey/q/category/<int:id>', view_func=surveyq_category_view,
                 methods=['GET', 'PUT', 'DELETE'])