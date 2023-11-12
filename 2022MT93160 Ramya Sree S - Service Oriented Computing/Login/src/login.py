from flask import Flask, render_template, request
import mysql.connector
import requests

app = Flask(__name__)

db_config = {
    "host": "localhost",
    "user": "Ramya",
    "password": "Nagamani@230498",
    "database": "assignment_login"
}

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("SELECT c_type FROM customer_profile WHERE c_name = %s AND c_password = %s", (username, password))
    result = cursor.fetchone()

    for x in result:
        c_type = x

    print(c_type)

    data = {'c_name': username}
    if result:
        print('c_type retrieved')
        if c_type == 'Customer':
            print('c_type and Customer matches')
            # Send an HTTP GET request to the second microservice customer interface
            response = requests.get('http://localhost:5001/products')
        else:
            if c_type == 'Administrator':
                print('c_type and Administrator matches')
                # Send an HTTP GET request to the second microservice customer interface
                response = requests.get('http://localhost:5001/')
        # Return the response from the second microservice
        return response.text
    else:
        return 'Unauthorized User'

@app.route('/forgot_password')
def forgot_password_page():
    return render_template('forgot_password.html')

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    
    username = request.form['username']
    mobile = request.form['mobile']

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM customer_profile WHERE c_name = %s AND c_mobile = %s", (username, mobile,))
    result = cursor.fetchone()

    if result:
        # Send password recovery instructions to the user
        return 'Password recovery instructions sent to your registered mobile number.'
    else:
        return 'Mobile number not found in our records.'

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    new_user_type = request.form['new-user-type']
    new_username = request.form['new-username']
    new_password = request.form['new-password']
    new_mobile = str(request.form['new-mobile'])
    new_address = request.form['new-address']
    
    print('1.', new_user_type, new_username, new_mobile, new_address)
    
    data = {'c_name': new_username, 'c_mobile': new_mobile, 'c_address': new_address}
    data1 = {'c_name': new_username}
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    print(new_user_type)
    if new_user_type == 'Customer':
        cursor.execute("INSERT INTO customer_profile (c_type, c_name, c_password, c_mobile) VALUES (%s, %s, %s, %s)", (new_user_type,new_username, new_password, new_mobile))
        print('New Customer being added.')
        # Send the JSON message to the Checkout microservice to add username, mobile no. and address to order_checkout table
        response = requests.get('http://localhost:5001/products')
        print('New Customer successfully added.')
        connection.commit()
        # Send an HTTP GET request to the Product microservice Customer interface
        response = requests.get('http://localhost:5001/products', params=data1)
    else: 
        if new_user_type == 'Administrator':
            cursor.execute("INSERT INTO customer_profile (c_type, c_name, c_password, c_mobile) VALUES (%s, %s, %s, %s)", (new_user_type,new_username, new_password, new_mobile))
            print('New Administrator being added.')
            connection.commit()
            # Send an HTTP GET request to the Product microservice Administrator interface
            response = requests.get('http://localhost:5001/')
            
    return response.text

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
