from flask import url_for,render_template, redirect,request, flash
from flask_bootstrap import Bootstrap
from forms import RegisterForm, LoginForm, NNForm
from models import Users

from website import app,db
from subprocess import call






@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/NN/')
def NN_page():
    form = NNForm(request.form)
    print(request.method, form.validate_on_submit())
    if request.method == "POST" and form.validate_on_submit():
        # user = Users.query.filter_by(email=form.email.data).first_or_404()
        # if user:
        #     if user.check_pw(form.password.data):
        #         return "You successfully logged in."
        #     else:
        #         print(form)
        #         return render_template('login_page.html', form=form)
        # flash("Thanks for Registering. Check your email for your ID code.")
        #
        return redirect((url_for("success_NN_submission")))

    return render_template('NN_page.html', form=form)



app.route('/submission-successful')
def success_NN_submission():
    return "The submitted structure has been accepted by the neural net. " \
           "You will receive an email with the results upon completion. "


app.route('/submission-failed')
def failed_NN_submission():
    return "The submitted structure was not accepted by the neural network. " \
           "This is most likely due to a syntax or formatting error. Please " \
           "try again."


@app.route('/FAQ/')
def FAQ_page():
    return render_template("FAQ_page.html")




@app.route('/register/', methods=['GET','POST'])
def register_page():
    #ToDo this logic needs to be checked for correct user registration and validation.
    form = RegisterForm(request.form)
    print( request.method, form.validate_on_submit())
    if request.method == "POST" and form.validate_on_submit():
        user = Users(form.first_name.data, form.last_name.data, \
                     form.email.data, form.organization.data, )

        db.session.add(user)
        db.session.commit()
        flash("Thanks for Registering. Check your email for your ID code.")

        return redirect((url_for("NN_page")))

    return render_template('register.html',form=form)




@app.route('/login/', methods=['GET','POST'])
def login_page():

    form = LoginForm(request.form)
    print(request.method, form.validate_on_submit())
    if request.method == "POST" and form.validate_on_submit():
        # user = Users.query.filter_by(email=form.email.data).first_or_404()
        # if user:
        #     if user.check_pw(form.password.data):
        #         return "You successfully logged in."
        #     else:
        #         print(form)
        #         return render_template('login_page.html', form=form)
        # flash("Thanks for Registering. Check your email for your ID code.")
        #
        return redirect((url_for("NN_page")))

    return render_template('login_page.html', form=form)




if __name__ == "__main__":
    #nav.init_app(app)

    app.run()