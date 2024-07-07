from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db,tlist
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)

@app.route('/',methods=["GET","POST"])
def hello_world():
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo=tlist(Title=title,desc=desc,date_time=datetime.utcnow())
        db.session.add(todo)
        db.session.commit()
    alltodo=tlist.query.all()
    return render_template('index.html' , alltodo=alltodo)


@app.route('/about')
def about():
    return render_template('About.html')
@app.route('/search', methods=["GET"])
def search():
    query = request.args.get('query', '')

    print(f"Query: {query}")
   
    if query:
        # Filter titles based on the query
        results = tlist.query.filter(tlist.Title.ilike(f'%{query}%')).all()
    else:
        results = []
    
    return render_template('search.html', query=query,  results=results)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo=tlist.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=["GET","POST"])
def update(sno):
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo=tlist.query.filter_by(sno=sno).first()
        todo.Title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo=tlist.query.filter_by(sno=sno).first()
    return render_template('update.html' , todo=todo)
if __name__ == '__main__':
    with app.app_context():
       db.create_all()
    
    app.run(debug=True)