from flask import request, Blueprint
from .auth import Create_new_user, Login
from .services import get_all_staff, get_one_staff, update_staff, delete_staff, get_all_std, get_one_std, update_std, delete_std, create_new_std


routes = Blueprint('routes', __name__)


# staff endpoints
@routes.post("/api/v1/staff/createnew")
def createNew():
    data = request.get_json()
    return Create_new_user(data)

@routes.post("/api/v1/staff/login")
def login():
    data = request.get_json()
    return Login(data)

@routes.get("/api/v1/staff/getall")
def get_all_users():
    return get_all_staff()

@routes.get("/api/v1/staff/getone/<int:id>")
def get_one_user(id:int):
   return get_one_staff(id)

@routes.put("/api/v1/staff/update/<int:id>")
def updata_staff_user(id):
    data = request.get_json()
    return update_staff(id,data)

@routes.delete("/api/v1/staff/delete/<int:id>")
def delete_staff_user(id):
    return delete_staff(id)

#student Endpoints

@routes.post("/api/v1/student/createnew")
def create_new_student():
    data = request.get_json()
    return create_new_std(data)

@routes.get("/api/v1/student/getall")
def get_all_student():
    return get_all_std()


@routes.get("/api/v1/student/getone/<int:id>")
def get_one_student(id:int):
    return get_one_std(id)


@routes.put("/api/v1/student/update/<int:id>")
def update_student(id:int):
    data = request.get_json()
    return update_std(id, data)


@routes.delete("/api/v1/student/delete/<int:id>")
def delete_student(id:int):
    return delete_std(id)
