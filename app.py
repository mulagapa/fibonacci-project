from flask import Flask, render_template, request, redirect, url_for, session, make_response, abort, jsonify
# from flask_sqlalchemy import SQLAlchemy
import flask_sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from collections import OrderedDict
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:uscfpmlockshop@db/fib'
db = flask_sqlalchemy.SQLAlchemy(app)
print("after", flask_sqlalchemy)


#cache declaration
fibonacci_cache = OrderedDict({})

#defining the database model
class Fibonacci(db.Model):
    n = db.Column(db.Integer, primary_key=True)
    sequence = db.Column(db.Text)

    def __init__(self, n, sequence):
        self.n = n
        self.sequence = sequence

with app.app_context():
    db.create_all()

#initial end point for setting the n value and calculating the n value
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        n = int(request.form['n'])
        error_message = ''
        # error handling the n value
        try:
            if n <= 0:
                abort(404, "Invalid input. Please enter a positive integer.")
                # return redirect(url_for('negative_test_case.html'))

        except ValueError:
            error_message = "Invalid input. Please enter a positive integer."
        if not error_message:
            session['n'] = n
            #checking if the  value is already in the database or the cache
            fib_numbers = Fibonacci.query.filter_by(n=n).first()
            cached_sequence = fibonacci_cache.get(n)
            if fib_numbers or cached_sequence:
                return redirect(url_for('fibonacci_list'))
            #calculating the fibonacci series
            sequence = generate_fibonacci(n)
            #adding the value to the cache
            commitingToCache(sequence,n)
            fib = Fibonacci(n=n, sequence=','.join(map(str, sequence)))
            #adding the value to the database
            commitingToDatabase(fib)
            return redirect(url_for('fibonacci_list'))
    return render_template('index.html')

@app.errorhandler(404)
def bad_request(error):
    resp = make_response(render_template('negative_test_case.html'), 404)
    return resp

def commitingToCache(sequence,n):
    if len(fibonacci_cache) == 5:
        fibonacci_cache.popitem(True)
    fibonacci_cache[n] = sequence
    fibonacci_cache.move_to_end(n, True)

def commitingToDatabase(fibonacci):

    max_retries = 3
    retires = 0
    # making sure the values are added to the database happens
    while retires < max_retries:

        try:
            db.session.add(fibonacci)
            db.session.commit()
            break

        except SQLAlchemyError as err:
            db.session.rollback()
            retires += 1
            if retires == max_retries:
                raise err
        finally:
            db.session.close()




@app.route('/fibonacci_list')
def fibonacci_list():
    fib_numbers = Fibonacci.query.filter_by(n=session['n']).first()
    result_list = fib_numbers.sequence.split(',')
    return render_template('fibonacci_list.html', fib_numbers=result_list)


def generate_fibonacci(n):
    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
        if len(sequence) + 2 == n or len(sequence) + 1 == n:
            fib_numbers = Fibonacci.query.filter_by(n=len(sequence)).first()
            if not fib_numbers:
                fib = Fibonacci(n=len(sequence), sequence=','.join(map(str, sequence)))
                commitingToDatabase(fib)
    return sequence[:n]

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)
