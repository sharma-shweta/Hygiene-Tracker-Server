from flask import Blueprint, request, json, make_response, jsonify
from database import db
from server_utils.utils import Serializer
from server_utils.HTTP_status_returns import __OK__, __NOT_FOUND__
from flask.views import MethodView
from datetime import datetime

org_blueprint = Blueprint("org_blueprint", __name__)

class Organization(db.Model, Serializer):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.String())
    contactNo = db.Column(db.String())
    email = db.Column(db.String())
    createDate = db.Column(db.String())

    def __init__(self, name="", address="", contactNo="", email=""):
        self.name = name
        self.address = address
        self.contactNo = contactNo
        self.email = email
        self.createDate = str(datetime.utcnow())

    def __repr__(self):
        return {"Organization": self.name}

    def __unicode__(self):
        return self.name

    def serialize(self):
        return Serializer.serialize(self)

class OrganizationAPI(MethodView):
    def get(self, id):
        if id is None:
            organzations = Organization.query.all()
            message = {"results": (Organization.serialize_list(organzations))}
            return make_response(jsonify(message), 200)
        organzation = Organization.query.filter(Organization.id==id).first()
        return make_response(json.dumps(organzation.serialize()), 200)

    def post(self):
        org = Organization(
            request.form['name'],
            request.form['address'],
            request.form['contactNo'],
            request.form['email'],
        )
        db.session.add(org)
        db.session.commit()
        return __OK__()

    def delete(self, id):
        db.session.delete(Organization.query.get(id))
        db.session.commit()
        return __OK__()

    def put(self, id):
        org = Organization.query.get(id)
        org.name = request.form['name']
        org.address = request.form['address']
        org.contactNo = request.form['contactNo']
        org.email = request.form['email']
        db.session.commit()
        return __OK__()


organization_view = OrganizationAPI.as_view('organization_api')
org_blueprint.add_url_rule('/organizations/', defaults={'id': None},
                 view_func=organization_view, methods=['GET',])
org_blueprint.add_url_rule('/organizations/', view_func=organization_view, methods=['POST',])
org_blueprint.add_url_rule('/organizations/<int:id>', view_func=organization_view,
                 methods=['GET', 'PUT', 'DELETE'])