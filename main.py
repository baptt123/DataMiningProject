import os

import joblib
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler

# Biến toàn cục để lưu mô hình và scaler
global model, scaler
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Thay bằng một chuỗi bí mật để dùng với session
# model=joblib.load('naive_bayes_model.pkl')
# # Khởi tạo mô hình Naive Bayes
# model_test = GaussianNB()
# Routes for each HTML page
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/chart')
def chart():
    # Kết nối tới database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    # Truy vấn dữ liệu bệnh tim
    cursor.execute("""
         SELECT diagnosis, COUNT(*) 
         FROM patients_data_mining
         GROUP BY diagnosis
     """)
    heart_disease_data = cursor.fetchall()

    # Truy vấn các yếu tố rủi ro (Ví dụ: tuổi, huyết áp, cholesterol, đường huyết)
    cursor.execute("""
         SELECT AVG(age), AVG(resting_blood_pressure), AVG(cholesterol), AVG(blood_sugar)
         FROM patients_data_mining
     """)
    risk_factors_data = cursor.fetchall()

    # Đóng kết nối
    conn.close()

    # Tính toán tỷ lệ bệnh tim
    heart_disease_positive = heart_disease_data[0][1] if len(heart_disease_data) > 0 else 0
    heart_disease_negative = heart_disease_data[1][1] if len(heart_disease_data) > 1 else 0

    # Tính toán các yếu tố rủi ro (Ví dụ: tuổi, huyết áp, cholesterol, đường huyết)
    age_risk = risk_factors_data[0][0]
    bp_risk = risk_factors_data[0][1]
    cholesterol_risk = risk_factors_data[0][2]
    glucose_risk = risk_factors_data[0][3]

    # Trả về dữ liệu cho template
    return render_template('chart.html',
                           heart_disease_positive=heart_disease_positive,
                           heart_disease_negative=heart_disease_negative,
                           age_risk=age_risk,
                           bp_risk=bp_risk,
                           cholesterol_risk=cholesterol_risk,
                           glucose_risk=glucose_risk)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/copy')
def copy():
    return render_template('copy.html')

@app.route('/datapatient')
def datapatient():
    # Kết nối tới database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Truy vấn dữ liệu từ database
    query = """
        SELECT age, gender, chest_pain_type, resting_blood_pressure, cholesterol,
               max_heart_rate, exercise_angina, blood_sugar, diagnosis
        FROM patients_data_mining
    """
    cursor.execute(query)

    # Lấy dữ liệu từ kết quả truy vấn
    data = cursor.fetchall()

    # Đóng kết nối
    conn.close()

    # Cung cấp params vào context
    params = {
        'blog_name': 'Heart Failure Prediction System'
    }

    # Trả về template và truyền dữ liệu vào template
    return render_template('datapatient.html', data=data, params=params)


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
def login():
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
        # avatar = request.files['avatar']
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
        # if avatar.filename != '':
        #     avatar_path = os.path.join('static/uploads', avatar.filename)
        #     avatar.save(avatar_path)
        # else:
        #     avatar_path = None

        # Thêm thông tin người dùng vào database
        insert_query = """
        INSERT INTO users (username, password)
        VALUES (%s, %s)
        """
        cursor.execute(insert_query, (username, password))
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
@app.route('/test_export_pdf')
def test_export_pdf():
    return render_template('test_export_pdf.html')
# Cấu hình kết nối MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',  # Thay bằng username MySQL của bạn
    'password': '',  # Thay bằng password MySQL của bạn
    'database': 'data mining project',  # Thay bằng tên database của bạn
}


def preprocess_data(data):
    """Tiền xử lý dữ liệu"""
    # Chuyển đổi dữ liệu phân loại
    data['gender'] = data['gender'].map({'M': 1, 'F': 0})
    data['exercise_angina'] = data['exercise_angina'].map({'Y': 1, 'N': 0})
    return data

