# import re
# import codecs
# from bs4 import BeautifulSoup as bs
# from functools import wraps

from flask import jsonify, current_app, redirect, url_for, request, make_response
from flask_jwt_extended import (get_raw_jwt,get_jwt_identity,
                                verify_jwt_refresh_token_in_request,
                                unset_jwt_cookies)
from jwt import ExpiredSignatureError
from wtforms.validators import Regexp, EqualTo, ValidationError

from website import jwt

# def find_all_css_lines_in_file(filename):
#     with open("./templates/{}".format(filename),'r') as f:
#         soup = bs(f.read(),'lxml')
#     print(soup.prettify())
#     print(soup.find_all('link'))
#
# find_all_css_lines_in_file('index.html')




#get username from refresh jwt and redirects to the refresh_endpoint passing the username
@jwt.expired_token_loader
def handle_expired_token():
    try:
        verify_jwt_refresh_token_in_request()
    except ExpiredSignatureError:
        print('REFRESH TOKEN has expired. Rerouting to login page...')
        response = make_response(redirect(url_for('login_page')))
        unset_jwt_cookies(response)
        return response
    #print(current_app.config['JWT_USER_CLAIMS'])
    username = get_jwt_identity()
    raw_jwt_claim = get_raw_jwt()
    print(jsonify(user= username, raw_jwt=raw_jwt_claim))
    return redirect(url_for('refresh_endpoint', username=username,
                            prev_url=request.url), code=307)



#This allows me to stop people who have not logged in yet.
@jwt.invalid_token_loader
def missing_JWT_token(msg):
    print('from missing_JWT_token:', msg)
    response = make_response(redirect(url_for('login_page')))
    unset_jwt_cookies(response)
    return response
    # return "The site being accessed requires a valid JWT to view." \
    #        "Error: {}".format(msg)




#This decorator is not being used but I might use it later if I decide to refactor.
def refresh_token(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_refresh_token_in_request()
        print(current_app.config['JWT_USER_CLAIMS'])
        user = get_jwt_identity()
        #ref_token = jwt._decode_jwt_from_cookies('refresh')
        print("refresh_token_user:", user)
        return jsonify(user=user)
        #return flask response from here
    return wrapper




#This is to check if a password does not the regexp. If it does match then pw is not accepted.
class NoneRegExp(Regexp):
    def __call__(self, form, field, message=None):
        match = self.regex.match(field.data or '')
        if match:
            if message is None:
                if self.message is None:
                    message = field.gettext('Invalid input.')
                else:
                    message = self.message

            raise ValidationError(message)
        return match


#This is to make sure either the pdb_struct is provided or a pdb file is uploaded but not both.
class OrTo(EqualTo):
    """
    Compares if 2 fields are both provided when only 1 should be (the 'other' one).

    :param fieldname:
        The name of the 'other' field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if other.data and field.data:
            d = {
                'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                'other_name': self.fieldname
            }
            message = self.message
            if message is None:
                message = field.gettext('{} and {} cannot both be provided'\
                                        .format(other.label.text,field.label.text))
            raise ValidationError(message % d)
