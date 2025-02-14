import csv
import os
import secrets

from mysql.connector import Error
import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from scipy.stats import zscore
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, f1_score, \
    confusion_matrix
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Biến toàn cục để lưu mô hình và scaler
global model, scaler
app = Flask(__name__, static_folder='static')
app.secret_key = secrets.token_hex(16)  # Tạo khóa bí mật 32 ký tự
# Cấu hình kết nối MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',  # Thay bằng username MySQL của bạn
    'password': '',  # Thay bằng password MySQL của bạn
    'database': 'data mining project',  # Thay bằng tên database của bạn
}


# Routes for each HTML page
@app.route('/')
def welcome():
    return redirect('/index')


@app.route('/index')
def index():
    if 'username' not in session:
        flash('Vui lòng đăng nhập trước.', 'warning')
        return redirect('/login')
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/chart', methods=['GET', 'POST'])
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
         SELECT AVG(age), AVG(resting_blood_pressure), AVG(cholesterol), 
                AVG(CASE 
                    WHEN blood_sugar = 'low' THEN 70
                    WHEN blood_sugar = 'normal' THEN 100
                    WHEN blood_sugar = 'high' THEN 140
                    WHEN blood_sugar = 'very high' THEN 180
                    ELSE NULL END) as avg_blood_sugar
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

    # Lấy dữ liệu bệnh tim
    query = "SELECT age, resting_blood_pressure, cholesterol, blood_sugar, diagnosis FROM patients_data_mining"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()

    # Chuyển đổi dữ liệu thành DataFrame
    df = pd.DataFrame(data, columns=["age", "bp", "cholesterol", "blood_sugar", "diagnosis"])

    # Xử lý dữ liệu cho mô hình
    X = df[["age", "bp", "cholesterol"]]
    y = df["diagnosis"]

    # Huấn luyện mô hình Random Forest để đánh giá tầm quan trọng
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Lấy độ quan trọng của từng yếu tố
    feature_importances = model.feature_importances_
    factors = ["Tuổi", "Huyết Áp", "Cholesterol"]
    importance_data = [{"label": factors[i], "value": feature_importances[i]} for i in range(len(factors))]

    # Tiền xử lý dữ liệu phân cụm
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

    # 💡 **Tạo danh sách khuyến nghị sức khỏe**
    recommendations = []

    if request.method == 'POST':
        # Nhận dữ liệu từ form
        age = int(request.form['age'])
        heart_disease = int(request.form['heart_disease'])
        cholesterol = int(request.form['cholesterol'])
        bp = int(request.form['bp'])
        glucose = request.form['glucose']  # Nhận giá trị dưới dạng string

        # Chuyển đổi giá trị đường huyết sang dạng số để xử lý
        if glucose == 'low':
            glucose_value = 70
        elif glucose == 'normal':
            glucose_value = 100
        elif glucose == 'high':
            glucose_value = 140
        elif glucose == 'very high':
            glucose_value = 180
        else:
            glucose_value = None  # Giá trị không hợp lệ

        # Khuyến nghị theo độ tuổi
        recommendations.append(f"Với độ tuổi {age}:")
        if age < 40:
            recommendations.append("✅ Bạn còn trẻ, hãy duy trì lối sống lành mạnh để tránh nguy cơ bệnh tim sau này.")
        elif 40 <= age < 60:
            recommendations.append("⚠️ Tuổi trung niên, cần kiểm soát tốt sức khỏe để giảm nguy cơ bệnh tim.")
        elif age >= 60:
            recommendations.append("⚠️ Tuổi cao, bạn cần chú ý đến sức khỏe tim mạch và kiểm tra thường xuyên.")

        # Khuyến nghị theo cholesterol
        recommendations.append(f"\nCholesterol: {cholesterol} mg/dL")
        if cholesterol <= 150:
            recommendations.append("✅ Mức Cholesterol ổn định, hãy duy trì chế độ ăn uống và luyện tập lành mạnh.")
        elif 150 < cholesterol <= 200:
            recommendations.append("✅ Cholesterol ở mức ổn định, nhưng hãy kiểm soát chế độ ăn uống để giữ mức này.")
        else:  # cholesterol > 200
            recommendations.append(
                "⚠️ Cholesterol cao, cần giảm thực phẩm chứa nhiều cholesterol như thịt đỏ, đồ chiên rán.")
            recommendations.append("✅ Ăn nhiều rau xanh, cá hồi và uống đủ nước.")

        # Khuyến nghị theo huyết áp
        recommendations.append(f"\nHuyết áp: {bp} mmHg")
        if bp <= 130:
            recommendations.append(
                "✅ Huyết áp của bạn ổn định, hãy tiếp tục duy trì thói quen ăn uống và tập thể dục lành mạnh.")
        else:  # bp > 130
            recommendations.append("⚠️ Huyết áp cao, hãy giảm muối và thực phẩm chế biến sẵn.")
            recommendations.append("✅ Duy trì tập thể dục nhẹ nhàng như đi bộ hoặc yoga để kiểm soát huyết áp.")

        # Khuyến nghị theo đường huyết
        recommendations.append(f"\nĐường huyết: {glucose}")
        if glucose_value is not None:
            if glucose_value <= 140:
                recommendations.append(
                    "✅ Đường huyết của bạn ổn định, hãy duy trì chế độ ăn uống lành mạnh và kiểm tra định kỳ.")
            else:  # glucose_value > 140
                recommendations.append("⚠️ Đường huyết cao, hãy giảm ăn đường, tránh nước ngọt có ga.")
                recommendations.append("✅ Kiểm tra đường huyết định kỳ và ăn thực phẩm giàu chất xơ.")

        # Khuyến nghị nếu bệnh tim có và các chỉ số ổn định
        if heart_disease == 1 and (cholesterol <= 200 and bp <= 130 and glucose_value <= 140):
            recommendations.append(
                "✅ Mặc dù bạn có bệnh tim, các chỉ số hiện tại của bạn rất ổn định. Tiếp tục duy trì lối sống lành mạnh.")
        elif heart_disease == 1 and (cholesterol > 200 or bp > 130 or glucose_value > 140):
            recommendations.append(
                "⚠️ Bạn có bệnh tim và các chỉ số không ổn định. Hãy theo dõi sức khỏe thường xuyên và tuân thủ chỉ dẫn của bác sĩ.")

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
                           correlation_bp_cholesterol_data=correlation_bp_cholesterol_data,
                           importance_data=importance_data,
                           recommendations=recommendations)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/datapatient')
