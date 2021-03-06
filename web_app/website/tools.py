
from flask import render_template, jsonify, current_app, redirect, url_for, request, make_response
from flask_jwt_extended import (get_raw_jwt,get_jwt_identity,
                                create_access_token,create_refresh_token,
                                set_access_cookies,set_refresh_cookies,
                                verify_jwt_refresh_token_in_request,
                                unset_jwt_cookies)
from jwt import ExpiredSignatureError
from wtforms.validators import Regexp, EqualTo, ValidationError

from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from . import app,jwt,mail, mj





'''JWT Authentication Helper Functions'''
def create_JWT_n_redirect(user, redirect_page='homepage'):
    #The user must be a database object.
    access_token = create_access_token(identity=user.email, fresh=True)
    refresh_token = create_refresh_token(identity=user.email)

    response = make_response(redirect(url_for(redirect_page)))
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    app.logger.info('Create access and refresh token, redirecting to {}'.format(redirect_page))
    # response.headers['Authorization'] = 'Bearer {}'.format(access_token)
    return response




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
@jwt.unauthorized_loader
@jwt.invalid_token_loader
def missing_JWT_token(msg):
    print('from missing_JWT_token func:', msg)
    app.logger.warning('End user attempted to access a page that requires valid JWT. '
                       '{}'.format(msg))
    message_header = "Login Required"
    message_body = "This page is only accessible to logged in users."
    response = make_response(render_template('intermediate_page.html',
                                             message_header=message_header,
                                             message_body=message_body,
                                             login=True,
                                             register=True,
                                             ))
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









'''Form Validation Helper Functions'''
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





'''EMAIL Helper Functions'''

#This is what I used for google
def send_email(subject,recipient, text_body=None, html_body=None):
    msg = Message(subject, recipients=recipient, sender=app.config['MAIL_USERNAME'])
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)





#Mailjet email server settings
def mj_send_email(recipient,sender="confirm_email_nn_app@yahoo.com",
                  subject='Confirm your email', text_body=None, html_body=None):
    data = {
        'FromEmail': sender,
        'FromName': '<no-reply-email_confirmation>',
        'Subject': subject,
        'Text-part': text_body,
        'Html-part': html_body,
        'Recipients': [
            {
                "Email": recipient
            }
        ]
    }
    result = mj.send.create(data=data)
    #pass


"""
This is to send an email other than the confirmation email. The function for email
confirmation is a method in the User model. 
"""
def send_confirmation_email(user_email='danny.jesus.diaz.94@gmail.com',
                            subject='NN Web App email',
                            html_template='email_confirmation_2.html'):
    confirm_serializer = URLSafeTimedSerializer(app.config['MAIL_SECRET_KEY'])
    token = confirm_serializer.dumps(user_email,salt=app.config['MAIL_SALT'])
    confirm_url = url_for('confirm_email_endpoint',token=token, _external=True)
    print(confirm_url)
    html = render_template(html_template,confirm_url=confirm_url)

    send_email(subject,
               [user_email,app.config['MAIL_DEFAULT_SENDER']],
               text_body=confirm_url,
               html_body=html)

    #mj_send_email(recipient=user_email,html_body=html)

