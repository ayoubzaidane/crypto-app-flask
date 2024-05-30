from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask import Flask, jsonify, render_template
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import requests
import json
import os

import requests
import json
import os

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

# Replace with your actual CoinMarketCap API key
API_KEY = 'aceb8534-869d-491c-8a1b-323d12520298'

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    print("About route called")
    cryptocurrency_data = get_cryptocurrency_data('BTC')
    print("Cryptocurrency Data:", json.dumps(cryptocurrency_data, indent=4))
    return render_template('about.html', cryptocurrency_data=cryptocurrency_data)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

def get_cryptocurrency_data(symbol):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': symbol,
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }

    try:
        response = requests.get(url, headers=headers, params=parameters)
        response.raise_for_status()
        data = response.json()
        print("API Data:", json.dumps(data, indent=4))

        if 'data' in data:
            # Create a folder to store JSON files if it doesn't exist
            if not os.path.exists('data'):
                os.makedirs('data')

            # Write the data to a JSON file
            with open(f'data/{symbol}_data.json', 'w') as json_file:
                json.dump(data['data'], json_file, indent=4)

            return data['data']
        else:
            print("No 'data' key in API response.")
            return data
    except requests.exceptions.RequestException as e:
        print("API call failed, reading from sample_data.json:", str(e))
        # If the API call fails, read from the sample JSON file
        with open('sample_data.json', 'r') as json_file:
            sample_data = json.load(json_file)
            print("Sample Data:", json.dumps(sample_data, indent=4))
            return sample_data['data']

if __name__ == '__main__':
    app.run(debug=True)
