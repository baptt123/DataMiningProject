import os

import joblib
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, f1_score, \
    confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler

# Định nghĩa danh sách các route cần kiểm tra quyền truy cập
restricted_routes = ['/chart', '/exportpdf', '/datapatient']
# Biến toàn cục để lưu mô hình và scaler
global model, scaler
app = Flask(__name__,static_folder='static')
app.secret_key = 'your_secret_key'  # Thay bằng một chuỗi bí mật để dùng với session


@app.before_request
def check_admin():
    # Lấy URL hiện tại và kiểm tra xem nó có trong danh sách restricted_routes không
    if request.path in restricted_routes:
        # Kiểm tra nếu session có chứa username và role là admin
        if 'username' not in session or session.get('role') != 'admin':
            flash('Bạn phải có quyền admin hoặc phải đăng nhập mói được phép truy cập', 'danger')
            return redirect(url_for('role'))  # Chuyển hướng về trang đăng nhập
        if 'username' not in session or session.get('role') =='user':
            return redirect(url_for('index'))




# # Phân quyền đăng nhập
@app.route('/role', methods=['GET'])
def role():
    return render_template('role.html')


# Routes for each HTML page
@app.route('/')
def welcome():
    return render_template('role.html')


@app.route('/index')
def index():
    # if 'username' not in session:
    #     flash('Vui lòng đăng nhập trước.', 'warning')
    #     return redirect(url_for('login'))
    return render_template('index.html')


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

    # Phân cụm bằng KMeans
    cursor.execute("""
          SELECT age, cholesterol 
          FROM patients_data_mining
      """)
    clustering_data = cursor.fetchall()

    cursor.execute("""
             SELECT age, resting_blood_pressure, cholesterol
             FROM patients_data_mining
             LIMIT 50
         """)
    correlation_data = cursor.fetchall()

    conn.close()

    # Tiền xử lý dữ liệu phân cụm
    from sklearn.cluster import KMeans
    import numpy as np

    clustering_array = np.array(clustering_data)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(clustering_array)
    labels = kmeans.labels_

    # Tạo danh sách cụm
    cluster_1 = [{"x": int(clustering_array[i][0]), "y": int(clustering_array[i][1])}
                 for i in range(len(labels)) if labels[i] == 0]
    cluster_2 = [{"x": int(clustering_array[i][0]), "y": int(clustering_array[i][1])}
                 for i in range(len(labels)) if labels[i] == 1]
    cluster_3 = [{"x": int(clustering_array[i][0]), "y": int(clustering_array[i][1])}
                 for i in range(len(labels)) if labels[i] == 2]

    # Tính toán tỷ lệ bệnh tim
    heart_disease_positive = heart_disease_data[0][1] if len(heart_disease_data) > 0 else 0
    heart_disease_negative = heart_disease_data[1][1] if len(heart_disease_data) > 1 else 0

    # Tính toán các yếu tố rủi ro
    age_risk = risk_factors_data[0][0]
    bp_risk = risk_factors_data[0][1]
    cholesterol_risk = risk_factors_data[0][2]
    glucose_risk = risk_factors_data[0][3]

    # Chuẩn bị dữ liệu cho biểu đồ tương quan
    correlation_age_bp_data = [{"x": age, "y": bp} for age, bp, _ in correlation_data]
    correlation_age_cholesterol_data = [{"x": age, "y": cholesterol} for age, _, cholesterol in correlation_data]
    correlation_bp_cholesterol_data = [{"x": bp, "y": cholesterol} for _, bp, cholesterol in correlation_data]

    # Trả về dữ liệu cho template
    return render_template('chart.html',
                           heart_disease_positive=heart_disease_positive,
                           heart_disease_negative=heart_disease_negative,
                           age_risk=age_risk,
                           bp_risk=bp_risk,
                           cholesterol_risk=cholesterol_risk,
                           glucose_risk=glucose_risk,
                           cluster_1=cluster_1,
                           cluster_2=cluster_2,
                           cluster_3=cluster_3,
                           correlation_age_bp_data=correlation_age_bp_data,
                           correlation_age_cholesterol_data=correlation_age_cholesterol_data,
                           correlation_bp_cholesterol_data=correlation_bp_cholesterol_data)


