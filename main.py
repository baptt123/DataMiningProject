import os

from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Thay bằng một chuỗi bí mật để dùng với session

# Routes for each HTML page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/chart')
def chart():
    return render_template('chart.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/copy')
def copy():
    return render_template('copy.html')

@app.route('/datapatient')
def datapatient():
    return render_template('datapatient.html')

@app.route('/dataset_test')
def dataset_test():
    return render_template('Dataset_test.html')

@app.route('/description')
def description():
    return render_template('description.html')

@app.route('/forgotpassword')
def forgot_password():
    return render_template('forgotpassword.html')

@app.route('/individual_test')
def individual_test():
    return render_template('Individual-Test.html')

@app.route('/layout')
def layout():
    return render_template('layout.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Kết nối tới database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Kiểm tra thông tin người dùng
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            # Đăng nhập thành công
            session['username'] = username
            flash('Đăng nhập thành công', 'success')
            return redirect(url_for('index'))
        else:
            # Đăng nhập thất bại
            flash('Thông tin đăng nhập không đúng', 'danger')
            return redirect(url_for('login_page'))

    return render_template('login.html')

# Đăng ký
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        avatar = request.files['avatar']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Kiểm tra mật khẩu nhập lại
        if password != confirm_password:
            flash("Mật khẩu không khớp", "danger")
            return redirect(url_for('register'))

        # Kết nối tới database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Kiểm tra xem username đã tồn tại chưa
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user:
            # Username đã tồn tại
            flash("Tài khoản đã tồn tại", "danger")
            cursor.close()
            conn.close()
            return redirect(url_for('register'))

        # Lưu file avatar
        if avatar.filename != '':
            avatar_path = os.path.join('static/uploads', avatar.filename)
            avatar.save(avatar_path)
        else:
            avatar_path = None

        # Thêm thông tin người dùng vào database
        insert_query = """
        INSERT INTO users (username, password, avatar_path)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (username, password, avatar_path))
        conn.commit()

        cursor.close()
        conn.close()

        flash("Đăng ký thành công, hãy đăng nhập", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

# Đăng xuất
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Bạn đã đăng xuất', 'info')
    return redirect(url_for('login_page'))

# Cấu hình kết nối MySQL
db_config = {
    'host': 'localhost',
    'user': 'your_username',  # Thay bằng username MySQL của bạn
    'password': 'your_password',  # Thay bằng password MySQL của bạn
    'database': 'your_database',  # Thay bằng tên database của bạn
}

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
