from flask import render_template, request, redirect
from flask_login import login_user, logout_user

import dao
from thuNgan import login, app


@app.route('/')
def index():
    return render_template('mainPage.html')


@app.route("/billDetail", methods=['GET', 'POST'])
def bill_detail():
    return render_template('billDetail.html',
                           thuocs=dao.load_thuoc_trong_hoa_don(1))


@app.route('/bills', methods=['GET', 'POST'])
def bill_process():
    kw = request.args.get('billID')
    bills = dao.load_bills(kw=kw)
    return render_template('thuNgan2.html', bills=bills)


@app.route("/login", methods=['get', 'post'])
def login_process():
    if request.method.__eq__('POST'):
        phone = request.form.get('phone')
        password = request.form.get('password')

        u = dao.auth_user(phone=phone, password=password)
        if u:
            login_user(u)
            return redirect('/')

    return render_template('login.html')


@app.route("/register", methods=['get', 'post'])
def register_process():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            data = request.form.copy()
            del data['confirm']

            dao.add_user(**data)
            return redirect('/login')
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)


@app.route("/logout")
def logout_process():
    logout_user()
    return redirect('/login')


@app.route("/dangKyLich")
def dang_ky_lich():
    return render_template('dangKyLich.html')


@app.route("/phieuKham")
def phieu_kham():
    # if request.method.__eq__('POST'):
    #     NgayLapPhieu = request.form.get('dateForm')
    #     # ThuocTrongPhieuKhams =

    return render_template('phieuKham1.html')


@login.user_loader
def get_user_by_id(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run()
