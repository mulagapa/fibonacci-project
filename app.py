from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import LargeBinary, Unicode, Integer, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
import redis
# import mysql.connector
from collections import OrderedDict

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:uscfpmlockshop@db/fib'
db = SQLAlchemy(app)
# db = mysql.connector.connect(user='manidhar', host='0.0.0.0', port='3306', password='testing', database='test')


fibonacci_cache = OrderedDict({})


class Fibonacci(db.Model):
    n = db.Column(db.Integer, primary_key=True)
    sequence = db.Column(db.Text)

    def __init__(self, n, sequence):
        self.n = n
        self.sequence = sequence

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        n = int(request.form['n'])
        session['n'] = n
        fib_numbers = Fibonacci.query.filter_by(n=n).first();
        cached_sequence = fibonacci_cache.get(n)
        if fib_numbers or cached_sequence:
            return redirect(url_for('fibonacci_list'))
        sequence = generate_fibonacci(n)
        # fibonacci_cache[n] = sequence
        commitingToCache(sequence,n)
        fib = Fibonacci(n=n, sequence=','.join(map(str, sequence)))
        commitingToDatabase(fib)
        return redirect(url_for('fibonacci_list'))
    return render_template('index.html')


def commitingToCache(sequence,n):
    if len(fibonacci_cache) == 5:
        fibonacci_cache.popitem(True)
    fibonacci_cache[n] = sequence
    fibonacci_cache.move_to_end(n, True)

def commitingToDatabase(fibonacci):

    max_retries = 3
    retires = 0

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
            fib_numbers = Fibonacci.query.filter_by(n=len(sequence)).first();
            if not fib_numbers:
                fib = Fibonacci(n=len(sequence), sequence=','.join(map(str, sequence)))
                commitingToDatabase(fib)
    return sequence[:n]

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)
