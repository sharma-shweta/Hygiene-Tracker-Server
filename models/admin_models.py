from flask_admin.contrib import sqla

# Customized admin interface
class CustomView(sqla.ModelView):
    # list_template = 'list.html'
    # create_template = 'create.html'
    # edit_template = 'edit.html'
    pass

class UserAdmin(CustomView):
    form_columns = ['name', 'username', 'email', 'password',
                    'telNo1', 'telNo2', 'address', 'city',
                    'state', 'faxNo', 'status', 'role', 'organization']
    column_searchable_list = ('name', 'name')
    column_labels = dict(telNo1='Tel No. 1', telNo2='Tel No. 2', faxNo='Fax No', createDate='Create Date')
    #column_exclude_list = ('password')

class OrganizationAdmin(CustomView):
    form_columns = ['name', 'address', 'contactNo', 'email']
    column_labels = dict(contactNo='Contact No.')

class RoleAdmin(CustomView):
    form_columns = ['name']

class HouseTypeAdmin(CustomView):
    form_columns = ['name']

class OccupationAdmin(CustomView):
    form_columns = ['name']

class SurveyQuestionnaireAdmin(CustomView):
    form_columns = ['surveyQuestion', 'category']
    column_labels = dict(surveyQuestion='Survey Question')

class SurveyQCategoryAdmin(CustomView):
    form_columns = ['name']

class SurveyAnswerAdmin(CustomView):
    form_columns = ['answer', 'question', 'photoReq', 'vidReq']
    column_labels = dict(photoReq='Photo Requirement', vidReq='Video Requirement')

class ClientRegisterAdmin(CustomView):
    form_columns = ['name', 'village', 'panchayat', 'block', 'ward', 'taluk', 'district', 'guardian',
                 'gender', 'houseNo', 'address', 'city', 'state', 'country', 'status']
    column_labels = dict(houseNo='House No.', status='Remarks', createDate='Create Date')

class ClientDetailsAdmin(CustomView):
    form_columns =  ['client', 'maleAdults', 'femaleAdults', 'maleChildren', 'femaleChildren', 'totSchoolGoing',
                 'occupation', 'houseType', 'surveyType']
    column_labels = dict(maleAdults='Male Adults', femaleAdults='Female Adults', maleChildren='Male Children',
                         femaleChildren='Female Children', totSchoolGoing='Total School Going', houseType='House Type',
                         surveyType='Survey Type', createDate='Create Date')

class ClientResponseAdmin(CustomView):
    form_columns = ['client', 'user', 'question', 'answer', 'answerDesc']
    column_labels = dict(answerDesc='Answer Comments', createDate='Create Date')

class SurveyTypeAdmin(CustomView):
    form_columns = ['name']

class ClientClassAdmin(CustomView):
    form_columns = ['client', 'classType', 'status']

class ClientClassTypeAdmin(CustomView):
    form_columns = ['name']

class ClientResponseSummaryAdmin(CustomView):
    form_columns = ['client', 'user', 'clientClassType', 'remarks']
    column_labels = dict(clientClassType='Client Class Type', createDate='Create Date')