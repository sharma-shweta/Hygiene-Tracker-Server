__author__ = 'shweta'

from flask import Blueprint, request, json, make_response, jsonify
from database import db
from server_utils.utils import Serializer
from server_utils.HTTP_status_returns import __OK__, __NOT_FOUND__
from flask.views import MethodView

surveyq_blueprint = Blueprint("surveyq_blueprint", __name__)

class SurveyQuestionnaire(db.Model, Serializer):
    __tablename__ = 'surveyqs'

    id = db.Column(db.Integer, primary_key=True)
    surveyQuestion = db.Column(db.String())
    category = db.relationship('SurveyQCategory')
    categoryId = db.Column(db.Integer, db.ForeignKey('surveyq_categories.id'), nullable=False)

    def __init__(self, surveyQuestion="", categoryId=""):
        self.surveyQuestion = surveyQuestion
        self.categoryId = categoryId

    def __repr__(self):
        return {"Survey Question": self.surveyQuestion}

    def __unicode__(self):
        return self.surveyQuestion

    def serialize(self):
        return Serializer.serialize(self)

class SurveyQuestionnaireAPI(MethodView):
    def get(self, id):
        if id is None:
            questions = SurveyQuestionnaire.query.all()
            message = {"results": (SurveyQuestionnaire.serialize_list(questions))}
            return make_response(jsonify(message), 200)
        question = SurveyQuestionnaire.query.filter(SurveyQuestionnaire.id==id).first()
        return make_response(json.dumps(question.serialize()), 200)

    def post(self):
        question = SurveyQuestionnaire(
                    request.form['surveyQuestion'],
                    request.form['categoryId'],
                )
        db.session.add(question)
        db.session.commit()
        return __OK__()

    def delete(self, id):
        db.session.delete(SurveyQuestionnaire.query.get(id))
        db.session.commit()
        return __OK__()

    def put(self, id):
        question = SurveyQuestionnaire.query.get(id)
        question.surveyQuestion = request.form['surveyQuestion']
        question.categoryId = request.form['categoryId']
        db.session.commit()
        return __OK__()


survey_q_view = SurveyQuestionnaireAPI.as_view('survey_q_api')
surveyq_blueprint.add_url_rule('/survey/q/', defaults={'id': None},
                 view_func=survey_q_view, methods=['GET',])
surveyq_blueprint.add_url_rule('/survey/q/', view_func=survey_q_view, methods=['POST',])
surveyq_blueprint.add_url_rule('/survey/q/<int:id>', view_func=survey_q_view,
                 methods=['GET', 'PUT', 'DELETE'])