from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'


class Drink(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=True,nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name}-{self.description}"

@app.route('/')
def index():
    return jsonify("Drinks APP")


def insert(item):
    db.session.add(item)
    db.session.commit()

@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    out = [{'name':drink.name,'description':drink.description} for drink in drinks]
    return {"drinks":out} # Dict serializable by default

@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    if drink is None: return None
    return {"name":drink.name,"description":drink.description}

@app.route('/drinks',methods=['POST'])
def add_drink():
    new_drink = request.json
    drink = Drink(name=new_drink['name'],description = new_drink['description'])
    db.session.add(drink)
    db.session.commit()
    return {"message":202}

@app.route('/drinks/<id>',methods=['DELETE'])
def delete_drink():
    drink = get_drink(id)
    if drink is None: return {"message":404}
    db.session.delete(drink)
    db.session.commit()
    return {"message":202}

def init_db(db):
    db.create_all()

if __name__ == '__main__':
    init_db(db)
    app.run()