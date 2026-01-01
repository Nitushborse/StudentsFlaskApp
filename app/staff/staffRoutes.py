import bcrypt
from flask import request, jsonify, Blueprint
from app.utils.checkToken import token_required
from app.models import Staff, db


staff_bp = Blueprint("staff",  __name__)




@staff_bp.get("/staff/getall")
@token_required
def get_all_staff():
    users = Staff.query.all()
    result = [
        {
            "id":user.id,
            "name": user.name,
            "email": user.email,
            "createdAt": user.createdAt.isoformat(),    
            "isAdmin": user.isAdmin
        }
        for user in users
    ]
    return jsonify(result), 200



@staff_bp.get("/staff/getone/<int:id>")
@token_required
def get_one_staff(id:int):
    staff_member = Staff.query.get(id)
    
    if not staff_member:
        return jsonify({"error":"user not found"}), 404

    result = {
        "id": staff_member.id,
        "name": staff_member.name,
        "email": staff_member.email,
        "createdAt": staff_member.createdAt.isoformat(),
        "isAdmin": staff_member.isAdmin
    }

    # Ensure the order explicitly
    # ordered_result = {key: result[key] for key in ["id","name", "email", "createdAt", "isAdmin"]}
    return jsonify(result), 200
    # return jsonify(ordered_result), 200


@staff_bp.put("/staff/update/<int:id>")
@token_required
def updata_staff(id):
    data = request.get_json()
    staff_member = Staff.query.get(id)

    if request.user.get("isAdmin") == 0:
        return jsonify({"error": "Admin access required"}), 403
    
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



@staff_bp.delete("/staff/delete/<int:id>")
@token_required
def delete_staff_user(id):
    staff_member = Staff.query.get(id)
    
    if request.user.get("isAdmin") == 0:
        return jsonify({"error": "Admin access required"}), 403

    if not staff_member:
        return jsonify({"error":"user not found"}), 404

    
    # Delete the staff member
    db.session.delete(staff_member)
    db.session.commit()

    return jsonify({
        "message": "Staff member deleted successfully"
    }), 200
