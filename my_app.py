
from flask import Flask, request, jsonify
import pyrebase
app = Flask(__name__)


firebaseConfig =  {
  'apiKey': "AIzaSyAPRJE2s91QMbUw6Y2GbFKhgE5b9GvbJtE",
  'authDomain': "kurtproject-5029d.firebaseapp.com",
  'databaseURL': "https://kurtproject-5029d-default-rtdb.firebaseio.com",
  'projectId': "kurtproject-5029d",
  'storageBucket': "kurtproject-5029d.appspot.com",
  'messagingSenderId': "487114580082",
  'appId': "1:487114580082:web:779d38a64a6bda6924a2eb",
  'measurementId': "G-2FW5PRV932"
}
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

@app.route("/employees")
def all_users():
    try:
        vals = db.child("Employees").get()
        lists = []
        for val in vals.each():
            dicts = val.val()
            dicts['empid'] = val.key()
            lists.append(dicts)
        return jsonify(lists), 200
    except Exception as e:
        error_message = f"Error fetching data: {str(e)}"
        return jsonify({"error": error_message}), 500

@app.route("/employees/<empid>")
def get_user(empid):
    try:
        val = db.child("Employees").child(empid).get().val()
        val["empid"] = empid
        return jsonify(val), 200
    except TypeError:  
        error_message = f"No employee with empid {empid} found"
        return jsonify({"error": error_message}), 404
    
@app.route("/employees/<empid>", methods=["DELETE", "PUT"])
def change_employee(empid):
    if(request.method == "DELETE"):
        try:
            val = db.child("Employees").child(empid).get().val()
            if val is None:
                return jsonify({"error": f"No employee with empid {empid} found"}), 404
            db.child("Employees").child(empid).remove()
            return jsonify({"message": f"Employee with empid {empid} deleted", "deleted_employee": val}), 200

        except Exception as e:
            return jsonify({"error": f"Error deleting employee: {str(e)}"}), 500
    elif (request.method == "PUT"):
        try:
            data = request.json
            if "lastname" not in data or "firstname" not in data or "hired_date" not in data: 
                return jsonify({"error": "Some parameters are missing"}), 400
            
            lastname = data['lastname']
            firstname = data['firstname']
            hired_date = data['hired_date']
            val = db.child("Employees").child(empid).get().val()
            if val is  None:
                return jsonify({"error": f"No Employee with empid {empid} found"}), 404
            details = {
                'lastname': lastname, 
                'firstname': firstname, 
                'hired_date': hired_date
            }
            db.child("Employees").child(empid).update(details)
            return jsonify(details), 200
        except Exception as e:
            return jsonify({"error": f"Error updating employee: {str(e)}"}), 500
    
@app.route("/employees", methods=["POST"])
def add_employee():
    try:
        if(request.method == "POST"):
            data = request.json
            if "lastname" not in data or "firstname" not in data or "hired_date" not in data or "empid" not in data: 
                print(lastname, firstname, hired_date, empid)
                return jsonify({"error": "Some parameters are missing"}), 400
            empid  = data['empid']
            lastname = data['lastname']
            firstname = data['firstname']
            hired_date = data['hired_date']
            val = db.child("Employees").child(empid).get().val()
            if val is not None:
                return jsonify({"error": f"Employee with empid {empid} found"}), 404
            details = {
                'lastname': lastname, 
                'firstname': firstname, 
                'hired_date': hired_date
            }
            db.child("Employees").child(empid).set(details)
            return jsonify(details), 200

    except Exception as e:
        return jsonify({"error": f"Error creating employee: {str(e)}"}), 500



#GET
#POST
#PUT
#DELETE 

if __name__ == "__main__":
    app.run(debug = True)