__author__ = 'shweta'

from flask import Blueprint, request, json, make_response, jsonify
from database import db
from server_utils.utils import Serializer
from server_utils.HTTP_status_returns import __OK__, __NOT_FOUND__
from flask.views import MethodView

survey_ans_blueprint = Blueprint("survey_ans_blueprint", __name__)

class SurveyAnswer(db.Model, Serializer):
    __tablename__ = 'surveyans'

    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(), nullable=False)
    question = db.relationship('SurveyQuestionnaire')
    questionId = db.Column(db.Integer, db.ForeignKey('surveyqs.id'), nullable=False)
    photoReq = db.Column(db.Boolean)
    vidReq = db.Column(db.Boolean)

    def __init__(self, answer="", questionId="", photoReq="", vidReq=""):
        self.answer = answer
        self.questionId = questionId
        self.photoReq = photoReq
        self.vidReq = vidReq

    def __repr__(self):
        return {"Survey Answer": self.answer}

    def __unicode__(self):
        return self.answer

    def serialize(self):
        return Serializer.serialize(self)

class SurveyAnswerAPI(MethodView):
    def get(self, id):
        if id is None:
            answers = SurveyAnswer.query.all()
            message = {"results": (SurveyAnswer.serialize_list(answers))}
            return make_response(jsonify(message), 200)
        answer = SurveyAnswer.query.filter(SurveyAnswer.id==id).first()
        return make_response(json.dumps(answer.serialize()), 200)

    def post(self):
        ans = SurveyAnswer(
                    request.form['answer'],
                    request.form['questionId'],
                    request.form['photoReq'],
                    request.form['vidReq'],
                )
        db.session.add(ans)
        db.session.commit()
        return __OK__()

    def delete(self, id):
        db.session.delete(SurveyAnswer.query.get(id))
        db.session.commit()
        return __OK__()

    def put(self, id):
        ans = SurveyAnswer.query.get(id)
        ans.answer = request.form['answer']
        ans.questionId = request.form['questionId']
        ans.photoReq = request.form['photoReq']
        ans.vidReq = request.form['vidReq']
        db.session.commit()
        return __OK__()


survey_ans_view = SurveyAnswerAPI.as_view('survey_ans_api')
survey_ans_blueprint.add_url_rule('/survey/ans/', defaults={'id': None},
                 view_func=survey_ans_view, methods=['GET',])
survey_ans_blueprint.add_url_rule('/survey/ans/', view_func=survey_ans_view, methods=['POST',])
survey_ans_blueprint.add_url_rule('/survey/ans/<int:id>', view_func=survey_ans_view,
                 methods=['GET', 'PUT', 'DELETE'])