def datapatient():
    # Kết nối tới database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Truy vấn dữ liệu từ database
    query = """
         SELECT patient_id,fullname,age, gender, chest_pain_type, resting_blood_pressure, cholesterol,
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


# Đăng xuất
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Bạn đã đăng xuất', 'info')
    return redirect(url_for('login'))


def fetch_data_from_db_for_exportpdf():
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor() as cursor:
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
                        CASE 
                            WHEN exercise_angina = 'Y' THEN 'Có'
                            WHEN exercise_angina = 'N' THEN 'Không'
                            ELSE exercise_angina
                        END as exercise_angina,
                        blood_sugar,
                        diagnosis
                    FROM patients_data_mining
                 
                """
                cursor.execute(query)
                data = cursor.fetchall()
        return data
    except Exception as e:
        raise Exception(f"Lỗi khi load dữ liệu từ db: {str(e)}")




# Route chính để xuất báo cáo PDF
@app.route('/exportpdf')
def exportpdf():
    try:
        data = fetch_data_from_db_for_exportpdf()


        return render_template('exportpdf.html', data=data,
                               )
    except Exception as e:
        return f"Lỗi khi lấy dữ liệu: {str(e)}"


def save_to_db_for_predict(fullname, age, gender, chest_pain_type, resting_blood_pressure, cholesterol,
                           max_heart_rate, exercise_angina, blood_sugar, shortness_of_breath, fatigue, dizziness,
                           chest_pain_frequency, heart_rate_variability
                           , pulse_pressure, ldl_hdl_ratio, stress_level, family_history, diagnosis):
    """Lưu dữ liệu vào cơ sở dữ liệu"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Lấy giá trị ID lớn nhất hiện có và cộng thêm 1
        cursor.execute("SELECT COALESCE(MAX(patient_id), 0) + 1 FROM patients_data_mining")
        new_id = cursor.fetchone()[0]

        query = """
        INSERT INTO patients_data_mining 
        (patient_id,fullname,age, gender, chest_pain_type, resting_blood_pressure, cholesterol, 
         max_heart_rate, exercise_angina, blood_sugar, shortness_of_breath, fatigue, dizziness, chest_pain_frequency, heart_rate_variability
                , pulse_pressure, ldl_hdl_ratio,stress_level, family_history, diagnosis)
        VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (new_id, fullname, age, gender, chest_pain_type, resting_blood_pressure,
                  cholesterol, max_heart_rate, exercise_angina,
                  blood_sugar, shortness_of_breath, fatigue, dizziness, chest_pain_frequency, heart_rate_variability
                  , pulse_pressure, ldl_hdl_ratio, stress_level, family_history, diagnosis)

        cursor.execute(query, values)
        conn.commit()
        print("Dữ liệu đã được lưu vào cơ sở dữ liệu")

    except mysql.connector.Error as err:
        print(f"Lỗi: {err}")
    finally:
        cursor.close()
        conn.close()


