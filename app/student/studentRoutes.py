from flask import request, jsonify, Blueprint
from app.utils.checkToken import token_required
from app.models import Student, db


student_bp = Blueprint("student", __name__)


@token_required
@student_bp.post("/student/createnew")
def create_new_student():
    data = request.get_json()
    if not data:
        return jsonify({"error": "missing request body"}), 400
    
    required_fields = ["roll_no", "firstname", "middlename", "lastname", "age", "email", "mobileno", "course", "year"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
        
    roll_no = data['roll_no']
    firstname = data['firstname']
    middlename = data['middlename']
    lastname = data['lastname']
    age = data['age']
    email = data['email']
    mobileno = data['mobileno']
    course = data['course']
    year = data['year']

    if Student.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    new_student = Student(
        roll_no = roll_no,
        firstname = firstname,
        middlename = middlename,
        lastname = lastname,
        age = age,
        email = email,
        mobileno = mobileno,
        course = course,
        year = year
    )

    db.session.add(new_student)
    db.session.commit()

    return jsonify({
        "message":"Student created successfully",
        "user": new_student.to_dict()
    }), 201




@token_required
@student_bp.get("/student/getall")
def get_all_students():
    student = Student.query.get(id)

    if not student:
        return jsonify({"error": "student not found"}), 404
    
    return jsonify(student.to_dict()), 200




@student_bp.put("/student/getone/<int:id>")
def get_one_student(id):
    student = Student.query.get(id)

    if not student:
        return jsonify({"error": "student not found"}), 404
    
    return jsonify(student.to_dict()), 200





@token_required
@student_bp.put("/student/update/<int:id>")
def update_student(id):
    data = request.get_json()
    student = Student.query.get(id)

    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    # Update the student's attributes from the data
    student.roll_no = data.get('roll_no', student.roll_no)
    student.firstname = data.get('firstname', student.firstname)
    student.middlename = data.get('middlename', student.middlename)
    student.lastname = data.get('lastname', student.lastname)
    student.age = data.get('age', student.age)
    student.email = data.get('email', student.email)
    student.mobileno = data.get('mobileno', student.mobileno)
    student.course = data.get('course', student.course)
    student.year = data.get('year', student.year)

    # Commit the changes to the database
    try:
        db.session.commit()
        return jsonify(student.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    



    
@token_required
@student_bp.delete("/student/delete/<int:id>")
def delete_student(id):
    student = Student.query.get(id)

    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Student deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


