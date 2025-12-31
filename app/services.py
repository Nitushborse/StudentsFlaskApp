from .models import db, Staff, Student
from flask import jsonify
import bcrypt
from .check_token import token_required

@token_required
# get all staff list
def get_all_staff():
    users = Staff.query.all()
    result = [
        {
            "id":user.id,
            "name": user.name,
            "email": user.email,
            "createdAt": user.createdAt.isoformat(),  # Formatting datetime for JSON
            "isAdmin": user.isAdmin
        }
        for user in users
    ]
    return jsonify(result), 200

@token_required
# get staff by id
def get_one_staff(id):
    staff_member = Staff.query.get(id)
    
    if not staff_member:
        return jsonify({"error":"user not found"}), 404
    
    result = {
        "id": staff_member.id,
        "name": staff_member.name,
        "email": staff_member.email,
        "createdAt": staff_member.createdAt,
        "isAdmin": staff_member.isAdmin
    }
    
    # Ensure the order explicitly
    ordered_result = {key: result[key] for key in ["id","name", "email", "createdAt", "isAdmin"]}

    return jsonify(ordered_result), 200

@token_required
# update staff
def update_staff(id, data):
    staff_member = Staff.query.get(id)
    if not staff_member:
         return jsonify({"error":"user not found"}), 404
    
    # Update fields (add any additional validation as needed)
    staff_member.name = data.get('name', staff_member.name)
    staff_member.email = data.get('email', staff_member.email)
    staff_member.isAdmin = data.get('isAdmin', staff_member.isAdmin)

    if 'password' in data:
        password = data.get('password')
        staff_member.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    db.session.commit()

    return jsonify({
        "message": "Staff member updated successfully",
        "user": staff_member.to_dict()
    }), 200

@token_required
# delete staff
def delete_staff(id):
    staff_member = Staff.query.get(id)
    
    if not staff_member:
        return jsonify({"error":"user not found"}), 404
    

    # Delete the staff member
    db.session.delete(staff_member)
    db.session.commit()

    return jsonify({
        "message": "Staff member deleted successfully"
    }), 200


@token_required
# create new student
def create_new_std(data):
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
# get all students list
def get_all_std():
    students = Student.query.all()
    students_list = [student.to_dict() for student in students]
    return jsonify(students_list), 200

@token_required
# get one student by id
def get_one_std(id):
    student = Student.query.get(id)

    if not student:
        return jsonify({"error": "student not found"}), 404
    
    return jsonify(student.to_dict()), 200

@token_required
# update student data
def update_std(id, data):
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
# delete student data
def delete_std(id):
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