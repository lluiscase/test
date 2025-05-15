from flask import Flask, redirect,render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer,String
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id: Mapped[int]= mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(200),nullable=False)
    date_created: Mapped[datetime] = mapped_column(default=datetime.now)
    

def __repr__(self):
    return '<Task %r>' % self.id

@app.route('/', methods=['POST','GET'] )
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        type_content = request.form.getlist('options')
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>') 
def delete(id):
    delete_item = Todo.query.get(id)
    try:
        db.session.delete(delete_item)
        db.session.commit()
        return redirect('/')
    except:
        print("Algo deu errado")


@app.route('/update/<int:id>', methods=['GET','POST']) 
def update(id):
    update_item = Todo.query.get(id)
    print(update_item)
    if request.method == 'POST':
        update_item.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            print("Troca de informações não funcionou")
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)