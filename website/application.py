from flask import url_for,render_template, redirect,request, jsonify,flash,\
                    make_response, session

from flask_jwt_extended import (create_access_token, create_refresh_token,
                            jwt_required, get_jwt_identity, get_jwt_claims,
                            set_access_cookies,set_refresh_cookies,
                            unset_jwt_cookies, get_raw_jwt,
                            jwt_refresh_token_required, jwt_optional,
                            verify_jwt_in_request_optional,
                            verify_jwt_refresh_token_in_request)


from forms import RegisterForm, LoginForm, NNForm
from models import Users
from tools import missing_JWT_token, handle_expired_token

from website import app,db,jwt
from subprocess import call






@app.route('/')
@jwt_optional
def homepage():
    current_user = get_jwt_identity() or None
    # if current_user == None:
    #     raise Exception('Anonymous User!!')
    # else:
    #return jsonify(current_user=current_user)

    return render_template('homepage.html', active_page='Home', current_user=current_user)



@app.route('/FAQ')
@jwt_optional
def FAQ_page():
    current_user = get_jwt_identity() or None
    return render_template("FAQ_page.html", active_page='FAQ', current_user=current_user)


#ToDo When the token expires I get an HTTP status code of 401 I can use expired_token_loader refresh token.

@app.route('/token/refresh', methods=['GET','POST'])
@jwt_refresh_token_required
def refresh_endpoint():
    # Create the new access token from refresh token username passed in.
    username = request.args['username']
    print('refresh_endpoint.. creating new access token for user: ', username)
    access_token = create_access_token(username)

    # #Set the JWT access cookie in the response
    response = make_response(redirect(request.args['prev_url']))
    set_access_cookies(response,access_token)
    return response

    #trouble shooting code
    # ref_token = request.cookies.get('refresh_token_cookie')
    # csrftoken = request.cookies.get('csrftoken')
    # decode_ref_token = decode_token(ref_token)
    # print('ref_token:', ref_token)
    # print('current_user:', current_user, get_raw_jwt())




@app.route('/token/remove', methods=['GET','POST'])
@jwt_required
def logout_endpoint():
    #ToDo Still need to build the logout page.
    #response = make_response(redirect(url_for('logout_page')))
    verify_jwt_refresh_token_in_request()
    username = get_jwt_identity()
    response = make_response(redirect(url_for("logout_page",username=username)))
    unset_jwt_cookies(response)
    session['successful_logout'] = True
    return  response




@app.route('/register', methods=['GET','POST'])
def register_page():
    #ToDo this logic needs to be checked for correct user registration and validation.
    form = RegisterForm(request.form)
    print( request.method, form.validate_on_submit())
    if request.method == "POST" and form.validate_on_submit():
        user = Users(form.first_name.data, form.last_name.data, \
                     form.email.data, form.password.data, form.organization.data)
        user.save_to_db()
        flash("Thanks for Registering. Please login")

        return redirect(url_for("NN_page"))

    return render_template('register.html',active_page='Register', form=form, )



@app.route('/login/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginForm(request.form)
    print(request.method, request.form)
    if request.method == "POST":
        #This checks if the user is in the db and returns the user obj.
        user = form.validate_on_submit()
        if user:
            access_token = create_access_token(identity=user.email, fresh=True)
            refresh_token = create_refresh_token(identity=user.email)

            response = make_response(redirect(url_for('NN_page')))
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            #response.headers['Authorization'] = 'Bearer {}'.format(access_token)
            print(response)
            return response
            #return jsonify({'access_token':access_token})
            #return redirect((url_for("NN_page")))

    return render_template('login_page.html', active_page='Login', form=form)




@app.route('/logged_out',methods=['GET','POST'])
def logout_page():
    #print("session:", session.viewitems())
    #print(session.pop('successful_logout',False))
    # if session.pop('successful_logout' == True:
    #     return render_template('logout_page.html')
    # else:
    #    return redirect(url_for('homepage'))

    if request.cookies.get('refresh_token_cookie',False):
        return redirect(url_for('logout_endpoint'))
    elif session.has_key('successful_logout'):
        session.pop('successful_logout')
        return render_template('logout_page.html',
                               username=request.args.get('username','User'))
    else:
        return redirect(url_for('homepage'))
        #raise Exception('Shit is fucked','Cookies:',request.cookies,
        #                'Session:', session.viewitems())

@app.route('/NN/', methods=['GET','POST'])
@jwt_required
def NN_page():
    jwt_claims = get_raw_jwt()
    #print(jwt_claims)
    #print('cookie keys:', request.cookies.get('refresh_token_cookie'))
    user = get_jwt_identity() or None
    print('User:',user)
    form = NNForm(request.form)
    print(request.data)
    print(request.form.viewkeys(), form.validate_on_submit())
    if request.method == "POST" and form.validate_on_submit():

        return "Submission successful" #redirect(url_for("success_NN_submission"))

    return render_template('NN_page.html', active_page='NN',form=form, current_user=user)




#This function is to test jwt_optional functionality.
@app.route('/partially-protected', methods=['GET'])
@jwt_optional
def partially_protected():
    # If no JWT is sent in with the request, get_jwt_identity()
    # will return None
    current_user = get_jwt_identity()
    print('current user PARTIALLY Protected:', current_user)
    if current_user:
        return jsonify(logged_in_as=current_user), 200
    else:
        return jsonify(logged_in_as='anonymous user'), 200




app.route('/submission-successful')
def success_NN_submission():
    return "The submitted structure has been accepted by the neural net. " \
           "You will receive an email with the results upon completion. "




app.route('/submission-failed')
def failed_NN_submission():
    return "The submitted structure was not accepted by the neural network. " \
           "This is most likely due to a syntax or formatting error. Please " \
           "try again."


if __name__ == "__main__":
    app.run()