@app.route('/contact')
def contact():
    return render_template('contact.html')


# @app.route('/copy')
# def copy():
#     return render_template('copy.html')

@app.route('/datapatient')
def datapatient():
    # Kết nối tới database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Truy vấn dữ liệu từ database
    query = """
         SELECT patient_id, fullname, age, gender, chest_pain_type, resting_blood_pressure, cholesterol,
                max_heart_rate, exercise_angina, blood_sugar, shortness_of_breath, fatigue, dizziness,
                chest_pain_frequency, heart_rate_variability, pulse_pressure, ldl_hdl_ratio, stress_level,
                family_history, diagnosis
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
# @app.route('/dataset_test')
# def dataset_test():
#     return render_template('Dataset_test.html')

@app.route('/description')
def description():
    return render_template('description.html')


@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgot_password():
    password = None  # Biến để lưu mật khẩu tìm thấy (nếu có)

    if request.method == 'POST':
        username = request.form['username']

        # Kết nối tới database để tìm kiếm username
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "SELECT password FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            password = user[0]  # Lấy mật khẩu từ kết quả truy vấn
        else:
            flash("Username not found in the system.", "danger")

    return render_template('forgotpassword.html', password=password)


@app.route('/predict')
def predict():
    return render_template('predict.html')


@app.route('/layout')
def layout():
    return render_template('layout.html')


# @app.route('/login', methods=['GET', 'POST'])
# #Dang nhap
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#
#         # Kết nối tới database
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor()
#
#         # Kiểm tra thông tin người dùng
#         query = "SELECT * FROM users WHERE username = %s AND password = %s"
#         cursor.execute(query, (username, password))
#         user = cursor.fetchone()
#
#         cursor.close()
#         conn.close()
#
#         if user:
#             # Đăng nhập thành công
#             session['username'] = username
#             flash('Đăng nhập thành công', 'success')
#             return redirect(url_for('index'))
#         else:
#             # Đăng nhập thất bại
#             flash('Thông tin đăng nhập không đúng', 'danger')
#             return redirect(url_for('login'))
#
#     return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Kết nối tới database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Trả về kết quả dưới dạng từ điển

        # Kiểm tra thông tin người dùng và lấy role
        query = "SELECT username, role FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            # Đăng nhập thành công, lưu thông tin vào session
            session['username'] = user['username']
            session['role'] = user['role']
            flash('Đăng nhập thành công', 'success')
            return redirect(url_for('index'))
        else:
            # Đăng nhập thất bại
            flash('Thông tin đăng nhập không đúng', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


# Kiểm tra trước khi vào trang thông tin bệnh nhân ở phía admin
# @app.before_request
# def restrict_admin_page():
#     if request.endpoint == 'admin' and ('username' not in session or session.get('role') != 'admin'):
#         flash('Bạn không có quyền truy cập trang admin', 'danger')
#         return redirect(url_for('login'))
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
        INSERT INTO users (username, password,role)
        VALUES (%s, %s,%s)
        """
        cursor.execute(insert_query, (username, password, 'user'))
        conn.commit()

        cursor.close()
        conn.close()

        flash("Đăng ký thành công, hãy đăng nhập", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


# @app.route('/upload')
# def upload():
#     return render_template('upload.html')

# Đăng xuất
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Bạn đã đăng xuất', 'info')
    return redirect(url_for('login'))


# @app.route('/exportpdf')
# def test_export_pdf():
#     try:
#         # Kết nối database
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor()
#
#         # Truy vấn dữ liệu
#         query = """
#             SELECT
#                 patient_id,
#                 age,
#                 CASE
#                     WHEN gender = 'M' THEN 'Nam'
#                     WHEN gender = 'F' THEN 'Nữ'
#                     ELSE gender
#                 END as gender,
#                 chest_pain_type,
#                 resting_blood_pressure,
#                 cholesterol,
#                 max_heart_rate,
#                 CASE
#                     WHEN exercise_angina = 'Y' THEN 'Có'
#                     WHEN exercise_angina = 'N' THEN 'Không'
#                     ELSE exercise_angina
#                 END as exercise_angina,
#                 blood_sugar,
#                 CASE
#                     WHEN diagnosis = 1 THEN 'Có bệnh'
#                     WHEN diagnosis = 0 THEN 'Không bệnh'
#                     ELSE CAST(diagnosis AS CHAR)
#                 END as diagnosis
#             FROM patients_data_mining
#             ORDER BY patient_id
#         """
#         cursor.execute(query)
#         data = cursor.fetchall()
#
#         cursor.close()
#         conn.close()
#
#         return render_template('exportpdf.html', data=data)
#
#     except Exception as e:
#         return f"Lỗi khi lấy dữ liệu: {str(e)}"
# Lấy dữ liệu từ cơ sở dữ liệu
def fetch_data_from_db():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = """
            SELECT 
                patient_id,
                age,
                CASE 
                            WHEN gender = 'M' THEN 'Nam'
                            WHEN gender = 'F' THEN 'Nữ'
                            ELSE gender
                        END as gender,
                
                chest_pain_type,
                resting_blood_pressure,
                cholesterol,
                max_heart_rate,
                exercise_angina,
                blood_sugar,
                shortness_of_breath,
                fatigue,
                dizziness,
                chest_pain_frequency,
                heart_rate_variability,
                pulse_pressure,
                ldl_hdl_ratio,
                stress_level,
                family_history,
                diagnosis
            FROM patients_data_mining
            ORDER BY patient_id
        """
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except Exception as e:
        raise Exception(f"Lỗi khi load dữ liệu từ db: {str(e)}")

# Chuẩn bị đặc trưng cho từng bệnh nhân và dự đoán
# Cập nhật hàm chuẩn bị dữ liệu để phân loại thành 3 cấp độ
def prepare_features(row):
    # Giả sử bạn đã cập nhật mô hình để phân loại thành 3 lớp
    model = joblib.load('model/heart_disease_rf_model.joblib')
    scaler = joblib.load('model/heart_disease_scaler.joblib')

    # Các tham số khác
    (patient_id, age, gender, chest_pain_type, resting_blood_pressure, cholesterol,
     max_heart_rate, exercise_angina, blood_sugar, shortness_of_breath, fatigue,
     dizziness, chest_pain_frequency, heart_rate_variability, pulse_pressure,
     ldl_hdl_ratio, stress_level, family_history, diagnosis) = row #Unpack the row

    gender = 1 if gender == 'Nam' else 0
    exercise_angina = 1 if exercise_angina == 'Có' else 0
    family_history = 1 if family_history == 'Y' else 0
    shortness_of_breath = {'None': 0, 'Mild': 1, 'Moderate': 2, 'Severe': 3}[shortness_of_breath]
    fatigue = {'Never': 0, 'Sometimes': 1, 'Often': 2}[fatigue]
    dizziness = {'Never': 0, 'Occasional': 1, 'Often': 2}[dizziness]

    # Mã hóa các chỉ số
    features = pd.DataFrame([[age, gender, chest_pain_type,
                              resting_blood_pressure, cholesterol,
                              max_heart_rate, exercise_angina, blood_sugar,
                              shortness_of_breath, fatigue, dizziness,
                              chest_pain_frequency, heart_rate_variability, pulse_pressure,
                              ldl_hdl_ratio, stress_level, family_history]],
                            columns=['age', 'gender', 'chest_pain_type',
                                     'resting_blood_pressure', 'cholesterol',
                                     'max_heart_rate', 'exercise_angina', 'blood_sugar',
                                     'shortness_of_breath', 'fatigue', 'dizziness',
                                     'chest_pain_frequency', 'heart_rate_variability', 'pulse_pressure',
                                     'ldl_hdl_ratio', 'stress_level', 'family_history'])

    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]  # Dự đoán cấp độ rủi ro
    return {
        'patient_id': patient_id,
        'age': age,
        'gender': gender,
        'chest_pain_type': chest_pain_type,
        'resting_blood_pressure': resting_blood_pressure,
        'cholesterol': cholesterol,
        'max_heart_rate': max_heart_rate,
        'exercise_angina': exercise_angina,
        'blood_sugar': blood_sugar,
        'shortness_of_breath': shortness_of_breath,
        'fatigue': fatigue,
        'dizziness': dizziness,
        'chest_pain_frequency': chest_pain_frequency,
        'heart_rate_variability': heart_rate_variability,
        'pulse_pressure': pulse_pressure,
        'ldl_hdl_ratio': ldl_hdl_ratio,
        'stress_level': stress_level,
        'family_history': family_history,
        'prediction': int(prediction),
        'diagnosis': diagnosis
    }
