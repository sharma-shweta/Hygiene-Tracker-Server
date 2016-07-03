__author__ = 'shweta'

from flask import Blueprint, request, json, make_response, jsonify
from database import db
from server_utils.utils import Serializer
from server_utils.HTTP_status_returns import __OK__, __NOT_FOUND__
from flask.views import MethodView
from datetime import datetime

clients_blueprint = Blueprint("clients_blueprint", __name__)

class ClientRegister(db.Model, Serializer):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    village = db.Column(db.String())
    panchayat = db.Column(db.String())
    block = db.Column(db.String())
    ward = db.Column(db.String())
    taluk = db.Column(db.String())
    district = db.Column(db.String())
    guardian = db.Column(db.String())
    gender = db.Column(db.String())
    houseNo = db.Column(db.String())
    address = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String())
    country = db.Column(db.String())
    status = db.Column(db.String())
    createDate = db.Column(db.String())


    def __init__(self, name="", village="", panchayat="", block="", ward="", taluk="", district="", guardian="",
                 gender="", houseNo="", address="", city="", state="", country="", status=""):
        self.name = name
        self.village = village
        self.panchayat = panchayat
        self.block = block
        self.ward= ward
        self.taluk = taluk
        self.district = district
        self.guardian == guardian
        self.gender = gender
        self.houseNo = houseNo
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.status = status
        self.createDate = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __repr__(self):
        return {"Client": self.name}

    def __unicode__(self):
        return self.name

    def serialize(self):
        return Serializer.serialize(self)

class ClientRegisterAPI(MethodView):
    def get(self, id):
        if id is None:
            clients = ClientRegister.query.all()
            message = {"results": (ClientRegister.serialize_list(clients))}
            return make_response(jsonify(message), 200)
        client = ClientRegister.query.filter(ClientRegister.id==id).first()
        return make_response(json.dumps(client.serialize()), 200)

    def post(self):
        question = ClientRegister(
                    request.form['name'],
                    request.form['village'],
                    request.form['panchayat'],
                    request.form['block'],
                    request.form['ward'],
                    request.form['taluk'],
                    request.form['district'],
                    request.form['guardian'],
                    request.form['gender'],
                    request.form['houseNo'],
                    request.form['address'],
                    request.form['city'],
                    request.form['state'],
                    request.form['country'],
                    request.form['status']
                    )
        db.session.add(question)
        db.session.commit()
        return __OK__()

    def delete(self, id):
        db.session.delete(ClientRegister.query.get(id))
        db.session.commit()
        return __OK__()

    def put(self, id):
        client = ClientRegister.query.get(id)
        client.name = request.form['name']
        client.village = request.form['village']
        client.panchayat = request.form['panchayat']
        client.block = request.form['block']
        client.ward = request.form['ward']
        client.taluk = request.form['taluk']
        client.district = request.form['district']
        client.guardian = request.form['guardian']
        client.gender = request.form['gender']
        client.houseNo = request.form['houseNo']
        client.address = request.form['address']
        client.city = request.form['city']
        client.state = request.form['state']
        client.country = request.form['country']
        client.status = request.form['status']
        db.session.commit()
        return __OK__()


clients_view = ClientRegisterAPI.as_view('survey_q_api')
clients_blueprint.add_url_rule('/clients/', defaults={'id': None},
                 view_func=clients_view, methods=['GET',])
clients_blueprint.add_url_rule('/clients/', view_func=clients_view, methods=['POST',])
clients_blueprint.add_url_rule('/clients/<int:id>', view_func=clients_view,
                 methods=['GET', 'PUT', 'DELETE'])