import hashlib

from sqlalchemy import func

from thuNgan.app import phieu_kham
from thuNgan.models import HoaDon, User, db, ThuocTrongPhieuKham, Thuoc, DonVi, PhieuKham


def load_bills(kw=None):
    query = HoaDon.query
    if kw:
        query = query.filter(HoaDon.id.contains(kw))
    return query.all()


def load_thuoc_trong_hoa_don(hoadon_id):
    if hoadon_id:
        # query = (
        #     db.session.query(PhieuKham.id, Thuoc.TenThuoc, DonVi.TenDonVi, ThuocTrongPhieuKham.LieuLuong, Thuoc.GiaThuoc,
        #                      func.sum(Thuoc.GiaThuoc * ThuocTrongPhieuKham.LieuLuong)).select_from(ThuocTrongPhieuKham)
        #     .join(HoaDon, HoaDon.id == PhieuKham.HoaDon_id)
        #     .join(PhieuKham, PhieuKham.id == ThuocTrongPhieuKham.PhieuKham_id)
        #     .join(Thuoc, Thuoc.id == ThuocTrongPhieuKham.Thuoc_id)
        #     .join(DonVi, DonVi.id == Thuoc.DonVi_id))
        # query.filter(PhieuKham.id == ThuocTrongPhieuKham.PhieuKham_id)
        p = PhieuKham.query.filter(PhieuKham.HoaDon_id.__eq__(hoadon_id))
        query = (
            db.session.query(Thuoc.TenThuoc, DonVi.TenDonVi, ThuocTrongPhieuKham.LieuLuong, Thuoc.GiaThuoc,
                             func.sum(Thuoc.GiaThuoc * ThuocTrongPhieuKham.LieuLuong)).select_from(ThuocTrongPhieuKham)
                .join(Thuoc, Thuoc.id == ThuocTrongPhieuKham.Thuoc_id)
                .join(DonVi, DonVi.id == Thuoc.DonVi_id))
        query.filter(ThuocTrongPhieuKham.PhieuKham_id.__eq__(p.PhieuKham_id))
        return query.all()


def auth_user(phone, password, role=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User.query.filter(User.username.__eq__(phone), User.password.__eq__(password))

    if role:
        u = u.filter(User.user_role.__eq__(role))

    return u.first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def add_user(name, username, password, phone):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User(name=name, username=username, password=password, phone=phone)

    db.session.add(u)
    db.session.commit()
