import re
import codecs
from bs4 import BeautifulSoup as bs
from functools import wraps

from flask import jsonify, current_app, redirect, url_for, request, make_response
from flask_jwt_extended import (get_raw_jwt,get_jwt_identity,
                                verify_jwt_refresh_token_in_request,
                                jwt_refresh_token_required, set_access_cookies,
                                unset_jwt_cookies)
from jwt import ExpiredSignatureError
from website import jwt

# def find_all_css_lines_in_file(filename):
#     with open("./templates/{}".format(filename),'r') as f:
#         soup = bs(f.read(),'lxml')
#     print(soup.prettify())
#     print(soup.find_all('link'))
#
# find_all_css_lines_in_file('index.html')



@jwt.invalid_token_loader #This allows me to stop people who have not logged in yet.
def missing_JWT_token(msg):
    print('from missing_JWT_token:', msg)
    return redirect(url_for('login_page'))
    # return "The site being accessed requires a valid JWT to view." \
    #        "Error: {}".format(msg)


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






@jwt.expired_token_loader
def handle_expired_token():
    #get username from jwt and redirect to the refresh_endpoint
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




@jwt.invalid_token_loader #This allows me to stop people who have not logged in yet.
def missing_JWT_token(msg):
    print('from missing_JWT_token:', msg)
    response = make_response(redirect(url_for('login_page')))
    unset_jwt_cookies(response)
    return response
    # return "The site being accessed requires a valid JWT to view." \
    #        "Error: {}".format(msg)



