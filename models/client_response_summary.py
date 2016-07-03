__author__ = 'shweta'

from flask import Blueprint, request, json, make_response, jsonify
from database import db
from server_utils.utils import Serializer
from server_utils.HTTP_status_returns import __OK__, __NOT_FOUND__
from flask.views import MethodView
from datetime import datetime

client_response_summary_blueprint = Blueprint("client_response_summary_blueprint", __name__)

class ClientResponseSummary(db.Model, Serializer):
    __tablename__ = 'clientresponsesummary'

    id = db.Column(db.Integer, primary_key=True)
    client = db.relationship('ClientRegister')
    clientId = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    user = db.relationship('User')
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    clientClassType = db.relationship('ClientClassType')
    clientClassTypeId = db.Column(db.Integer, db.ForeignKey('clientclasstypes.id'))
    remarks = db.Column(db.String())
    createDate = db.Column(db.String())

    def __init__(self, clientId="", userId="", clientClassTypeId="", remarks=""):
        self.clientId = clientId
        self.userId = userId
        self.clientClassTypeId = clientClassTypeId
        self.remarks = remarks
        self.createDate = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __repr__(self):
        return {"Client Response": self.answerDesc}

    def __unicode__(self):
        return self.answerDesc

    def serialize(self):
        return Serializer.serialize(self)

class ClientResponseSummaryAPI(MethodView):
    def get(self, clientId, ansId):
        if ansId is None:
            ans = ClientResponseSummary.query.all()
            message = {"results": (ClientResponseSummary.serialize_list(ans))}
            return make_response(jsonify(message), 200)
        ans = ClientResponseSummary.query.filter(ClientResponseSummary.id==id).first()
        return make_response(json.dumps(ans.serialize()), 200)

    def post(self):
        ans = ClientResponseSummary(
                    request.form['clientId'],
                    request.form['userId'],
                    request.form['clientClassTypeId'],
                    request.form['remarks']
                )
        db.session.add(ans)
        db.session.commit()
        return __OK__()

    def delete(self, id):
        db.session.delete(ClientResponseSummary.query.get(id))
        db.session.commit()
        return __OK__()

    def put(self, id):
        ans = ClientResponseSummary.query.get(id)
        ans.clientId = request.form['clientId']
        ans.userId = request.form['userId']
        ans.clientClassId = request.form['clientClassTypeId']
        ans.remarks = request.form['remarks']
        db.session.commit()
        return __OK__()


client_response_summary_view = ClientResponseSummaryAPI.as_view('client_response_api')
client_response_summary_blueprint.add_url_rule('/clients/<int:clientId>/summary/<int:ansId>', defaults={'ansId': None},
                 view_func=client_response_summary_view, methods=['GET',])
client_response_summary_blueprint.add_url_rule('/clients/summary/', view_func=client_response_summary_view, methods=['POST',])
client_response_summary_blueprint.add_url_rule('/clients/summary/<int:id>', view_func=client_response_summary_view,
                 methods=['PUT', 'DELETE'])

