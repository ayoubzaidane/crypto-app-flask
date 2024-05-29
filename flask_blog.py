from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


app = Flask(__name__)

app.config['SECRET_KEY'] = '130f4371245015b86e679de8ce4af16df122669fdd3803e579b56fa401ad5918'

posts = [
    {
        'author': 'zakaria bouzkarn',
        'title': 'calistenique',
        'content': 'muscle up',
        'date_posted': 'april 2, 2024'
    },
    {
        'author': 'ayoub zaidane',
        'title': 'blockchain',
        'content': 'crypto',
        'date_posted': 'june 1, 2022'
    }
]

@app.route("/")
@app.route("/home")
def home():
    print("Home route called")
    print("Posts:", posts)
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    print("About route called")
    return render_template('about.html')

@app.route("/register", methods=['GET', 'POST'] )
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))    
    return render_template('register.html', title='Register', form=form)
    

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('you have been logged in!','success',)
            return redirect(url_for('home'))
        else:
            flash('login unsuccessful. please check username and password','danger' )
    return render_template('login.html', title='login', form=form)


if __name__ == '__main__':
    app.run(debug=True)