def save_to_csv_for_predict(fullname, age, gender, chest_pain_type, resting_blood_pressure, cholesterol,
                            max_heart_rate, exercise_angina, blood_sugar, shortness_of_breath, fatigue, dizziness,
                            chest_pain_frequency, heart_rate_variability, pulse_pressure, ldl_hdl_ratio,
                            stress_level, family_history, diagnosis,
                            filename='data/heart_disease_data_updated_5_2_25.csv'):
    """Lưu dữ liệu vào file CSV"""
    try:
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Mở file CSV để ghi
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Ghi tiêu đề nếu file trống
            if file.tell() == 0:
                writer.writerow(['patient_id', 'fullname', 'age', 'gender', 'chest_pain_type',
                                 'resting_blood_pressure', 'cholesterol', 'max_heart_rate',
                                 'exercise_angina', 'blood_sugar', 'shortness_of_breath',
                                 'fatigue', 'dizziness', 'chest_pain_frequency',
                                 'heart_rate_variability', 'pulse_pressure',
                                 'ldl_hdl_ratio', 'stress_level', 'family_history',
                                 'diagnosis'])
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Lấy giá trị ID lớn nhất hiện có và cộng thêm 1
            cursor.execute("SELECT COALESCE(MAX(patient_id), 0) + 1 FROM patients_data_mining")
            new_id = cursor.fetchone()[0]
            # Ghi dữ liệu vào file
            writer.writerow([new_id, fullname, age, gender, chest_pain_type, resting_blood_pressure,
                             cholesterol, max_heart_rate, exercise_angina, blood_sugar,
                             shortness_of_breath, fatigue, dizziness, chest_pain_frequency,
                             heart_rate_variability, pulse_pressure, ldl_hdl_ratio,
                             stress_level, family_history, diagnosis])

        print("Dữ liệu đã được lưu vào file CSV")

    except Exception as e:
        print(f"Lỗi khi lưu dữ liệu vào file CSV: {e}")


# === Hàm chuyển đổi giá trị sang chuỗi tiếng Anh ===
def convert_blood_sugar(value):
    return {1: "Normal", 2: "High", 3: "Very High", 4: "Low"}.get(value, "Unknown")


def convert_shortness_of_breath(value):
    return {1: "None", 2: "Severe", 3: "Moderate"}.get(value, "Unknown")


def convert_fatigue(value):
    return {1: "None", 2: "Sometimes", 3: "Often"}.get(value, "Unknown")


def convert_dizziness(value):
    return {1: "None", 2: "Occasional", 3: "Often"}.get(value, "Unknown")


