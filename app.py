from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=False)
    data = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"Title: {self.title} : Notes: {self.data}"

# Get all notes    
@app.route("/get", methods=["GET"])
def get_all():
    notes = Notes.query.all()
    output = []
    for note in notes:
        note_data = {"title":note.title,"data":note.data}
        output.append(note_data)
    return {"notes":output}

# Get one note
@app.route("/get/<id>",methods=["GET"])
def get_note(id):
    note = Notes.query.filter_by(id=id).first()
    if note is None:
        return {"error": "Not found"}
    return {"note": note.data}

# Add a note
@app.route("/add", methods=["POST"])
def add_note():
    new_note = Notes(title=request.json["title"], data=request.json["data"])
    db.session.add(new_note)
    db.session.commit()
    return {new_note.id :new_note.data}

# Delete a note
@app.route("/delete/<id>", methods=["DELETE"])
def delete_note(id):
    delete_note = Notes.query.filter_by(id=id).first()
    if delete_note is None:
        return {"error": "not found"}
    db.session.delete(delete_note)
    db.session.commit()
    return {"message": "Deleted"}

# Update a note
@app.route("/update/<id>",methods=["PUT"])
def update(id):
    update_note = Notes.query.filter_by(id=id).first()
    if update_note is None:
        return{"error":"note not found"}
    else:
        update_note.title=request.json["title"]
        update_note.data=request.json["data"]
        db.session.commit()
        return {"message": "updated" }   
   
if __name__ == "__main__":
    app.run(debug=True)