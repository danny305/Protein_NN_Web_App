from flask import url_for,render_template, redirect,request, flash
from flask_bootstrap import Bootstrap
from forms import RegisterForm
from models import RegUsers

from website import app,db
from subprocess import call






@app.route('/')
def homepage():

    return render_template('homepage.html')

@app.route('/NN/')
def NN_page():

    return render_template("NN_page.html")


@app.route('/FAQ/')
def FAQ_page():

    return render_template("FAQ_page.html")


@app.route('/register/', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    print( request.method, form.validate())
    if request.method == "POST" and form.validate():
        user = RegUsers(form.first_name.data,form.last_name.data,\
                        form.email.data, form.organization.data, )

        db.session.add(user)
        db.session.commit()
        flash("Thanks for Registering. Check your email for your ID code.")

        return redirect((url_for("NN_page")))

    return render_template('register.html',form=form)



if __name__ == "__main__":
    #nav.init_app(app)

    app.run(debug=True)