@app.route('/predict_heart', methods=['POST', 'GET'])
def predict_heart():
    try:

        if request.method == 'POST':
            # Tải mô hình và scaler
            model = joblib.load('models/random_forest_model_latest.joblib')
            scaler = joblib.load('models/random_forest_scaler_latest.joblib')

            # Lấy dữ liệu từ form
            age = int(request.form['age'])
            fullname = request.form['fullname']
            gender = request.form['gender']
            chest_pain_type = int(request.form['chest_pain_type'])
            resting_blood_pressure = int(request.form['resting_blood_pressure'])
            cholesterol = int(request.form['cholesterol'])
            max_heart_rate = int(request.form['max_heart_rate'])
            exercise_angina = request.form['exercise_angina']
            blood_sugar = int(request.form['blood_sugar'])
            shortness_of_breath = int(request.form['shortness_of_breath'])
            fatigue = int(request.form['fatigue'])
            dizziness = int(request.form['dizziness'])
            chest_pain_frequency = int(request.form['chest_pain_frequency'])
            heart_rate_variability = int(request.form['heart_rate_variability'])
            pulse_pressure = int(request.form['pulse_pressure'])
            ldl_hdl_ratio = float(request.form['ldl_hdl_ratio'])
            stress_level = int(request.form['stress_level'])
            family_history = int(request.form['family_history'])

            # Chuyển đổi giá trị sang chuỗi tiếng Anh
            blood_sugar_str = convert_blood_sugar(blood_sugar)
            shortness_of_breath_str = convert_shortness_of_breath(shortness_of_breath)
            fatigue_str = convert_fatigue(fatigue)
            dizziness_str = convert_dizziness(dizziness)

            # Mã hóa các thuộc tính
            gender_encoded = 1 if gender == 'M' else 0
            exercise_angina_encoded = 1 if exercise_angina == 'Y' else 0

            # === Thêm các đặc trưng tương tác ===
            age_blood_pressure_interaction = age * resting_blood_pressure
            cholesterol_blood_pressure_interaction = cholesterol * resting_blood_pressure
            max_heart_rate_age_interaction = max_heart_rate / age
            chest_pain_blood_pressure_interaction = chest_pain_type * resting_blood_pressure
            cholesterol_diagnosis_interaction = cholesterol * family_history
            ldl_hdl_cholesterol_interaction = ldl_hdl_ratio * cholesterol
            stress_pain_interaction = stress_level * chest_pain_frequency
            family_history_diagnosis_interaction = family_history * 1  # Giữ nguyên do nó đã binary
            blood_sugar_fatigue_interaction = blood_sugar * fatigue
            chest_pain_diagnosis_interaction = chest_pain_frequency * 1  # Giữ nguyên do nó có ý nghĩa trực tiếp

            # Chuẩn bị dữ liệu để dự đoán
            features = pd.DataFrame([[
                age, gender_encoded, chest_pain_type, resting_blood_pressure, cholesterol, max_heart_rate,
                exercise_angina_encoded, blood_sugar, shortness_of_breath, fatigue, dizziness, chest_pain_frequency,
                heart_rate_variability, pulse_pressure, ldl_hdl_ratio, stress_level, family_history,
                # Thêm các đặc trưng mới
                age_blood_pressure_interaction, cholesterol_blood_pressure_interaction, max_heart_rate_age_interaction,
                chest_pain_blood_pressure_interaction, cholesterol_diagnosis_interaction,
                ldl_hdl_cholesterol_interaction, stress_pain_interaction, family_history_diagnosis_interaction,
                blood_sugar_fatigue_interaction, chest_pain_diagnosis_interaction
            ]], columns=[
                'age', 'gender', 'chest_pain_type', 'resting_blood_pressure', 'cholesterol', 'max_heart_rate',
                'exercise_angina', 'blood_sugar', 'shortness_of_breath', 'fatigue', 'dizziness', 'chest_pain_frequency',
                'heart_rate_variability', 'pulse_pressure', 'ldl_hdl_ratio', 'stress_level', 'family_history',
                # Tên cột cho các đặc trưng mới
                'age_blood_pressure_interaction', 'cholesterol_blood_pressure_interaction',
                'max_heart_rate_age_interaction',
                'chest_pain_blood_pressure_interaction', 'cholesterol_diagnosis_interaction',
                'ldl_hdl_cholesterol_interaction', 'stress_pain_interaction', 'family_history_diagnosis_interaction',
                'blood_sugar_fatigue_interaction', 'chest_pain_diagnosis_interaction'
            ])

            # Chuẩn hóa đặc trưng
            features_scaled = scaler.transform(features)

            # Dự đoán kết quả
            prediction = model.predict(features_scaled)[0]
            result = 1 if prediction == 1 else 0
            risk_level = ""
            if result == 0:
                risk_level = "Không có nguy cơ mắc bệnh tim."
            elif result == 1:
                # Sử dụng các yếu tố để đánh giá mức độ rủi ro (điều chỉnh các ngưỡng cho phù hợp)
                risk_factors = 0
                if age > 60:
                    risk_factors += 1
                if cholesterol > 240:
                    risk_factors += 1
                if resting_blood_pressure > 140:
                    risk_factors += 1
                if max_heart_rate < 100:
                    risk_factors += 1
                if exercise_angina_encoded == 1:
                    risk_factors += 1
                if blood_sugar > 1:
                    risk_factors += 1

                if risk_factors >= 3:
                    risk_level = "Nặng (High Risk) - Cần can thiệp y tế ngay."
                elif risk_factors == 2:
                    risk_level = "Trung bình (Moderate Risk) - Cần theo dõi chặt chẽ."
                else:
                    risk_level = "Nhẹ (Low Risk) - Có nguy cơ nhưng chưa nghiêm trọng."
            # Lưu kết quả xuống cơ sở dữ liệu
            save_to_db_for_predict(
                fullname=fullname, age=age, gender=gender, chest_pain_type=chest_pain_type,
                resting_blood_pressure=resting_blood_pressure,
                cholesterol=cholesterol, max_heart_rate=max_heart_rate, exercise_angina=exercise_angina,
                blood_sugar=blood_sugar_str, shortness_of_breath=shortness_of_breath_str, fatigue=fatigue_str,
                dizziness=dizziness_str,
                chest_pain_frequency=chest_pain_frequency, heart_rate_variability=heart_rate_variability,
                pulse_pressure=pulse_pressure, ldl_hdl_ratio=ldl_hdl_ratio, stress_level=stress_level,
                family_history=family_history, diagnosis=result
            )
            save_to_csv_for_predict(
                fullname=fullname, age=age, gender=gender, chest_pain_type=chest_pain_type,
                resting_blood_pressure=resting_blood_pressure,
                cholesterol=cholesterol, max_heart_rate=max_heart_rate, exercise_angina=exercise_angina,
                blood_sugar=blood_sugar_str, shortness_of_breath=shortness_of_breath_str, fatigue=fatigue_str,
                dizziness=dizziness_str,
                chest_pain_frequency=chest_pain_frequency, heart_rate_variability=heart_rate_variability,
                pulse_pressure=pulse_pressure, ldl_hdl_ratio=ldl_hdl_ratio, stress_level=stress_level,
                family_history=family_history, diagnosis=result
            )

            # Trả kết quả về dưới dạng JSON
            return jsonify({
                'diagnosis': result,
                'blood_sugar': blood_sugar_str,
                'shortness_of_breath': shortness_of_breath_str,
                'fatigue': fatigue_str,
                'dizziness': dizziness_str,
                'risk_level': risk_level
            })

        # Nếu phương thức là GET, hiển thị form
        return render_template('predict.html')

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'error': f'Có lỗi xảy ra: {str(e)}'}), 500


