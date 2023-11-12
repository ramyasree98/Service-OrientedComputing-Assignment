from flask import Flask, render_template, request, redirect, url_for
import pymysql
import requests

app = Flask(__name__)

# Connect to the database
db = pymysql.connect(host="localhost", user="Ramya", password="Nagamani@230498", database="book_store")


@app.route("/")
def index():
    # Get all products from the databases
    cursor = db.cursor()
    cursor.execute("SELECT id,title,author,price FROM products")
    # Fetch the product data using cursor.fetchall()
    products = cursor.fetchall()
    return render_template("prod_admin.html", products=products)

@app.route("/products")
def main_products():
    # Get the data from the request
    data = request.args
    key1 = data.get('c_name')
    print(f'Login Microservice has passed Username {key1} to Product Microservice after successful Login')
    # Get all products from the database
    cursor = db.cursor()
    cursor.execute("SELECT id,title,author,price FROM products")
    # Fetch the product data using cursor.fetchall()
    products = cursor.fetchall()
    return render_template("prod_main.html", products=products, key1=key1)




@app.route("/edit_product/<id>")
def edit_product(id):
    # Get the product with the specified ID
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products WHERE id=%s", (id,))
    product = cursor.fetchone()

    return render_template("edit_product.html", product=product)


    

@app.route("/update_product", methods=["POST"])
def update_product():
    # Update the product with the specified ID
    id = request.form["id"]
    title = request.form["title"]
    author = request.form["author"]
    price = request.form["price"]

    cursor = db.cursor()
    cursor.execute("UPDATE products SET title=%s, author=%s, price=%s WHERE id=%s", (title, author, price, id))
    db.commit()

    return redirect("/")

@app.route("/delete_product/<id>")
def delete_product(id):
    # Delete the product with the specified ID
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE id=%s", (id,))
    db.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)