def save_to_db(age, gender, chest_pain_type, resting_blood_pressure, cholesterol,
               max_heart_rate, exercise_angina, blood_sugar, diagnosis):
    """Lưu dữ liệu vào cơ sở dữ liệu"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Lấy giá trị ID lớn nhất hiện có và cộng thêm 1
        cursor.execute("SELECT COALESCE(MAX(patient_id), 0) + 1 FROM patients_data_mining")
        new_id = cursor.fetchone()[0]

        query = """
        INSERT INTO patients_data_mining 
        (patient_id, age, gender, chest_pain_type, resting_blood_pressure, cholesterol, 
         max_heart_rate, exercise_angina, blood_sugar, diagnosis)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (new_id, age, gender, chest_pain_type, resting_blood_pressure,
                  cholesterol, max_heart_rate, exercise_angina,
                  blood_sugar, diagnosis)

        cursor.execute(query, values)
        conn.commit()
        print("Dữ liệu đã được lưu vào cơ sở dữ liệu")

    except mysql.connector.Error as err:
        print(f"Lỗi: {err}")
    finally:
        cursor.close()
        conn.close()

def load_data_from_db():
    """Lấy dữ liệu từ cơ sở dữ liệu"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = """
        SELECT age, gender, chest_pain_type, resting_blood_pressure, cholesterol,
               max_heart_rate, exercise_angina, blood_sugar, diagnosis
        FROM patients_data_mining
        """

        cursor.execute(query)
        result = cursor.fetchall()

        data = pd.DataFrame(result, columns=[
            'age', 'gender', 'chest_pain_type', 'resting_blood_pressure',
            'cholesterol', 'max_heart_rate', 'exercise_angina',
            'blood_sugar', 'diagnosis'
        ])

        return data

    except mysql.connector.Error as err:
        print(f"Lỗi: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

def train_model(data):
    """Huấn luyện mô hình Random Forest"""
    try:
        # Tiền xử lý dữ liệu
        data = preprocess_data(data)

        # Chọn đặc trưng
        X = data[['age', 'gender', 'chest_pain_type', 'resting_blood_pressure',
                  'cholesterol', 'max_heart_rate', 'exercise_angina', 'blood_sugar']]
        y = data['diagnosis']

        # Chia tập dữ liệu
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Chuẩn hóa dữ liệu
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Huấn luyện mô hình Random Forest
        model = RandomForestClassifier(n_estimators=100, random_state=42,max_depth=5)
        model.fit(X_train_scaled, y_train)

        # Dự đoán và đánh giá
        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"Độ chính xác của mô hình: {accuracy:.2f}")
        print("\nBáo cáo chi tiết:")
        print(classification_report(y_test, y_pred, zero_division=1))

        # Lưu mô hình và scaler
        os.makedirs('model', exist_ok=True)
        joblib.dump(model, 'model/heart_disease_rf_model.joblib')
        joblib.dump(scaler, 'model/heart_disease_scaler.joblib')

        return model, scaler

    except Exception as e:
        print(f"Lỗi khi huấn luyện mô hình: {e}")
        return None, None

# @app.route('/predict_heart', methods=['GET', 'POST'])
# def predict_heart():
#     try:
#         # Tải mô hình và scaler
#         model = joblib.load('model/heart_disease_rf_model.joblib')
#         scaler = joblib.load('model/heart_disease_scaler.joblib')
#
#         if request.method == 'POST':
#             # Lấy dữ liệu từ form
#             age = int(request.form['age'])
#             gender = request.form['gender']
#             chest_pain_type = int(request.form['chest_pain_type'])
#             resting_blood_pressure = int(request.form['resting_blood_pressure'])
#             cholesterol = int(request.form['cholesterol'])
#             max_heart_rate = int(request.form['max_heart_rate'])
#             exercise_angina = request.form['exercise_angina']
#             blood_sugar = int(request.form['blood_sugar'])
#
#             # Mã hóa các thuộc tính
#             gender_encoded = 1 if gender == 'M' else 0
#             exercise_angina_encoded = 1 if exercise_angina == 'Y' else 0
#
#             # Chuẩn bị dữ liệu để dự đoán
#             features = pd.DataFrame([[
#                 age, gender_encoded, chest_pain_type, resting_blood_pressure,
#                 cholesterol, max_heart_rate, exercise_angina_encoded, blood_sugar
#             ]], columns=[
#                 'age', 'gender', 'chest_pain_type', 'resting_blood_pressure',
#                 'cholesterol', 'max_heart_rate', 'exercise_angina', 'blood_sugar'
#             ])
#
#             # Chuẩn hóa đặc trưng
#             features_scaled = scaler.transform(features)
#
#             # Dự đoán kết quả
#             prediction = model.predict(features_scaled)[0]
#             result = 1 if prediction == 1 else 0
#
#             # Lưu kết quả xuống cơ sở dữ liệu
#             save_to_db(
#                 age=age,
#                 gender=gender,
#                 chest_pain_type=chest_pain_type,
#                 resting_blood_pressure=resting_blood_pressure,
#                 cholesterol=cholesterol,
#                 max_heart_rate=max_heart_rate,
#                 exercise_angina=exercise_angina,
#                 blood_sugar=blood_sugar,
#                 diagnosis=result
#             )
#
#             # Huấn luyện lại mô hình với dữ liệu mới từ DB
#             data = load_data_from_db()
#             train_model(data)
#
#             # Trả kết quả về giao diện
#             return f"""
#                 <h1>Kết quả chẩn đoán: {'Có bệnh' if result == 1 else 'Không bệnh'}</h1>
#                 <a href="/">Quay lại</a>
#             """
#
#     except Exception as e:
#         return f"""
#             <h1>Đã xảy ra lỗi trong quá trình xử lý: {e}</h1>
#             <a href="/">Quay lại</a>
#         """
#
#     # Nếu phương thức là GET, hiển thị form
#     return render_template('Individual-Test.html')
@app.route('/predict_heart', methods=['GET', 'POST'])
def predict_heart():
    try:
        # Tải mô hình và scaler
        model = joblib.load('model/heart_disease_rf_model.joblib')
        scaler = joblib.load('model/heart_disease_scaler.joblib')

        if request.method == 'POST':
            # Lấy dữ liệu từ form
            age = int(request.form['age'])
            gender = request.form['gender']
            chest_pain_type = int(request.form['chest_pain_type'])
            resting_blood_pressure = int(request.form['resting_blood_pressure'])
            cholesterol = int(request.form['cholesterol'])
            max_heart_rate = int(request.form['max_heart_rate'])
            exercise_angina = request.form['exercise_angina']
            blood_sugar = int(request.form['blood_sugar'])

            # Mã hóa các thuộc tính
            gender_encoded = 1 if gender == 'M' else 0
            exercise_angina_encoded = 1 if exercise_angina == 'Y' else 0

            # Chuẩn bị dữ liệu để dự đoán
            features = pd.DataFrame([[
                age, gender_encoded, chest_pain_type, resting_blood_pressure,
                cholesterol, max_heart_rate, exercise_angina_encoded, blood_sugar
            ]], columns=[
                'age', 'gender', 'chest_pain_type', 'resting_blood_pressure',
                'cholesterol', 'max_heart_rate', 'exercise_angina', 'blood_sugar'
            ])

            # Chuẩn hóa đặc trưng
            features_scaled = scaler.transform(features)

            # Dự đoán kết quả
            prediction = model.predict(features_scaled)[0]
            result = 1 if prediction == 1 else 0

            # Lưu kết quả xuống cơ sở dữ liệu
            save_to_db(
                age=age,
                gender=gender,
                chest_pain_type=chest_pain_type,
                resting_blood_pressure=resting_blood_pressure,
                cholesterol=cholesterol,
                max_heart_rate=max_heart_rate,
                exercise_angina=exercise_angina,
                blood_sugar=blood_sugar,
                diagnosis=result
            )

            # Huấn luyện lại mô hình với dữ liệu mới từ DB
            data = load_data_from_db()
            train_model(data)

            # Trả kết quả về dưới dạng JSON
            return jsonify({'message': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Nếu phương thức là GET, hiển thị form
    return render_template('Individual-Test.html')

# Khởi tạo mô hình ban đầu khi ứng dụng chạy
def init_model():
    data = load_data_from_db()
    train_model(data)

# Gọi hàm khởi tạo mô hình
init_model()

# Chạy ứng dụng Flask
if __name__ == '__main__':
    app.run(debug=True)