def perform_kmeans_clustering(data):
    """Thực hiện phân cụm KMeans trên dữ liệu"""
    X = data[['age', 'cholesterol']]  # Sử dụng tuổi và cholesterol cho việc phân cụm
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=3, random_state=42)
    data['cluster'] = kmeans.fit_predict(X_scaled)

    return data


from flask import session, render_template
import mysql.connector
from mysql.connector import Error

from flask import session, render_template
import mysql.connector
from mysql.connector import Error

@app.route("/datauser")
def datauser():
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Fetch results as dictionary
        fullName = session.get('username')

        patients = []  # Mặc định là danh sách rỗng nếu không có user

        if fullName:
            # Query to get all patients for the logged-in user (use parameterized query)
            query = """
                SELECT * FROM patients_data_mining 
                JOIN users ON patients_data_mining.fullname = users.username 
                WHERE patients_data_mining.fullname = %s
            """
            cursor.execute(query, (fullName,))
            patients = cursor.fetchall()

        # Close the connection
        cursor.close()
        conn.close()

        print('Dữ liệu:', patients)
        return render_template('datauser.html', patients=patients)

    except Error as e:
        return f"Error connecting to MySQL database: {str(e)}", 500




@app.route('/compare_with_community', methods=['GET', 'POST'])
def compare_with_community():
    try:
        # Get data from the form
        age = int(request.form['age'])
        gender = request.form['gender']
        chest_pain_type = int(request.form['chest_pain_type'])
        resting_blood_pressure = int(request.form['resting_blood_pressure'])
        cholesterol = int(request.form['cholesterol'])
        max_heart_rate = int(request.form['max_heart_rate'])
        exercise_angina = request.form['exercise_angina']
        blood_sugar = request.form['blood_sugar']
        data_limit = request.form['data_limit']  # Nhận khoảng số lượng

        # Call the comparison logic
        comparison_text = compare_with_community_logic(
            age, gender, chest_pain_type, resting_blood_pressure,
            cholesterol, max_heart_rate, exercise_angina, blood_sugar, data_limit
        )

        # Create response object
        response = jsonify({'message': comparison_text})

        # Add header object and set utf-8
        response.headers['Content-Type'] = 'application/json; charset=utf-8'

        return response

    except Exception as e:
        # Create error response
        error_response = jsonify({'error': str(e)})

        # Add header for error and set utf-8
        error_response.headers['Content-Type'] = 'application/json; charset=utf-8'

        return error_response, 500  # 500 status code for internal server error


