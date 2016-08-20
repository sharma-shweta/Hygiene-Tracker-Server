from flask import Flask, request, jsonify
import flask_admin as admin
from database import db
from flask.ext.restless import APIManager
import os
# from flask.ext.cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456790'
app.config.from_object(os.environ['APP_SETTINGS'])
db.init_app(app)
# CORS(app)

manager = APIManager(app, flask_sqlalchemy_db=db)

from models.server_models import *
from models.admin_models import *
from server_utils.HTTP_status_returns import __OK__, __NOT_FOUND__

from models.occupation import occupation_blueprint
from models.house_type import housetype_blueprint
from models.user import user_blueprint
from models.role import role_blueprint
from models.organization import org_blueprint
from models.surveyq_category import surveyq_category_blueprint
from models.survey_questionnaire import surveyq_blueprint
from models.survey_answer import survey_ans_blueprint
from models.client_register import clients_blueprint
from models.client_details import client_details_blueprint
from models.client_response import client_response_blueprint
from models.survey_types import survey_type_blueprint
from models.client_class import client_class_blueprint
from models.client_class_types import client_class_type_blueprint
from models.client_response_summary import client_response_summary_blueprint

admin = admin.Admin(app, name='Hygiene Tracker', template_mode='bootstrap3', base_template='layout.html')
admin.add_view(UserAdmin(User, db.session))
admin.add_view(OrganizationAdmin(Organization, db.session))
admin.add_view(RoleAdmin(Role, db.session))
admin.add_view(OccupationAdmin(Occupation, db.session))
admin.add_view(HouseTypeAdmin(HouseType, db.session))
admin.add_view(SurveyQCategoryAdmin(SurveyQCategory, db.session, category='Survey'))
admin.add_view(SurveyQuestionnaireAdmin(SurveyQuestionnaire, db.session, category='Survey'))
admin.add_view(SurveyAnswerAdmin(SurveyAnswer, db.session, category='Survey'))
admin.add_view(SurveyTypeAdmin(SurveyType, db.session, category='Survey'))
admin.add_view(ClientRegisterAdmin(ClientRegister, db.session, category='Client'))
admin.add_view(ClientDetailsAdmin(ClientDetails, db.session, category='Client'))
admin.add_view(ClientResponseAdmin(ClientResponse, db.session, category='Client'))
admin.add_view(ClientClassTypeAdmin(ClientClassType, db.session, category='Client'))
#admin.add_view(ClientClassAdmin(ClientClass, db.session, category='Client'))
admin.add_view(ClientResponseSummaryAdmin(ClientResponseSummary, db.session, category='Client'))

app.register_blueprint(org_blueprint)
app.register_blueprint(role_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(occupation_blueprint)
app.register_blueprint(housetype_blueprint)
app.register_blueprint(surveyq_category_blueprint)
app.register_blueprint(surveyq_blueprint)
app.register_blueprint(survey_ans_blueprint)
app.register_blueprint(clients_blueprint)
app.register_blueprint(client_details_blueprint)
app.register_blueprint(client_response_blueprint)
app.register_blueprint(survey_type_blueprint)
app.register_blueprint(client_class_type_blueprint)
#app.register_blueprint(client_class_blueprint)
app.register_blueprint(client_response_summary_blueprint)

@app.route('/')
def home():
    return "Welcome to the Hygiene Tracker PM Tool!"

@app.route('/test', methods=['GET'])
def test():
    return jsonify(username="hello",
                   id=1)

@app.route('/fakelogin', methods=['POST', 'GET'])
def dummyLogin():
    return __OK__()

@app.route('/fakesignup', methods=['POST'])
def dummySignUp():
    return __OK__()

@app.route('/login', methods=['POST'])
def login():
    print ("LOGIN MSG: " + str(request.form))
    try:
        userObj = User.query.filter(User.username==request.form['username']).first()
        if userObj.password == request.form['password']:
            print ("RETURNING MSG: OK")
            return __OK__()
    except:
        print ("RETURNING MSG: ERROR")
        return __NOT_FOUND__()
    return  __NOT_FOUND__()

if __name__ == '__main__':
    app.run()
