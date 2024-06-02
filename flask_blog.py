from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask import Flask, jsonify, render_template
from requests import Request, Session
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from forms import RegistrationForm, LoginForm
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

@app.route("/about", methods=['GET', 'POST'])
def about():
    print("About route called")
    cryptocurrency_data = None
    error = None

    if request.method == 'POST':
        try:
            symbol = request.form['symbol'].upper()
            print(f"Fetching data for {symbol}")
            cryptocurrency_data = get_cryptocurrency_data(symbol)
            if not cryptocurrency_data:
                error = f"Data for {symbol} not found."
        except Exception as e:
            error_message = f"Error processing form data: {str(e)}"
            print(error_message)
            error = "An error occurred while processing the form data. Detailed error: " + error_message

    return render_template('about.html', cryptocurrency_data=cryptocurrency_data, error=error)

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
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'aceb8534-869d-491c-8a1b-323d12520298'
    }

    # Define the file path
    file_path = f"{symbol}_data.json"

    # Check if the file already exists
    if os.path.exists(file_path):
        # Read and return the data from the file
        with open(file_path, 'r') as file:
            crypto_info = json.load(file)
        return crypto_info

    try:
        # Fetch metadata including description
        info_url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'
        info_parameters = {'symbol': symbol}
        response_info = requests.get(info_url, headers=headers, params=info_parameters)
        response_info.raise_for_status()
        info_data = response_info.json()
        print("API Info Data:", json.dumps(info_data, indent=4))

        # Check the structure of the response
        if 'data' in info_data and isinstance(info_data['data'], dict):
            crypto_info = info_data['data'][symbol][0] if isinstance(info_data['data'][symbol], list) else info_data['data'][symbol]
        else:
            print("No 'data' key or 'symbol' key in API response for info.")
            return None

        # Fetch latest price data
        quote_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        quote_parameters = {'symbol': symbol}
        response_quote = requests.get(quote_url, headers=headers, params=quote_parameters)
        response_quote.raise_for_status()
        quote_data = response_quote.json()
        print("API Quote Data:", json.dumps(quote_data, indent=4))

        # Check the structure of the response
        if 'data' in quote_data and isinstance(quote_data['data'], dict):
            crypto_quote = quote_data['data'][symbol][0] if isinstance(quote_data['data'][symbol], list) else quote_data['data'][symbol]
        else:
            print("No 'data' key or 'symbol' key in API response for quote.")
            return None

        # Combine info and quote data
        crypto_info['quote'] = crypto_quote['quote']

        # Save the combined data to a JSON file
        with open(file_path, 'w') as file:
            json.dump(crypto_info, file, indent=4)

        return crypto_info

    except requests.exceptions.RequestException as e:
        print("API call failed:", str(e))
        return None
    except KeyError as e:
        print(f"Key error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
if __name__ == '__main__':
    app.run(debug=True)
