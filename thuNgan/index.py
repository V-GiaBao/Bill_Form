
from flask import render_template, request, redirect
from flask_login import login_user, logout_user


import dao
from thuNgan import login, app



@app.route('/')
def index():
    return render_template('mainPage.html')


@app.route("/bills/<int:bill_id>", methods=['GET', 'POST'])
def bill_detail(bill_id):
    thuocs = dao.load_thuoc_trong_hoa_don(bill_id)
    return render_template('billDetail.html', thuocs=thuocs)


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


@app.route("/phieuKham", methods=['GET', 'POST'])
def phieu_kham():
    thuoc = dao.load_thuoc()

    if request.method.__eq__('POST'):
        tong_thuoc = float(0)
        tien_thuoc = float(0)
        ngay = request.form.get('dateForm')
        benh = request.form.get('disease-txt')
        data = request.form.copy()
        # grouped_data = [data_list[i:i + 3] for i in range(0, len(data_list), 3)]
        del data['docName']
        del data['sdt']
        del data['dateForm']
        del data['disease-txt']
        data_list = list(data.items())
        grouped_data = [data_list[i:i + 3] for i in range(0, len(data_list), 3)]
        id = int(dao.them_phieu_kham(ngay, benh))
        for group in grouped_data:

            for key, value in group:
                if 'medicine' in key:
                    medicine = value
                if 'med-instruct' in key:
                    instruct = value
                if 'med-number' in key:
                    num = float(value)
                    tien_thuoc = dao.tao_thuoc_trong_phieu_kham(medicine, num, instruct, id)
                    tong_thuoc = tien_thuoc + tong_thuoc

        # for key, value in data.items():
        #
        #     if 'medicine' in key:
        #         medicine = value
        #     if 'med-instruct' in key:
        #         instruct = value
        #     if 'med-number' in key:
        #         num = float(value)
        #         tien_thuoc= dao.tao_thuoc_trong_phieu_kham(medicine, num, instruct,id)

        dao.cap_nhat_tien_thuoc(id, tong_thuoc)
    return render_template('phieuKham1.html',thuocs=thuoc)


@login.user_loader
def get_user_by_id(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run()
