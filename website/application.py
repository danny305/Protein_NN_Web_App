from flask import url_for,render_template, redirect,request, jsonify,flash,\
                    make_response, session
from flask_jwt_extended import (create_access_token, create_refresh_token,
                            jwt_required, get_jwt_identity, get_jwt_claims,
                            set_access_cookies,set_refresh_cookies,
                            unset_jwt_cookies, get_raw_jwt, jwt_refresh_token_required)

from forms import RegisterForm, LoginForm, NNForm
from models import Users

from website import app,db,jwt
from subprocess import call






@app.route('/')
def homepage():
    print(request.headers)
    return render_template('homepage.html')



@app.route('/FAQ/')
def FAQ_page():
    return render_template("FAQ_page.html")



@app.route('/token/refresh', methods=['GET','POST'])
@jwt_refresh_token_required
def refresh():
    #Create the new access token
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    #Set the JWT access cookie in the response
    response = make_response(redirect(request.referrer))
    set_access_cookies(response,access_token)
    return response





@app.route('/register/', methods=['GET','POST'])
def register_page():
    #ToDo this logic needs to be checked for correct user registration and validation.
    form = RegisterForm(request.form)
    print( request.method, form.validate_on_submit())
    if request.method == "POST" and form.validate_on_submit():
        user = Users(form.first_name.data, form.last_name.data, \
                     form.email.data, form.password.data, form.organization.data)
        user.save_to_db()
        flash("Thanks for Registering. Please login")

        return redirect((url_for("NN_page")))

    return render_template('register.html',form=form)




@app.route('/login/', methods=['GET','POST'])
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

    return render_template('login_page.html', form=form)






@jwt.invalid_token_loader #This allows me to stop people who have not logged in yet.
def missing_JWT_token(msg):
    print(msg)
    return redirect(url_for('login_page'))
    # return "The site being accessed requires a valid JWT to view." \
    #        "Error: {}".format(msg)




@app.route('/NN/', methods=['GET','POST'])
@jwt_required
def NN_page():
    jwt_claims = get_raw_jwt()
    print(jwt_claims)
    user = get_jwt_identity()
    print('User:',user,)
    form = NNForm(request.form, headers=request.headers)
    print(request.form, form.validate_on_submit())
    if request.method == "POST" and form.validate_on_submit():

        return redirect((url_for("success_NN_submission")))

    return render_template('NN_page.html', form=form)




app.route('/submission-successful')
def success_NN_submission(error):
    return "The submitted structure has been accepted by the neural net. " \
           "You will receive an email with the results upon completion. "




app.route('/submission-failed')
def failed_NN_submission():
    return "The submitted structure was not accepted by the neural network. " \
           "This is most likely due to a syntax or formatting error. Please " \
           "try again."


if __name__ == "__main__":
    app.run()