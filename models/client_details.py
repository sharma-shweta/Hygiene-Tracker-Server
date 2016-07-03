__author__ = 'shweta'

from flask import Blueprint, request, json, make_response, jsonify
from database import db
from server_utils.utils import Serializer
from server_utils.HTTP_status_returns import __OK__, __NOT_FOUND__
from flask.views import MethodView
from datetime import datetime

client_details_blueprint = Blueprint("client_details_blueprint", __name__)

class ClientDetails(db.Model, Serializer):
    __tablename__ = 'client_details'

    id = db.Column(db.Integer, primary_key=True)
    client = db.relationship('ClientRegister')
    clientId = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    maleAdults = db.Column(db.Integer)
    femaleAdults = db.Column(db.Integer)
    maleChildren = db.Column(db.Integer)
    femaleChildren = db.Column(db.Integer)
    totSchoolGoing = db.Column(db.Integer)
    occupation = db.relationship('Occupation')
    occupationId = db.Column(db.Integer, db.ForeignKey('occupations.id'), nullable=False)
    houseType = db.relationship('HouseType')
    houseTypeId = db.Column(db.Integer, db.ForeignKey('housetypes.id'), nullable=False)
    surveyType = db.relationship('SurveyType')
    surveyTypeId = db.Column(db.Integer, db.ForeignKey('surveytypes.id'))
    createDate = db.Column(db.String())

    def __init__(self, clientId="", maleAdults="", femaleAdults="", maleChildren="", femaleChildren="", totSchoolGoing="",
                 occupationId="", houseTypeId="", surveyTypeId=""):
        self.clientId = clientId
        self.maleAdults = maleAdults
        self.femaleAdults = femaleAdults
        self.maleChildren= maleChildren
        self.femaleChildren = femaleChildren
        self.totSchoolGoing == totSchoolGoing
        self.occupationId = occupationId
        self.houseTypeId = houseTypeId
        self.surveyTypeId = surveyTypeId
        self.createDate = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __repr__(self):
        return {"Client": self.clientId}

    def __unicode__(self):
        return self.name

    def serialize(self):
        return Serializer.serialize(self)

class ClientDetailsAPI(MethodView):
    def get(self, id):
        if id is None:
            clients = ClientDetails.query.all()
            message = {"results": (ClientDetails.serialize_list(clients))}
            return make_response(jsonify(message), 200)
        client = ClientDetails.query.filter(ClientDetails.id==id).first()
        return make_response(json.dumps(client.serialize()), 200)

    def post(self):
        question = ClientDetails(
                    request.form['clientId'],
                    request.form['maleAdults'],
                    request.form['femaleAdults'],
                    request.form['maleChildren'],
                    request.form['femaleChildren'],
                    request.form['totSchoolGoing'],
                    request.form['occupationId'],
                    request.form['houseTypeId'],
                    request.form['surveyTypeId']
                    )
        db.session.add(question)
        db.session.commit()
        return __OK__()

    def delete(self, id):
        db.session.delete(ClientDetails.query.get(id))
        db.session.commit()
        return __OK__()

    def put(self, id):
        client = ClientDetails.query.get(id)
        client.clientId = request.form['clientId']
        client.maleAdults = request.form['maleAdults']
        client.femaleAdults = request.form['femaleAdults']
        client.maleChildren = request.form['maleChildren']
        client.femaleChildren = request.form['femaleChildren']
        client.totSchoolGoing = request.form['totSchoolGoing']
        client.occupationId = request.form['occupationId']
        client.houseTypeId = request.form['houseTypeId']
        client.surveyType = request.form['surveyTypeId']
        db.session.commit()
        return __OK__()


client_details_view = ClientDetailsAPI.as_view('survey_q_api')
client_details_blueprint.add_url_rule('/clients/details/', defaults={'id': None},
                 view_func=client_details_view, methods=['GET',])
client_details_blueprint.add_url_rule('/clients/details/', view_func=client_details_view, methods=['POST',])
client_details_blueprint.add_url_rule('/clients/details/<int:id>', view_func=client_details_view,
                 methods=['GET', 'PUT', 'DELETE'])