# Tính toán các thông số đánh giá
def calculate_metrics(true_labels, predicted_labels):
    accuracy = accuracy_score(true_labels, predicted_labels)
    precision = precision_score(true_labels, predicted_labels, average='binary', pos_label=1, zero_division=0)
    recall = recall_score(true_labels, predicted_labels, average='binary', pos_label=1, zero_division=0)
    f1 = f1_score(true_labels, predicted_labels, average='binary', pos_label=1, zero_division=0)
    cm = confusion_matrix(true_labels, predicted_labels)

    return accuracy, precision, recall, f1, cm

# Chuyển ma trận nhầm lẫn thành DataFrame
def convert_cm_to_df(cm):
    cm_df = pd.DataFrame(cm, columns=["Predicted Negative", "Predicted Positive"],
                         index=["True Negative", "True Positive"])
    return cm_df

# Route chính để xuất báo cáo PDF
@app.route('/exportpdf')
def test_export_pdf():
    try:
        data = fetch_data_from_db()
        results = [prepare_features(row) for row in data]

        true_labels = [row['diagnosis'] for row in results]  # Lấy nhãn thực tế
        predicted_labels = [row['prediction'] for row in results]  # Lấy nhãn dự đoán

        accuracy, precision, recall, f1, cm = calculate_metrics(true_labels, predicted_labels)
        cm_df = convert_cm_to_df(cm)

        return render_template('exportpdf.html', data=results, accuracy=accuracy,
                               precision=precision, recall=recall, f1=f1, cm=cm_df.to_html())
    except Exception as e:
        return f"Lỗi khi lấy dữ liệu: {str(e)}"