@app.route("/comparing", methods=['GET', 'POST'])
def comparing():
    return render_template("comparing.html")


def compare_with_community_logic(age, gender, chest_pain_type, resting_blood_pressure, cholesterol,
                                 max_heart_rate, exercise_angina, blood_sugar, limit):
    """
    Lấy dữ liệu từ cơ sở dữ liệu và so sánh các cột liên quan đến bệnh nhân
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Đếm số lượng dữ liệu
        count_query = "SELECT COUNT(*) FROM patients_data_mining"
        cursor.execute(count_query)
        total_count = cursor.fetchone()[0]

        # Lấy dữ liệu theo giới hạn
        limit_value = 50 if limit == '50' else 100 if limit == '100' else total_count
        query = f"""
            SELECT 
                age,
                gender,
                chest_pain_type,
                resting_blood_pressure,
                cholesterol,
                max_heart_rate,
                exercise_angina,
                blood_sugar
            FROM patients_data_mining
            LIMIT {limit_value}
        """
        cursor.execute(query)
        data = cursor.fetchall()

        # Chuyển đổi dữ liệu thành DataFrame
        df = pd.DataFrame(data, columns=[
            'age', 'gender', 'chest_pain_type', 'resting_blood_pressure',
            'cholesterol', 'max_heart_rate', 'exercise_angina', 'blood_sugar'
        ])

        # Mã hóa dữ liệu
        df['gender'] = df['gender'].map({'M': 1, 'F': 0})
        df['exercise_angina'] = df['exercise_angina'].map({'Y': 1, 'N': 0})
        user_gender_encoded = 1 if gender == 'M' else 0
        user_exercise_angina_encoded = 1 if exercise_angina == 'Y' else 0

        # Tính toán giá trị trung bình và độ lệch chuẩn
        age_mean, age_std = df['age'].mean(), df['age'].std()
        rbp_mean, rbp_std = df['resting_blood_pressure'].mean(), df['resting_blood_pressure'].std()
        chol_mean, chol_std = df['cholesterol'].mean(), df['cholesterol'].std()
        mhr_mean, mhr_std = df['max_heart_rate'].mean(), df['max_heart_rate'].std()

        # So sánh dữ liệu bệnh nhân với giá trị trung bình
        comparison_text = f"So sánh với dữ liệu cộng đồng ({total_count} tổng số bản ghi):\n"
        if age > age_mean + age_std:
            comparison_text += f"- Tuổi của bạn ({age}) cao hơn đáng kể so với trung bình cộng đồng ({age_mean:.2f}).\n"
        elif age < age_mean - age_std:
            comparison_text += f"- Tuổi của bạn ({age}) thấp hơn đáng kể so với trung bình cộng đồng ({age_mean:.2f}).\n"

        if resting_blood_pressure > rbp_mean + rbp_std:
            comparison_text += f"- Huyết áp của bạn ({resting_blood_pressure}) cao hơn đáng kể so với trung bình ({rbp_mean:.2f}).\n"
        elif resting_blood_pressure < rbp_mean - rbp_std:
            comparison_text += f"- Huyết áp của bạn ({resting_blood_pressure}) thấp hơn đáng kể so với trung bình ({rbp_mean:.2f}).\n"

        if cholesterol > chol_mean + chol_std:
            comparison_text += f"- Cholesterol của bạn ({cholesterol}) cao hơn đáng kể so với trung bình ({chol_mean:.2f}).\n"
        elif cholesterol < chol_mean - chol_std:
            comparison_text += f"- Cholesterol của bạn ({cholesterol}) thấp hơn đáng kể so với trung bình ({chol_mean:.2f}).\n"

        if max_heart_rate < mhr_mean - mhr_std:
            comparison_text += f"- Nhịp tim tối đa của bạn ({max_heart_rate}) thấp hơn đáng kể so với trung bình ({mhr_mean:.2f}).\n"
        elif max_heart_rate > mhr_mean + mhr_std:
            comparison_text += f"- Nhịp tim tối đa của bạn ({max_heart_rate}) cao hơn đáng kể so với trung bình ({mhr_mean:.2f}).\n"

        if user_gender_encoded > df['gender'].mean() + 1:
            comparison_text += f"- So với cộng đồng thì giới tính của bạn có sự khác biệt lớn\n"
        if user_exercise_angina_encoded > df['exercise_angina'].mean() + 1:
            comparison_text += f"- So với cộng đồng thì khả năng đau thắt ngực của bạn có sự khác biệt lớn\n"

        cursor.close()
        conn.close()

        return comparison_text

    except Exception as e:
        print(f"Lỗi khi so sánh dữ liệu: {str(e)}")
        return "Không thể so sánh dữ liệu với cộng đồng."


# hàm này cho phần cross validation
def preprocess_data(data):
    """Tiền xử lý dữ liệu"""
    # Xử lý các giá trị null
    data = data.dropna()  # Đánh dấu và loại bỏ các giá trị null
    # Kiểm tra và lọc các giá trị bất thường
    valid_genders = {'M', 'F'}
    data = data[data['gender'].isin(valid_genders)]  # Loại bỏ giá trị không hợp lệ

    valid_yes_no = {'Y', 'N'}
    for col in ['exercise_angina', 'family_history']:
        data = data[data[col].isin(valid_yes_no)]  # Chỉ giữ các giá trị 'Y' hoặc 'N'

    valid_levels = {
        'blood_sugar': {'Very High', 'Normal', 'High'},
        'shortness_of_breath': {'Severe', 'None', 'Moderate'},
        'fatigue': {'Never', 'Sometime', 'Often'},
        'dizziness': {'Never', 'Occasional', 'Often'}
    }

    for col, valid_set in valid_levels.items():
        data = data[data[col].isin(valid_set)]  # Loại bỏ các giá trị ngoài danh mục hợp lệ
    # mã hóa dữ liệu phân loại
    data['gender'] = data['gender'].map({'M': 1, 'F': 0})
    data['exercise_angina'] = data['exercise_angina'].map({'Y': 1, 'N': 0})
    data['blood_sugar'] = data['blood_sugar'].map({'Very High': 2, 'Normal': 0, 'High': 1})
    data['shortness_of_breath'] = data['shortness_of_breath'].map({'Severe': 2, 'None': 0, 'Moderate': 1})
    data['fatigue'] = data['fatigue'].map({'Often': 1, 'Never': 0, 'Sometime': 2})
    data['dizziness'] = data['dizziness'].map({'Never': 0, 'Occasional': 1, 'Often': 2})
    data['family_history'] = data['family_history'].map({'Y': 1, 'N': 0})

    # Xử lý outlier bằng Z-score
    numeric_cols = data.select_dtypes(include=[np.number]).columns  # Chỉ lấy các cột số
    z_scores = np.abs(zscore(data[numeric_cols]))  # Tính Z-score
    data = data[(z_scores < 3).all(axis=1)]  # Giữ lại các dòng có Z-score < 3
    return data


def load_data_from_db_cross_validation():
    """Lấy dữ liệu từ cơ sở dữ liệu"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = """
        SELECT age, gender, chest_pain_type, resting_blood_pressure, cholesterol,
               max_heart_rate, exercise_angina, blood_sugar, shortness_of_breath, fatigue, dizziness, chest_pain_frequency, heart_rate_variability
                , pulse_pressure, ldl_hdl_ratio,stress_level, family_history, diagnosis
        FROM patients_data_mining
        """

        cursor.execute(query)
        result = cursor.fetchall()

        data = pd.DataFrame(result, columns=[
            'age', 'gender', 'chest_pain_type', 'resting_blood_pressure',
            'cholesterol', 'max_heart_rate', 'exercise_angina', 'blood_sugar', 'shortness_of_breath', 'fatigue',
            'dizziness',
            'chest_pain_frequency', 'heart_rate_variability',
            'pulse_pressure', 'ldl_hdl_ratio', 'stress_level',
            'family_history', 'diagnosis'
        ])

        return data

    except mysql.connector.Error as err:
        print(f"Lỗi: {err}")
        return None
    finally:
        cursor.close()
        conn.close()


def perform_cross_validation(data):
    """Thực hiện cross-validation trên dữ liệu"""
    try:
        processed_data = preprocess_data(data)
        if processed_data is None:
            raise ValueError("Dữ liệu tiền xử lý không hợp lệ")

        feature_columns = [
            'age', 'gender', 'chest_pain_type', 'resting_blood_pressure',
            'cholesterol', 'max_heart_rate', 'exercise_angina', 'blood_sugar',
            'shortness_of_breath', 'fatigue', 'dizziness',
            'chest_pain_frequency', 'heart_rate_variability',
            'pulse_pressure', 'ldl_hdl_ratio', 'stress_level',
            'family_history'
        ]

        missing_columns = [col for col in feature_columns if col not in processed_data.columns]
        if missing_columns:
            print(f"Cảnh báo: Thiếu các cột sau trong dữ liệu: {missing_columns}")
            feature_columns = [col for col in feature_columns if col in processed_data.columns]

        X = processed_data[feature_columns]
        y = processed_data['diagnosis']

        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        scaler = StandardScaler()
        model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)

        accuracies, precisions, recalls, f1_scores = [], [], [], []

        for fold, (train_idx, val_idx) in enumerate(cv.split(X, y), 1):
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

            X_train_scaled = scaler.fit_transform(X_train)
            X_val_scaled = scaler.transform(X_val)

            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_val_scaled)

            accuracies.append(accuracy_score(y_val, y_pred))
            precisions.append(precision_score(y_val, y_pred, zero_division=0))
            recalls.append(recall_score(y_val, y_pred, zero_division=0))
            f1_scores.append(f1_score(y_val, y_pred, zero_division=0))

            print(f"\nKết quả fold {fold}:")
            print(f"Accuracy: {accuracies[-1]:.3f}")
            print(f"Precision: {precisions[-1]:.3f}")
            print(f"Recall: {recalls[-1]:.3f}")
            print(f"F1-score: {f1_scores[-1]:.3f}")

        return {
            'accuracies': accuracies,
            'precisions': precisions,
            'recalls': recalls,
            'f1_scores': f1_scores,
            'accuracy_mean': np.mean(accuracies),
            'precision_mean': np.mean(precisions),
            'recall_mean': np.mean(recalls),
            'f1_mean': np.mean(f1_scores),
        }

    except Exception as e:
        print(f"Lỗi khi thực hiện cross-validation: {e}")
        return None


@app.route('/cross-validation')
def cross_validation():
    # Hiển thị dữ liệu
    data = load_data_from_db_cross_validation()
    results = perform_cross_validation(data)

    if results is None:
        return "Lỗi trong quá trình xử lý dữ liệu", 500

    return render_template(
        'cross-validation.html',
        accuracies=results["accuracies"],
        precisions=results["precisions"],
        recalls=results["recalls"],
        f1_scores=results["f1_scores"],
        accuracy_mean=results["accuracy_mean"],
        precision_mean=results["precision_mean"],
        recall_mean=results["recall_mean"],
        f1_mean=results["f1_mean"]
    )


# Chạy ứng dụng Flask
if __name__ == '__main__':
    app.run(debug=True)
