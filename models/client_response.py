__author__ = 'shweta'

from flask import Blueprint, request, json, make_response, jsonify
from database import db
from server_utils.utils import Serializer
from server_utils.HTTP_status_returns import __OK__, __NOT_FOUND__
from flask.views import MethodView
from datetime import datetime

client_response_blueprint = Blueprint("client_response_blueprint", __name__)

class ClientResponse(db.Model, Serializer):
    __tablename__ = 'clientresponses'

    id = db.Column(db.Integer, primary_key=True)
    client = db.relationship('ClientRegister')
    clientId = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    user = db.relationship('User')
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question = db.relationship('SurveyQuestionnaire')
    questionId = db.Column(db.Integer, db.ForeignKey('surveyqs.id'), nullable=False)
    answer = db.relationship('SurveyAnswer')
    answerId = db.Column(db.Integer, db.ForeignKey('surveyans.id'))
    answerDesc = db.Column(db.String())
    createDate = db.Column(db.String())

    def __init__(self, clientId="", userId="", questionId="", answerId="", answerDesc=""):
        self.clientId = clientId
        self.userId = userId
        self.questionId = questionId
        self.answerId = answerId
        self.answerDesc = answerDesc
        self.createDate = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __repr__(self):
        return {"Client Response": self.answerDesc}

    def __unicode__(self):
        return self.answerDesc

    def serialize(self):
        return Serializer.serialize(self)

class ClientResponseAPI(MethodView):
    #TODO: Empty returns
    def get(self, clientId, ansId):
        if ansId is None:
            ans = ClientResponse.query.all()
            message = {"results": (ClientResponse.serialize_list(ans))}
            return make_response(jsonify(message), 200)
        ans = ClientResponse.query.filter(ClientResponse.id==id).first()
        return make_response(json.dumps(ans.serialize()), 200)

    def post(self):
        ans = ClientResponse(
                    request.form['clientId'],
                    request.form['userId'],
                    request.form['questionId'],
                    request.form['answerId'],
                    request.form['answerDesc']
                )
        db.session.add(ans)
        db.session.commit()
        return __OK__()

    def delete(self, id):
        db.session.delete(ClientResponse.query.get(id))
        db.session.commit()
        return __OK__()

    def put(self, id):
        ans = ClientResponse.query.get(id)
        ans.clientId = request.form['clientId']
        ans.userId = request.form['userId']
        ans.questionId = request.form['questionId']
        ans.answerId = request.form['answerId']
        ans.answerDesc = request.form['answerDesc']
        db.session.commit()
        return __OK__()


client_response_view = ClientResponseAPI.as_view('client_response_api')
client_response_blueprint.add_url_rule('/clients/<int:clientId>/ans/<int:ansId>', defaults={'ansId': None},
                 view_func=client_response_view, methods=['GET',])
client_response_blueprint.add_url_rule('/clients/ans/', view_func=client_response_view, methods=['POST',])
client_response_blueprint.add_url_rule('/clients/ans/<int:id>', view_func=client_response_view,
                 methods=['PUT', 'DELETE'])