# Cấu hình kết nối MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',  # Thay bằng username MySQL của bạn
    'password': '123456',  # Thay bằng password MySQL của bạn
    'database': 'dataminingproject',  # Thay bằng tên database của bạn
    'auth_plugin': 'mysql_native_password'
}


def preprocess_data(data):
    """Tiền xử lý dữ liệu"""
    # Chuyển đổi dữ liệu phân loại
    data['gender'] = data['gender'].map({'M': 1, 'F': 0})
    data['exercise_angina'] = data['exercise_angina'].map({'Y': 1, 'N': 0})
    data['shortness_of_breath'] = data['shortness_of_breath'].map({'None': 0, 'Mild': 1, 'Moderate': 2, 'Severe': 3})
    data['fatigue'] = data['fatigue'].map({'Never': 0, 'Sometimes': 1, 'Often': 2})
    data['dizziness'] = data['dizziness'].map({'Never': 0, 'Occasional': 1, 'Often': 2})
    data['family_history'] = data['family_history'].map({'Y': 1, 'N': 0})
    return data


def save_to_db(age, gender, chest_pain_type, resting_blood_pressure, cholesterol,
               max_heart_rate, exercise_angina, blood_sugar, shortness_of_breath, fatigue,
               dizziness, chest_pain_frequency, heart_rate_variability, pulse_pressure,
               ldl_hdl_ratio, stress_level, family_history, diagnosis):
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
         max_heart_rate, exercise_angina, blood_sugar, shortness_of_breath, fatigue,
         dizziness, chest_pain_frequency, heart_rate_variability, pulse_pressure,
         ldl_hdl_ratio, stress_level, family_history, diagnosis)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (new_id, age, gender, chest_pain_type, resting_blood_pressure,
                  cholesterol, max_heart_rate, exercise_angina, blood_sugar,
                  shortness_of_breath, fatigue, dizziness, chest_pain_frequency,
                  heart_rate_variability, pulse_pressure, ldl_hdl_ratio,
                  stress_level, family_history, diagnosis)

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
               max_heart_rate, exercise_angina, blood_sugar,shortness_of_breath,fatigue,dizziness,
               chest_pain_frequency,heart_rate_variability,pulse_pressure,ldl_hdl_ratio,stress_level,family_history, diagnosis
        FROM patients_data_mining
        """

        cursor.execute(query)
        result = cursor.fetchall()

        data = pd.DataFrame(result, columns=[
            'age', 'gender', 'chest_pain_type', 'resting_blood_pressure',
            'cholesterol', 'max_heart_rate', 'exercise_angina',
            'blood_sugar','shortness_of_breath','fatigue','dizziness',
               'chest_pain_frequency','heart_rate_variability','pulse_pressure','ldl_hdl_ratio','stress_level','family_history', 'diagnosis'
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
        data = preprocess_data(data.copy())  # Pass a copy to avoid modifying the original DataFrame

        # Chọn đặc trưng
        X = data[['age', 'gender', 'chest_pain_type', 'resting_blood_pressure',
                  'cholesterol', 'max_heart_rate', 'exercise_angina', 'blood_sugar',
                  'shortness_of_breath', 'fatigue', 'dizziness', 'chest_pain_frequency',
                  'heart_rate_variability', 'pulse_pressure', 'ldl_hdl_ratio', 'stress_level', 'family_history']]
        print("Feature columns in train_model:", X.columns)  # Debugging: Print feature names
        y = data['diagnosis']  # Giả sử bạn đã cập nhật nhãn cho 3 lớp

        # Chia tập dữ liệu
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Chuẩn hóa dữ liệu
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)  # Cập nhật với đầy đủ đặc trưng mới
        joblib.dump(scaler, 'model/heart_disease_scaler.joblib')

        X_test_scaled = scaler.transform(X_test)  # Transform the test set using the fitted scaler

        # Huấn luyện mô hình Random Forest
        model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
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

def compare_with_community(user_data, all_data, threshold=0.1):
    """
    So sánh dữ liệu của người dùng với dữ liệu cộng đồng và đưa ra lời khuyên chi tiết.

    Args:
        user_data (pd.Series): Dữ liệu của người dùng (một dòng trong DataFrame).
        all_data (pd.DataFrame): Toàn bộ dữ liệu (trừ dữ liệu của người dùng).
        threshold (float): Ngưỡng để coi là "khác biệt" (ví dụ: 0.1 = 10%).

    Returns:
        str: Lời khuyên dựa trên so sánh.
    """

    advice = "Dựa trên sự so sánh với dữ liệu cộng đồng:\n"
    community_means = all_data.mean()
    community_stds = all_data.std()  # Tính độ lệch chuẩn

    # So sánh từng thuộc tính và đưa ra lời khuyên
    for feature in user_data.index:
        if feature in community_means and feature in community_stds:
            user_value = user_data[feature]
            community_mean = community_means[feature]
            community_std = community_stds[feature]

            # Tính Z-score để chuẩn hóa
            if community_std > 0:  # Avoid division by zero
                z_score = (user_value - community_mean) / community_std
            else:
                z_score = 0  # Nếu độ lệch chuẩn bằng 0, xem xét giá trị là tương đương

            if abs(z_score) > 1:  # Sử dụng Z-score để xác định sự khác biệt
                if feature == 'age':
                    advice += f"- Tuổi của bạn {'cao hơn' if user_value > community_mean else 'thấp hơn'} trung bình cộng đồng. {user_value:.0f} so với {community_mean:.0f}.\n"
                elif feature == 'gender':
                    advice += f"- Giới tính của bạn {'tương đồng' if user_value == community_mean else 'khác biệt'} so với cộng đồng.\n"
                elif feature == 'chest_pain_type':
                    advice += f"- Loại đau ngực của bạn {'tương đồng' if user_value == community_mean else 'khác biệt'} so với cộng đồng.\n"
                elif feature == 'resting_blood_pressure':
                    advice += f"- Huyết áp khi nghỉ của bạn {'cao hơn' if user_value > community_mean else 'thấp hơn'}  so với cộng đồng. Giá trị: {user_value:.0f} so với {community_mean:.0f} mmHg.\n"
                elif feature == 'cholesterol':
                    advice += f"- Cholesterol của bạn {'cao hơn' if user_value > community_mean else 'thấp hơn'} so với cộng đồng. Giá trị: {user_value:.0f} so với {community_mean:.0f} mg/dL.\n"
                elif feature == 'max_heart_rate':
                    advice += f"- Nhịp tim tối đa của bạn {'cao hơn' if user_value > community_mean else 'thấp hơn'} so với cộng đồng. Giá trị: {user_value:.0f} so với {community_mean:.0f} bpm.\n"
                elif feature == 'exercise_angina':
                    advice += f"- Đau thắt ngực khi tập: {'có' if user_value == 1 else 'không'} so với cộng đồng.\n"
                elif feature == 'blood_sugar':
                    advice += f"- Đường huyết của bạn {'cao' if user_value == 1 else 'bình thường'} so với cộng đồng.\n"
                elif feature == 'shortness_of_breath':
                    advice += f"- Khó thở của bạn {'khác biệt' if user_value != community_mean else 'tương đồng'} so với cộng đồng.\n"
                elif feature == 'fatigue':
                    advice += f"- Mệt mỏi của bạn {'khác biệt' if user_value != community_mean else 'tương đồng'} so với cộng đồng.\n"
                elif feature == 'dizziness':
                    advice += f"- Chóng mặt của bạn {'khác biệt' if user_value != community_mean else 'tương đồng'} so với cộng đồng.\n"
                elif feature == 'chest_pain_frequency':
                    advice += f"- Tần suất đau ngực của bạn {'khác biệt' if user_value != community_mean else 'tương đồng'} so với cộng đồng.\n"
                elif feature == 'heart_rate_variability':
                    advice += f"- Biến thiên nhịp tim của bạn {'cao hơn' if user_value > community_mean else 'thấp hơn'} so với cộng đồng. Giá trị: {user_value:.0f} so với {community_mean:.0f} ms.\n"
                elif feature == 'pulse_pressure':
                    advice += f"- Áp lực mạch của bạn {'cao hơn' if user_value > community_mean else 'thấp hơn'} so với cộng đồng. Giá trị: {user_value:.0f} so với {community_mean:.0f} mmHg.\n"
                elif feature == 'ldl_hdl_ratio':
                    advice += f"- Tỷ lệ LDL/HDL của bạn {'cao hơn' if user_value > community_mean else 'thấp hơn'} so với cộng đồng. Giá trị: {user_value:.1f} so với {community_mean:.1f}.\n"
                elif feature == 'stress_level':
                    advice += f"- Mức độ căng thẳng của bạn {'cao hơn' if user_value > community_mean else 'thấp hơn'} so với cộng đồng. Giá trị: {user_value:.0f} so với {community_mean:.0f}.\n"
                elif feature == 'family_history':
                     advice += f"- Tiền sử gia đình: {'có' if user_value == 1 else 'không'} so với cộng đồng.\n"
        else:
            advice += f"- Không thể so sánh {feature} với dữ liệu cộng đồng.\n"
    advice += "Vui lòng tham khảo ý kiến bác sĩ để được tư vấn chi tiết và có các biện pháp phòng ngừa phù hợp."
    return advice
@app.route('/predict_heart', methods=['GET', 'POST'])
def predict_heart():
    try:
        # Load the model and scaler (assuming they are loaded during app initialization)
        model = joblib.load('model/heart_disease_rf_model.joblib')
        scaler = joblib.load('model/heart_disease_scaler.joblib')

        if request.method == 'POST':
            # Get data from the form
            age = int(request.form['age'])
            gender = request.form['gender']
            chest_pain_type = int(request.form['chest_pain_type'])
            resting_blood_pressure = int(request.form['resting_blood_pressure'])
            cholesterol = int(request.form['cholesterol'])
            max_heart_rate = int(request.form['max_heart_rate'])
            exercise_angina = request.form['exercise_angina']
            blood_sugar = int(request.form['blood_sugar'])
            shortness_of_breath = request.form['shortness_of_breath']
            fatigue = request.form['fatigue']
            dizziness = request.form['dizziness']
            chest_pain_frequency = int(request.form['chest_pain_frequency'])
            heart_rate_variability = int(request.form['heart_rate_variability'])
            pulse_pressure = int(request.form['pulse_pressure'])
            ldl_hdl_ratio = float(request.form['ldl_hdl_ratio'])
            stress_level = int(request.form['stress_level'])
            family_history = request.form['family_history']

            # Encode categorical features (consistent with preprocessing in train_model)
            gender_encoded = 1 if gender == 'M' else 0  # Assuming 'M' is male, 'F' is female
            exercise_angina_encoded = 1 if exercise_angina == 'Y' else 0
            family_history_encoded = 1 if family_history == 'Y' else 0

            # Encode other categorical features (shortness_of_breath, fatigue, dizziness) - **IMPORTANT: Ensure consistency with preprocess_data() and training**
            shortness_of_breath_encoded = {'None': 0, 'Mild': 1, 'Moderate': 2, 'Severe': 3}[shortness_of_breath]
            fatigue_encoded = {'Never': 0, 'Sometimes': 1, 'Often': 2}[fatigue]
            dizziness_encoded = {'Never': 0, 'Occasional': 1, 'Often': 2}[dizziness]

            # Create a DataFrame for the input features
            features = pd.DataFrame([[
                age, gender_encoded, chest_pain_type, resting_blood_pressure,
                cholesterol, max_heart_rate, exercise_angina_encoded, blood_sugar,
                shortness_of_breath_encoded, fatigue_encoded, dizziness_encoded,
                chest_pain_frequency, heart_rate_variability, pulse_pressure,
                ldl_hdl_ratio, stress_level, family_history_encoded
            ]], columns=[
                'age', 'gender', 'chest_pain_type', 'resting_blood_pressure',
                'cholesterol', 'max_heart_rate', 'exercise_angina', 'blood_sugar',
                'shortness_of_breath', 'fatigue', 'dizziness', 'chest_pain_frequency',
                'heart_rate_variability', 'pulse_pressure', 'ldl_hdl_ratio', 'stress_level', 'family_history'
            ])
            print("Feature columns in predict_heart:", features.columns) # Debugging: Print feature names
            # Scale the features using the fitted scaler
            features_scaled = scaler.transform(features)

            # Make the prediction
            prediction = model.predict(features_scaled)[0]

            # Bắt đầu điều chỉnh code cho yêu cầu mới
            diagnosis = int(prediction)  # Chuyển prediction thành kiểu int

            risk_level = ""
            if diagnosis == 0:
                risk_level = "Không có khả năng mắc bệnh tim."  # No risk
                comparison_advice = "Dữ liệu của bạn tương đồng với cộng đồng. Duy trì lối sống lành mạnh."
            elif diagnosis == 1:  # Có bệnh
                # Use the existing features to determine the risk level
                if (age > 60 or cholesterol > 240 or resting_blood_pressure > 140 or
                    max_heart_rate < 60 or exercise_angina_encoded == 1 or blood_sugar > 140 or
                    stress_level > 7 or family_history_encoded == 1):
                        risk_level = "Nặng (High Risk) - Cần can thiệp y tế ngay."
                elif (age > 50 or 120 < resting_blood_pressure <= 140 or 180 < cholesterol <= 240 or
                      60 <= max_heart_rate <= 80):
                        risk_level = "Trung bình (Moderate Risk) - Cần theo dõi chặt chẽ."
                else:
                    risk_level = "Nhẹ (Low Risk) - Có nguy cơ nhưng chưa nghiêm trọng."

                # Load all data for comparison (only load once)
                all_data = load_data_from_db()
                # Convert gender and family_history in all_data to numerical values
                all_data['gender'] = all_data['gender'].map({'M': 1, 'F': 0})  # Assuming 'M' and 'F' are the only possible values
                all_data['family_history'] = all_data['family_history'].map({'Y': 1, 'N': 0})
                all_data['shortness_of_breath'] = all_data['shortness_of_breath'].map({'None': 0, 'Mild': 1, 'Moderate': 2, 'Severe': 3})
                all_data['fatigue'] = all_data['fatigue'].map({'Never': 0, 'Sometimes': 1, 'Often': 2})
                all_data['dizziness'] = all_data['dizziness'].map({'Never': 0, 'Occasional': 1, 'Often': 2})
                all_data = all_data.dropna(subset=['gender', 'family_history','shortness_of_breath', 'fatigue', 'dizziness'])

                # Create user_data as a Series
                user_data = pd.Series({
                    'age': age,
                    'gender': gender_encoded,
                    'chest_pain_type': chest_pain_type,
                    'resting_blood_pressure': resting_blood_pressure,
                    'cholesterol': cholesterol,
                    'max_heart_rate': max_heart_rate,
                    'exercise_angina': exercise_angina_encoded,
                    'blood_sugar': blood_sugar,
                    'shortness_of_breath': shortness_of_breath_encoded,
                    'fatigue': fatigue_encoded,
                    'dizziness': dizziness_encoded,
                    'chest_pain_frequency': chest_pain_frequency,
                    'heart_rate_variability': heart_rate_variability,
                    'pulse_pressure': pulse_pressure,
                    'ldl_hdl_ratio': ldl_hdl_ratio,
                    'stress_level': stress_level,
                    'family_history': family_history_encoded
                })


                # Get comparison advice
                comparison_advice = compare_with_community(user_data, all_data)

            else:
                risk_level = "Không xác định" # Handle unexpected prediction values
                comparison_advice = ""

            # Save data to the database (optional - but critical for model improvement)
            # Consider using try-except to handle potential database errors

            save_to_db(age, gender, chest_pain_type, resting_blood_pressure, cholesterol, max_heart_rate, exercise_angina, blood_sugar, shortness_of_breath,fatigue,dizziness,
                       chest_pain_frequency,heart_rate_variability,pulse_pressure,ldl_hdl_ratio,stress_level,family_history,diagnosis)

            # Return the prediction and advice as JSON
            return jsonify({'message': risk_level + "<br><br>" + comparison_advice})  # Return both risk and advice

    except Exception as e:
        # Handle any errors that occur during the prediction process
        return jsonify({'error': str(e)}), 500  # Return an error message as JSON
    # If the request method is GET, render the prediction form
    return render_template('predict.html')

# Khởi tạo mô hình ban đầu khi ứng dụng chạy
def init_model():
    data = load_data_from_db()
    train_model(data)


# Gọi hàm khởi tạo mô hình
init_model()


def perform_kmeans_clustering(data):
    """Thực hiện phân cụm KMeans trên dữ liệu"""
    X = data[['age', 'cholesterol']]  # Sử dụng tuổi và cholesterol cho việc phân cụm
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=3, random_state=42)
    data['cluster'] = kmeans.fit_predict(X_scaled)

    return data


# Chạy ứng dụng Flask
if __name__ == '__main__':
    app.run(debug=True)
