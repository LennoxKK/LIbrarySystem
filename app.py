from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = "xxxxxxxx"

db = SQLAlchemy(app)

# configuring our database uri
# note an error here

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://LKKequinox:LennoxEKK99@LKKequinox.mysql.pythonanywhere-services.com/LKKequinox$testdb"







# basic model

class Accounts(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __init__(user_name, password):
        self.user_name = user_name
        self.password = password


class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)

    def __init__(admin_id, first_name, last_name):
        self.admin_id = admin_id
        self.first_name = first_name
        self.last_name = last_name



class Members(db.Model):
    member_id = db.Column(db.Integer, primary_key=True)
    admission_number = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)

    def __init__(admission_number, first_name, last_name):
        self.admission_number = admission_number
        self.first_name = first_name
        self.last_name = last_name



class Books(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    author = db.Column(db.String(20), nullable=False)
    issue_count = db.Column(db.Integer, nullable=False)

    def __init__(book_id, book_name, title, status, author, issue_count):
        self.book_id = book_id
        self.book_name = book_name
        self.title = title
        self.status = status
        self.author = author
        self.issue_count = issue_count


class Inventory(db.Model):
    inventory_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey(Books.book_id))   # Foreign Key
    quantity = db.Column(db.Integer, nullable=False, default=0)

    def __init__(book_id, quantity):
        self.book_id = book_id
        self.quantity = quantity


class BookDetails(db.Model):
    details_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey(Books.book_id))   # Foreign Key
    edition = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, primary_key=True)

    def __init__(book_id, edition, description, price):
        self.book_id = book_id
        self.edition = edition
        self.description = description
        self.price = price


class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(20), nullable=False)
    category_quantity = db.Column(db.Integer, primary_key=True)

    def __init__(category_name, category_quantity):
        self.category_name = category_name
        self.category_quantity = category_quantity


class Reservation(db.Model):
    reservation_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey(Members.member_id))   # Foreign Key
    book_id = db.Column(db.Integer, db.ForeignKey(Books.book_id))   # Foreign Key

    member_name = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

    def __init__(member_id, book_id, member_name, phone_number):
        self.member_id = member_id
        self.book_id = book_id
        self.member_name = member_name
        self.phone_number = phone_number


class Issue(db.Model):
    issue_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey(Members.member_id))   # Foreign Key
    admin_id = db.Column(db.Integer, db.ForeignKey(Admin.admin_id))   # Foreign Key
    book_id = db.Column(db.Integer, db.ForeignKey(Books.book_id))   # Foreign Key

    date_issued = db.Column(db.DateTime, nullable=False, default=datetime.now())
    returning_date = db.Column(db.DateTime, nullable=False) # need to check date formatting
    returned_date = db.Column(db.DateTime, default=None)

    penalty = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Pending")

    def __init__(member_id, admin_id, book_id, returning_date, penalty, status):
        self.member_id = member_id
        self.admin_id = admin_id
        self.book_id = book_id
        self.returning_date = returning_date
        self.penalty = penalty
        self.status = status


class MemberRecord(db.Model):
    member_id = db.Column(db.Integer, primary_key=True)
    books_borrowed = db.Column(db.Integer, nullable=False)
    books_returned = db.Column(db.Integer, nullable=False)
    books_not_returned = db.Column(db.Integer, nullable=False)

    def __init__(books_borrowed, books_returned):
        self.books_borrowed = books_borrowed
        self.books_returned = books_returned
        self.books_not_returned = books_borrowed - books_returned


class Suppliers(db.Model):
    supplier_id = db.Column(db.Integer, primary_key=True)
    supplier_email = db.Column(db.String(20), nullable=False)
    supplier_name = db.Column(db.String(20), nullable=False)
    supplier_phone_number = db.Column(db.String(20), nullable=False)

    def __init__(supplier_email, supplier_name, supplier_phone_number):
        self.supplier_email = supplier_email
        self.supplier_name = supplier_name
        self.supplier_phone_number = supplier_phone_number


class BookOrders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey(Suppliers.supplier_id))   # Foreign Key
    admin_id = db.Column(db.Integer, db.ForeignKey(Admin.admin_id))   # Foreign Key
    status = db.Column(db.String(20), nullable=False)


    def __init__(supplier_id, admin_id, status):
        self.supplier_id = supplier_id
        self.admin_id = admin_id
        self.status = status


class BookOrderDetails(db.Model):
    order_detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(BookOrders.order_id))   # Foreign Key
    book_id = db.Column(db.Integer, db.ForeignKey(Books.book_id))   # Foreign Key
    book_quantity = db.Column(db.Integer, nullable=False)
    book_price = db.Column(db.Float, nullable=False)

    def __init__(order_id, book_id, book_quantity, book_price):
        self.order_id = order_id
        self.book_id = book_id
        self.book_quantity = book_quantity
        self.book_price = book_price


@app.route('/', methods=['POST','GET'])
def home():
    return 'GOOD NIGHT'


if __name__ == "__main__":
    app.run(debug=True)

