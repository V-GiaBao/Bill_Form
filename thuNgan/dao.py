import hashlib

from sqlalchemy import func

from thuNgan.models import HoaDon, User, db, ThuocTrongPhieuKham, Thuoc, DonVi, PhieuKham, QuyDinh


def load_bills(kw=None):
    query = HoaDon.query
    if kw:
        query = query.filter(HoaDon.id.contains(kw))
    return query.all()


def them_phieu_kham(ngay, benh):
    tienKham = QuyDinh.query.get(2).GiaTri
    hd = HoaDon(TienThuoc=0, TienKham=tienKham, TinhTrangThanhToan=False)
    db.session.add(hd)
    db.session.commit()
    pk = PhieuKham(NgayLapPhieu=ngay, LoaiBenh=benh, HoaDon_id=hd.id)
    db.session.add(pk)
    db.session.commit()
    return pk.id


def cap_nhat_tien_thuoc(phieu_id, tien):
    phieu = PhieuKham.query.filter(PhieuKham.id==phieu_id).first()
    hoadon = HoaDon.query.get(phieu.HoaDon_id)
    hoadon.TienThuoc = tien
    db.session.commit()


def tao_thuoc_trong_phieu_kham(ten, SoLuong, CachDung, phieu_id):
    thuoc = Thuoc.query.filter(Thuoc.TenThuoc.contains(ten)).first()
    DrugInReport = ThuocTrongPhieuKham(Thuoc_id=thuoc.id, PhieuKham_id=phieu_id, LieuLuong=SoLuong,
                                       CachDung=CachDung)
    db.session.add(DrugInReport)
    db.session.commit()
    return float(thuoc.GiaThuoc * SoLuong)




def load_thuoc():
    return Thuoc.query.all()


def load_thuoc_trong_hoa_don(hoadon_id):
    if hoadon_id:
        p = PhieuKham.query.filter(PhieuKham.HoaDon_id.__eq__(hoadon_id))

        query = (
            db.session.query(Thuoc.TenThuoc, DonVi.TenDonVi, ThuocTrongPhieuKham.LieuLuong, Thuoc.GiaThuoc,
                             func.sum(Thuoc.GiaThuoc * ThuocTrongPhieuKham.LieuLuong))
            .join(Thuoc, Thuoc.id == ThuocTrongPhieuKham.Thuoc_id)
            .join(DonVi, DonVi.id == Thuoc.DonVi_id)
            .group_by(Thuoc.TenThuoc, DonVi.TenDonVi, ThuocTrongPhieuKham.LieuLuong)
            .filter(ThuocTrongPhieuKham.PhieuKham_id.__eq__(hoadon_id)))
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
