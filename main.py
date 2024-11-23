from flask import Flask, render_template, request, redirect

from app.db.base import create_db, Session
from app.db.models import Pizza, Employee, Position


app = Flask(__name__, template_folder="app/templates")


@app.get("/")
def index():
    with Session() as session:
        employees = session.query(Employee).all()
        return render_template("index.html", employees=employees)
    

@app.route("/add_employee/", methods=["GET", "POST"])
def add_employee():
    with Session() as session:
        positions = session.query(Position).all()

        if request.method == "POST":
            name = request.form.get("name")
            position_id = request.form.get("position_id")
            employee = Employee(name=name, position_id=position_id)
            session.add(employee)
            session.commit()
            return redirect("/")

        return render_template("add_employee.html", positions=positions)
    

@app.route("/add_position/", methods=["GET", "POST"])
def add_position():
    if request.method == "POST":
        with Session() as session:
            name = request.form.get("name")
            position = Position(name=name)
            session.add(position)
            session.commit()
            return redirect("/")

    return render_template("add_position.html")


if __name__ == "__main__":
    app.run(debug=True, port=90)