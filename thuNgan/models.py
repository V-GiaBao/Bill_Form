from sqlalchemy import Integer, Boolean, Column, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from enum import Enum as RoleEnum
from flask_login import UserMixin
from thuNgan import app
from thuNgan import db

#bao model

class Bills(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tienKham = Column(Integer, default=0)
    tienThuoc = Column(Integer, default=0)
    tinhTrang = Column(Boolean, default=False)
class PhieuKham(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngay = Column(DateTime, default=0)

# Khong dùng enum chỗ đơn vị
class Thuoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenThuoc = Column(Integer, default=0)
    donVi = Column(String(255), default="0")
    giaThuoc = Column(Integer, default="0")


# dai model
class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2  # Patient
    DOCTOR = 3
    NURSE = 4


class User(db.Model, UserMixin):
    id_patient = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    arrangement = relationship('Arrangement', backref='user', lazy=True)  # Backref tới bảng Arrangement

class ArrList(db.Model):
    id_arr_list = Column(Integer, primary_key=True, autoincrement=True)
    appointment_date = Column(DateTime, nullable=False)
    patient_quantity = Column(Integer, nullable=False)
    description = Column(String(255), nullable=True)
    arrangement = relationship('Arrangement', backref='arrlist', lazy=True)

class Arrangement(db.Model):
    id_arrangement = Column(Integer, primary_key=True, autoincrement=True)
    id_arr_list = Column(Integer, ForeignKey(ArrList.id_arr_list), nullable=True)
    id_patient = Column(Integer, ForeignKey(User.id_patient), nullable=False)  # Khóa ngoại tham chiếu User.id_patient
    id_nurse = Column(Enum(UserRole), default=UserRole.NURSE, nullable=True) # nullable
    appointment_date = Column(DateTime, nullable=False)
    description = Column(String(255), nullable=True)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        import hashlib

        # users = [{
        #     "name": "nguyen dai nurse",
        #     "username": "nurse",
        #     "password": str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #     "phone": "0903214124",
        #     "user_role": UserRole.NURSE
        # }, {
        #     "name": "nguyen dai",
        #     "username": "patient123",
        #     "password": str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #     "phone": "0903214124",
        #     "user_role": UserRole.USER
        # }]
        # delete all users, arr_lists, arrangements before adding
        # db.session.query(Arrangement).delete()
        # db.session.query(ArrList).delete()
        # db.session.query(User).delete()

        # adding users session
        # for u in users:
        #     user = User(**u)
        #     db.session.add(user)
        # db.session.commit()

#         bills = [{
#             "tienKham": 17000000,
#             "tienThuoc": 27000000,
#         }, {
#             "tienKham": 37000000,
#             "tienThuoc": 47000000,
#         }, {
#             "tienKham": 57000000,
#             "tienThuoc": 67000000,
#         }, {
#             "tienKham": 77000000,
#             "tienThuoc": 87000000,
#         }, {
#             "tienKham": 97000000,
#             "tienThuoc": 18000000,
#         }]
#         for b in bills:
#             bill = Bills(**b)
#             db.session.add(bill)
#
#     db.session.commit()
# #
