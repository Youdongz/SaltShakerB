from flask import Flask, request, g, render_template
from Complain import Complaint_List

complaints = Complaint_List()
app = Flask(__name__)


@app.route("/")
def home():
    all_complaints = complaints.get_complaints()
    return render_template('index.html', all_complaints = all_complaints)

@app.route("/complain", methods=["POST"])
def receive_complaint():
    complaints.add_complaint(request.form['complaint'])
    return home()

@app.route("/salt/<complaint_id>")
def salt(complaint_id):
    complaint_id = int(float(complaint_id))
    complaints.salt(complaint_id)
    return home()

@app.route("/pepper/<complaint_id>")
def pepper(complaint_id):
    complaint_id = int(complaint_id)
    complaints.pepper(complaint_id)
    return home()


if __name__ == "__main__":
    app.debug = True
    app.run()
