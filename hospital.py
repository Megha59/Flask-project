from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "Secret Key"
 
#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/hospitaldb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)

class doctor(db.Model):
    did = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    dname = db.Column(db.String(80), unique=True, nullable=False, primary_key=False)
    department = db.Column(db.String(80), unique=True, nullable=False, primary_key=False)

class patient(db.Model):
    pid = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    pname = db.Column(db.String(80), unique=True, nullable=False, primary_key=False)
    disease = db.Column(db.String(80), unique=True, nullable=False, primary_key=False)


@app.route('/',methods=["GET"])

def home():
    return render_template("home.html")

@app.route('/doctor', methods=["GET", "POST"])
def docindex():
    
    if request.form:
        try:
            doct = doctor(did=request.form.get("did"),dname=request.form.get("dname"),department=request.form.get("dept"))
            db.session.add(doct)
            db.session.commit()
        except Exception as e:
            print("Failed to add doctor")
            print(e)

    doc = doctor.query.all()
    return render_template("docindex.html", doctor=doc)

@app.route('/patient', methods=["GET", "POST"])
def patindex():
    
    if request.form.get("add"):
        try:
            pat = patient(pid=request.form.get("pid"),pname=request.form.get("pname"),disease=request.form.get("disease"))
            db.session.add(pat)
            db.session.commit()
        except Exception as e:
            print("Failed to add patient")
            print(e)
    pat = patient.query.all()
    return render_template("patindex.html", patient=pat)

@app.route("/doctor/update", methods=["POST"])
def dupdate():
    try:
        newid = request.form.get("newid")
        oldid = request.form.get("oldid")
        newdname = request.form.get("newdname")
        olddname = request.form.get("olddname")
        newdept = request.form.get("newdept")
        olddept = request.form.get("olddept")
        doc = doctor.query.filter_by(did=oldid,dname=olddname,department=olddept).first()
        doc.did = newid
        doc.dname = newdname
        doc.department = newdept
        db.session.commit()
    except Exception as e:
        print("Couldn't update doctor")
        print(e)
    return redirect("/doctor")

@app.route("/patient/update", methods=["POST"])
def pupdate():
    try:
        newid = request.form.get("newid")
        oldid = request.form.get("oldid")
        newpname = request.form.get("newpname")
        oldpname = request.form.get("oldpname")
        newdis = request.form.get("newdis")
        olddis = request.form.get("olddis")
        pat = patient.query.filter_by(pid=oldid,pname=oldpname,disease=olddis).first()
        pat.pid = newid
        pat.pname = newpname
        pat.disease = newdis
        db.session.commit()
    except Exception as e:
        print("Couldn't update patient")
        print(e)
    return redirect("/patient")

@app.route("/doctor/delete", methods=["POST"])
def ddelete():
    did = request.form.get("did")
    doc = doctor.query.filter_by(did=did).first()
    db.session.delete(doc)
    db.session.commit()
    return redirect("/doctor")

@app.route("/patient/delete", methods=["POST"])
def pdelete():
    pid = request.form.get("pid")
    pat = patient.query.filter_by(pid=pid).first()
    db.session.delete(pat)
    db.session.commit()
    return redirect("/patient")


if __name__ == "__main__":
   app.run(debug=True)