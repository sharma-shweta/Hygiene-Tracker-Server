__author__ = 'shweta'

from flask import Blueprint, request, json
from database import db
from server_utils.utils import Serializer
from server_utils.HTTP_status_returns import __OK__, __NOT_FOUND__
from flask.views import MethodView
from datetime import datetime

client_class_blueprint = Blueprint("client_class_blueprint", __name__)

class ClientClass(db.Model, Serializer):
    __tablename__ = 'clientclasses'

    id = db.Column(db.Integer, primary_key=True)
    client = db.relationship('ClientRegister', backref='clients.cc')
    clientId = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    classType = db.relationship('ClientClassType', backref='clientclasstypes')
    classTypeId = db.Column(db.Integer, db.ForeignKey('clientclasstypes.id'), nullable=False)
    status = db.Column(db.String())
    createDate = db.Column(db.String())

    def __init__(self, clientId="", classTypeId="", status=""):
        self.clientId = clientId
        self.classTypeId = classTypeId
        self.status = status
        self.createDate = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __repr__(self):
        return "{'Client Class': %s}" % self.status

    def __unicode__(self):
        return self.status

    def serialize(self):
        return Serializer.serialize(self)


class ClientClassAPI(MethodView):
    #TODO: Error handling for all queries (if not found)
    def get(self, id):
        if id is None:
            clientClass = ClientClass.query.all()
            return '{\"results\": %s }' % (ClientClass.serialize_list(clientClass))
        clientClass = ClientClass.query.filter(ClientClass.id==id).first()
        return '{\"results\": %s }' % json.dumps(clientClass.serialize())

    def post(self):
        clientClass = ClientClass(
                            request.form['clientId'],
                            request.form['classTypeId'],
                            request.form['status'],
                        )
        db.session.add(clientClass)
        db.session.commit()
        return __OK__()

    def delete(self, id):
        db.session.delete(ClientClass.query.get(id))
        db.session.commit()
        return __OK__()

    def put(self, id):
        clientClass = ClientClass.query.get(id)
        clientClass.clientId = request.form['clientId']
        clientClass.classTypeId = request.form['classTypeId']
        clientClass.status = request.form['status']
        db.session.commit()
        return __OK__()


client_class_view = ClientClassAPI.as_view('client_class_api')
client_class_blueprint.add_url_rule('/clients/class/', defaults={'id': None},
                 view_func=client_class_view, methods=['GET',])
client_class_blueprint.add_url_rule('/clients/class/', view_func=client_class_view, methods=['POST',])
client_class_blueprint.add_url_rule('/clients/class/<int:id>', view_func=client_class_view,
                 methods=['GET', 'PUT', 'DELETE'])