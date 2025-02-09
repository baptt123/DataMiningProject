import os
import traceback

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

# Định nghĩa danh sách các route cần kiểm tra quyền truy cập
restricted_routes = ['/chart', '/exportpdf', '/datapatient']
# Biến toàn cục để lưu mô hình và scaler
global model, scaler
app = Flask(__name__, static_folder='static')



# @app.before_request
# def check_admin():
#     # Lấy URL hiện tại và kiểm tra xem nó có trong danh sách restricted_routes không
#     if request.path in restricted_routes:
#         # Kiểm tra nếu session có chứa username và role là admin
#         if 'username' not in session or session.get('role') != 'admin':
#             flash('Bạn phải có quyền admin hoặc phải đăng nhập mói được phép truy cập', 'danger')
#             return redirect(url_for('role'))  # Chuyển hướng về trang đăng nhập
#         if 'username' not in session or session.get('role') == 'user':
#             return redirect(url_for('index'))
#
#
# # # Phân quyền đăng nhập
# @app.route('/role', methods=['GET'])
# def role():
#     return render_template('role.html')


# Routes for each HTML page
@app.route('/')
def welcome():
    return render_template('chart.html')


@app.route('/index')
def index():
    # if 'username' not in session:
    #     flash('Vui lòng đăng nhập trước.', 'warning')
    #     return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/chart', methods=['GET', 'POST'])
def chart():
    # Connect to database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Query for diagnosis distribution
    cursor.execute("""
        SELECT diagnosis, COUNT(*) 
        FROM patients_data_mining
        GROUP BY diagnosis
    """)
    heart_disease_data = cursor.fetchall()

    # Query for risk factors including new fields
    cursor.execute("""
        SELECT 
            AVG(age), AVG(resting_blood_pressure), AVG(cholesterol),
            AVG(blood_sugar), AVG(max_heart_rate), AVG(stress_level),
            AVG(ldl_hdl_ratio), AVG(pulse_pressure)
        FROM patients_data_mining
    """)
    risk_factors_data = cursor.fetchall()

    # Query for clustering analysis
    cursor.execute("""
        SELECT age, cholesterol, max_heart_rate, stress_level 
        FROM patients_data_mining
    """)
    clustering_data = cursor.fetchall()

    # Query for correlation analysis
    cursor.execute("""
        SELECT age, resting_blood_pressure, cholesterol, max_heart_rate, stress_level
        FROM patients_data_mining
        LIMIT 50
    """)
    correlation_data = cursor.fetchall()

    # Get all health metrics for model training
    query = """
        SELECT 
            age, resting_blood_pressure, cholesterol, blood_sugar, max_heart_rate,
            stress_level, ldl_hdl_ratio, pulse_pressure,
            CASE 
                WHEN chest_pain_type = '1' THEN 1
                WHEN chest_pain_type = '2' THEN 2
                WHEN chest_pain_type = '3' THEN 3
                WHEN chest_pain_type = '4' THEN 4
                ELSE 0
            END as chest_pain_type,
            CASE
                WHEN exercise_angina = 'Y' THEN 1
                ELSE 0
            END as exercise_angina,
            CASE
                WHEN shortness_of_breath = 'Severe' THEN 3
                WHEN shortness_of_breath = 'Moderate' THEN 2
                WHEN shortness_of_breath = 'None' THEN 1
                ELSE 0
            END as shortness_of_breath,
            diagnosis
        FROM patients_data_mining
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()

    # Convert to DataFrame
    columns = [
        "age", "bp", "cholesterol", "glucose", "max_heart_rate",
        "stress_level", "ldl_hdl_ratio", "pulse_pressure",
        "chest_pain_type", "exercise_angina", "shortness_of_breath",
        "diagnosis"
    ]
    df = pd.DataFrame(data, columns=columns)

    # Train Random Forest model
    X = df.drop("diagnosis", axis=1)
    y = df["diagnosis"]
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Get feature importance
    feature_importances = model.feature_importances_
    factors = [
        "Tuổi", "Huyết áp", "Cholesterol", "Đường huyết", "Nhịp tim tối đa",
        "Mức độ stress", "Tỷ lệ LDL/HDL", "Áp lực mạch",
        "Loại đau ngực", "Đau thắt ngực khi vận động", "Khó thở"
    ]
    importance_data = [{"label": factors[i], "value": feature_importances[i]} for i in range(len(factors))]

    # Clustering analysis
    from sklearn.cluster import KMeans
    import numpy as np

    clustering_array = np.array(clustering_data)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(clustering_array)
    labels = kmeans.labels_

    # Create clusters
    cluster_data = []
    for i in range(3):
        cluster = [
            {
                "age": int(clustering_array[j][0]),
                "cholesterol": int(clustering_array[j][1]),
                "heart_rate": int(clustering_array[j][2]),
                "stress": int(clustering_array[j][3])
            }
            for j in range(len(labels)) if labels[j] == i
        ]
        cluster_data.append(cluster)

    # Process correlation data
    correlation_processed = {
        "age_bp": [{"x": age, "y": bp} for age, bp, _, _, _ in correlation_data],
        "age_cholesterol": [{"x": age, "y": chol} for age, _, chol, _, _ in correlation_data],
        "heart_rate_stress": [{"x": hr, "y": stress} for _, _, _, hr, stress in correlation_data]
    }

    # Generate health recommendations based on POST data
    recommendations = []
    if request.method == 'POST':
        age = int(request.form['age'])
        heart_disease = int(request.form['heart_disease'])
        cholesterol = int(request.form['cholesterol'])
        bp = int(request.form['bp'])
        glucose = int(request.form['glucose'])
        max_heart_rate = int(request.form.get('max_heart_rate', 0))
        stress_level = int(request.form.get('stress_level', 0))

        # Age-based recommendations
        recommendations.extend(generate_age_recommendations(age))

        # Clinical metrics recommendations
        recommendations.extend(generate_clinical_recommendations(
            cholesterol, bp, glucose, max_heart_rate, stress_level
        ))

        # Heart disease specific recommendations
        if heart_disease == 1:
            recommendations.extend(generate_heart_disease_recommendations(
                cholesterol, bp, glucose, max_heart_rate, stress_level
            ))

    return render_template(
        'chart.html',
        heart_disease_data=heart_disease_data,
        risk_factors=risk_factors_data[0],
        clusters=cluster_data,
        correlation_data=correlation_processed,
        importance_data=importance_data,
        recommendations=recommendations
    )


def generate_age_recommendations(age):
    """Generate age-specific health recommendations."""
    recommendations = []
    if age < 40:
        recommendations.append("✅ Ở độ tuổi của bạn, tập trung vào phòng ngừa là quan trọng nhất:")
        recommendations.append("- Duy trì chế độ ăn uống cân bằng và lành mạnh")
        recommendations.append("- Tập thể dục đều đặn, ít nhất 150 phút/tuần")
    elif 40 <= age < 60:
        recommendations.append("⚠️ Ở độ tuổi trung niên, cần đặc biệt chú ý:")
        recommendations.append("- Kiểm tra sức khỏe định kỳ 6 tháng/lần")
        recommendations.append("- Theo dõi huyết áp và cholesterol thường xuyên")
    else:
        recommendations.append("⚠️ Ở độ tuổi cao, cần:")
        recommendations.append("- Kiểm tra sức khỏe định kỳ 3 tháng/lần")
        recommendations.append("- Tuân thủ chặt chẽ các chỉ dẫn của bác sĩ")
    return recommendations


def generate_clinical_recommendations(cholesterol, bp, glucose, heart_rate, stress):
    """Generate recommendations based on clinical metrics."""
    recommendations = []

    # Cholesterol recommendations
    if cholesterol > 200:
        recommendations.append("⚠️ Cholesterol cao:")
        recommendations.append("- Giảm thực phẩm giàu chất béo bão hòa")
        recommendations.append("- Tăng cường rau xanh và cá giàu omega-3")

    # Blood pressure recommendations
    if bp > 130:
        recommendations.append("⚠️ Huyết áp cao:")
        recommendations.append("- Hạn chế muối trong khẩu phần ăn")
        recommendations.append("- Tập thể dục nhẹ nhàng đều đặn")

    # Heart rate recommendations
    if heart_rate > 100:
        recommendations.append("⚠️ Nhịp tim cao:")
        recommendations.append("- Thực hành các bài tập thở sâu")
        recommendations.append("- Giảm caffeine và các chất kích thích")

    # Stress level recommendations
    if stress > 7:
        recommendations.append("⚠️ Mức độ stress cao:")
        recommendations.append("- Thực hành thiền hoặc yoga")
        recommendations.append("- Cân bằng thời gian làm việc và nghỉ ngơi")

    return recommendations


def generate_heart_disease_recommendations(cholesterol, bp, glucose, heart_rate, stress):
    """Generate specific recommendations for heart disease patients."""
    recommendations = []
    recommendations.append("🏥 Khuyến nghị cho bệnh nhân tim mạch:")
    recommendations.append("- Tuân thủ chặt chẽ lịch uống thuốc")
    recommendations.append("- Theo dõi và ghi chép các chỉ số sức khỏe hàng ngày")
    recommendations.append("- Tham gia các chương trình phục hồi chức năng tim mạch")
    return recommendations


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



# Đăng xuất
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Bạn đã đăng xuất', 'info')
    return redirect(url_for('login'))



# Lấy dữ liệu từ cơ sở dữ liệu
def fetch_data_from_db():
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
                    ORDER BY patient_id
                """
                cursor.execute(query)
                data = cursor.fetchall()
        return data
    except Exception as e:
        raise Exception(f"Lỗi khi load dữ liệu từ db: {str(e)}")


# Chuẩn bị đặc trưng cho từng bệnh nhân và dự đoán
def prepare_features(row):
    model = joblib.load('model/heart_disease_rf_model.joblib')
    scaler = joblib.load('model/heart_disease_scaler.joblib')

    (patient_id, age, gender, chest_pain_type, resting_blood_pressure, cholesterol, max_heart_rate, exercise_angina,
     blood_sugar, shortness_of_breath,
     fatigue, dizziness, chest_pain_frequency, heart_rate_variability, pulse_pressure, ldl_hdl_ratio, stress_level,
     family_history, diagnosis) = row
    gender_encoded = 1 if gender == 'M' else 0
    exercise_angina_encoded = 1 if exercise_angina == 'Y' else 0

    # Bạn có thể cần phải mã hóa thêm chest_pain_type nếu cần
    chest_pain_type_encoded = chest_pain_type  # Thay đổi mã hóa tùy theo cách bạn lưu trữ giá trị này

    features = pd.DataFrame([[age, gender_encoded, chest_pain_type_encoded,
                              resting_blood_pressure, cholesterol,
                              max_heart_rate, exercise_angina_encoded, blood_sugar, shortness_of_breath,
                              fatigue, dizziness, chest_pain_frequency, heart_rate_variability, pulse_pressure,
                              ldl_hdl_ratio, stress_level, family_history, ]],
                            columns=['age', 'gender', 'chest_pain_type',
                                     'resting_blood_pressure', 'cholesterol',
                                     'max_heart_rate', 'exercise_angina', 'blood_sugar', 'shortness_of_breath',
                                     'fatigue', 'dizziness', 'chest_pain_frequency',
                                     'heart_rate_variability', 'pulse_pressure', 'ldl_hdl_ratio', 'stress_level',
                                     'family_history', 'diagnosis'
                                     ])
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]
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
    'password': '',  # Thay bằng password MySQL của bạn
    'database': 'data mining project minh thong',  # Thay bằng tên database của bạn
}


# def preprocess_data(data):
#     """Tiền xử lý dữ liệu"""
#     # Xử lý các giá trị null
#     data = data.dropna()  # Đánh dấu và loại bỏ các giá trị null
#     # Kiểm tra và lọc các giá trị bất thường
#     valid_genders = {'M', 'F'}
#     data = data[data['gender'].isin(valid_genders)]  # Loại bỏ giá trị không hợp lệ
#
#     valid_yes_no = {'Y', 'N'}
#     for col in ['exercise_angina', 'family_history']:
#         data = data[data[col].isin(valid_yes_no)]  # Chỉ giữ các giá trị 'Y' hoặc 'N'
#
#     valid_levels = {
#         'blood_sugar': {'Very High', 'Normal', 'High'},
#         'shortness_of_breath': {'Severe', 'None', 'Moderate'},
#         'fatigue': {'Never', 'Sometime', 'Often'},
#         'dizziness': {'Never', 'Occasional', 'Often'}
#     }
#
#     for col, valid_set in valid_levels.items():
#         data = data[data[col].isin(valid_set)]  # Loại bỏ các giá trị ngoài danh mục hợp lệ
#     # mã hóa dữ liệu phân loại
#     data['gender'] = data['gender'].map({'M': 1, 'F': 0})
#     data['exercise_angina'] = data['exercise_angina'].map({'Y': 1, 'N': 0})
#     data['blood_sugar'] = data['blood_sugar'].map({'Very High': 2, 'Normal': 0, 'High': 1})
#     data['shortness_of_breath'] = data['shortness_of_breath'].map({'Severe': 2, 'None': 0, 'Moderate': 1})
#     data['fatigue'] = data['fatigue'].map({'Often': 1, 'Never': 0, 'Sometime': 2})
#     data['dizziness'] = data['dizziness'].map({'Never': 0, 'Occasional': 1, 'Often': 2})
#     data['family_history'] = data['family_history'].map({'Y': 1, 'N': 0})
#
#     # Xử lý outlier bằng Z-score
#     numeric_cols = data.select_dtypes(include=[np.number]).columns  # Chỉ lấy các cột số
#     z_scores = np.abs(zscore(data[numeric_cols]))  # Tính Z-score
#     data = data[(z_scores < 3).all(axis=1)]  # Giữ lại các dòng có Z-score < 3
#     return data


def preprocess_data(data):
    """
    Tiền xử lý dữ liệu và tạo các đặc trưng tương tác
    """
    # Xử lý các giá trị null
    data = data.dropna()

    # Kiểm tra và lọc các giá trị bất thường
    valid_genders = {'M', 'F'}
    data = data[data['gender'].isin(valid_genders)]

    valid_yes_no = {'Y', 'N'}
    for col in ['exercise_angina', 'family_history']:
        data = data[data[col].isin(valid_yes_no)]

    valid_levels = {
        'blood_sugar': {'Very High', 'Normal', 'High'},
        'shortness_of_breath': {'Severe', 'None', 'Moderate'},
        'fatigue': {'Never', 'Sometime', 'Often'},
        'dizziness': {'Never', 'Occasional', 'Often'}
    }

    for col, valid_set in valid_levels.items():
        data = data[data[col].isin(valid_set)]

    # Mã hóa dữ liệu phân loại
    encoding_maps = {
        'gender': {'M': 1, 'F': 0},
        'exercise_angina': {'Y': 1, 'N': 0},
        'blood_sugar': {'Very High': 2, 'Normal': 0, 'High': 1},
        'shortness_of_breath': {'Severe': 2, 'None': 0, 'Moderate': 1},
        'fatigue': {'Often': 1, 'Never': 0, 'Sometime': 2},
        'dizziness': {'Never': 0, 'Occasional': 1, 'Often': 2},
        'family_history': {'Y': 1, 'N': 0}
    }

    for col, encoding in encoding_maps.items():
        data[col] = data[col].map(encoding)

    # Xử lý outlier bằng Z-score
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    z_scores = np.abs(zscore(data[numeric_cols]))
    data = data[(z_scores < 3).all(axis=1)]

    # Tạo các đặc trưng tương tác
    data['age_blood_pressure_interaction'] = data['age'] * data['resting_blood_pressure']
    data['cholesterol_blood_pressure_interaction'] = data['cholesterol'] * data['resting_blood_pressure']
    data['max_heart_rate_age_interaction'] = data['max_heart_rate'] / data['age']
    data['chest_pain_blood_pressure_interaction'] = data['chest_pain_type'] * data['resting_blood_pressure']
    data['cholesterol_diagnosis_interaction'] = data['cholesterol'] * data['family_history']
    data['ldl_hdl_cholesterol_interaction'] = data['ldl_hdl_ratio'] * data['cholesterol']
    data['stress_pain_interaction'] = data['stress_level'] * data['chest_pain_frequency']
    data['family_history_diagnosis_interaction'] = data['family_history'] * 1
    data['blood_sugar_fatigue_interaction'] = data['blood_sugar'] * data['fatigue']
    data['chest_pain_diagnosis_interaction'] = data['chest_pain_frequency'] * 1

    # Sắp xếp các cột theo thứ tự
    feature_columns = [
        'age', 'gender', 'chest_pain_type', 'resting_blood_pressure', 'cholesterol',
        'max_heart_rate', 'exercise_angina', 'blood_sugar', 'shortness_of_breath',
        'fatigue', 'dizziness', 'chest_pain_frequency', 'heart_rate_variability',
        'pulse_pressure', 'ldl_hdl_ratio', 'stress_level', 'family_history',
        'age_blood_pressure_interaction', 'cholesterol_blood_pressure_interaction',
        'max_heart_rate_age_interaction', 'chest_pain_blood_pressure_interaction',
        'cholesterol_diagnosis_interaction', 'ldl_hdl_cholesterol_interaction',
        'stress_pain_interaction', 'family_history_diagnosis_interaction',
        'blood_sugar_fatigue_interaction', 'chest_pain_diagnosis_interaction'
    ]

    return data[feature_columns]

def save_to_db(age, gender, chest_pain_type, resting_blood_pressure, cholesterol,
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
        (patient_id, age, gender, chest_pain_type, resting_blood_pressure, cholesterol, 
         max_heart_rate, exercise_angina, blood_sugar, shortness_of_breath, fatigue, dizziness, chest_pain_frequency, heart_rate_variability
                , pulse_pressure, ldl_hdl_ratio,stress_level, family_history, diagnosis)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (new_id, age, gender, chest_pain_type, resting_blood_pressure,
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


def load_data_from_db():
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










# === Hàm chuyển đổi giá trị sang chuỗi tiếng Anh ===
def convert_blood_sugar(value):
    return {1: "Normal", 2: "High", 3: "Very High", 4: "Low"}.get(value, "Unknown")

def convert_shortness_of_breath(value):
    return {1: "None", 2: "Severe", 3: "Moderate"}.get(value, "Unknown")

def convert_fatigue(value):
    return {1: "None", 2: "Sometimes", 3: "Often"}.get(value, "Unknown")

def convert_dizziness(value):
    return {1: "None", 2: "Occasional", 3: "Often"}.get(value, "Unknown")

# @app.route('/predict_heart', methods=['POST', 'GET'])
# def predict_heart():
#     try:
#         if request.method == 'POST':
#             # Tải mô hình và scaler
#             model = joblib.load('models/random_forest_model_20250208_175102.joblib')
#             scaler = joblib.load('models/scaler_20250208_175102.joblib')
#
#             # Lấy dữ liệu từ form
#             age = int(request.form['age'])
#             gender = request.form['gender']
#             chest_pain_type = int(request.form['chest_pain_type'])
#             resting_blood_pressure = int(request.form['resting_blood_pressure'])
#             cholesterol = int(request.form['cholesterol'])
#             max_heart_rate = int(request.form['max_heart_rate'])
#             exercise_angina = request.form['exercise_angina']
#             blood_sugar = int(request.form['blood_sugar'])
#             shortness_of_breath = int(request.form['shortness_of_breath'])
#             fatigue = int(request.form['fatigue'])
#             dizziness = int(request.form['dizziness'])
#             chest_pain_frequency = int(request.form['chest_pain_frequency'])
#             heart_rate_variability = int(request.form['heart_rate_variability'])
#             pulse_pressure = int(request.form['pulse_pressure'])
#             ldl_hdl_ratio = float(request.form['ldl_hdl_ratio'])
#             stress_level = int(request.form['stress_level'])
#             family_history = int(request.form['family_history'])
#
#             # Chuyển đổi giá trị sang chuỗi tiếng Anh
#             blood_sugar_str = convert_blood_sugar(blood_sugar)
#             shortness_of_breath_str = convert_shortness_of_breath(shortness_of_breath)
#             fatigue_str = convert_fatigue(fatigue)
#             dizziness_str = convert_dizziness(dizziness)
#
#             # Mã hóa các thuộc tính
#             gender_encoded = 1 if gender == 'M' else 0
#             exercise_angina_encoded = 1 if exercise_angina == 'Y' else 0
#
#             # === Thêm các đặc trưng tương tác ===
#             age_blood_pressure_interaction = age * resting_blood_pressure
#             cholesterol_blood_pressure_interaction = cholesterol * resting_blood_pressure
#             max_heart_rate_age_interaction = max_heart_rate / age
#             chest_pain_blood_pressure_interaction = chest_pain_type * resting_blood_pressure
#             cholesterol_diagnosis_interaction = cholesterol * family_history
#             ldl_hdl_cholesterol_interaction = ldl_hdl_ratio * cholesterol
#             stress_pain_interaction = stress_level * chest_pain_frequency
#             family_history_diagnosis_interaction = family_history * 1  # Giữ nguyên do nó đã binary
#             blood_sugar_fatigue_interaction = blood_sugar * fatigue
#             chest_pain_diagnosis_interaction = chest_pain_frequency * 1  # Giữ nguyên do nó có ý nghĩa trực tiếp
#
#             # Chuẩn bị dữ liệu để dự đoán
#             features = pd.DataFrame([[
#                 age, gender_encoded, chest_pain_type, resting_blood_pressure, cholesterol, max_heart_rate,
#                 exercise_angina_encoded, blood_sugar, shortness_of_breath, fatigue, dizziness, chest_pain_frequency,
#                 heart_rate_variability, pulse_pressure, ldl_hdl_ratio, stress_level, family_history,
#                 # Thêm các đặc trưng mới
#                 age_blood_pressure_interaction, cholesterol_blood_pressure_interaction, max_heart_rate_age_interaction,
#                 chest_pain_blood_pressure_interaction, cholesterol_diagnosis_interaction,
#                 ldl_hdl_cholesterol_interaction, stress_pain_interaction, family_history_diagnosis_interaction,
#                 blood_sugar_fatigue_interaction, chest_pain_diagnosis_interaction
#             ]], columns=[
#                 'age', 'gender', 'chest_pain_type', 'resting_blood_pressure', 'cholesterol', 'max_heart_rate',
#                 'exercise_angina', 'blood_sugar', 'shortness_of_breath', 'fatigue', 'dizziness', 'chest_pain_frequency',
#                 'heart_rate_variability', 'pulse_pressure', 'ldl_hdl_ratio', 'stress_level', 'family_history',
#                 # Tên cột cho các đặc trưng mới
#                 'age_blood_pressure_interaction', 'cholesterol_blood_pressure_interaction', 'max_heart_rate_age_interaction',
#                 'chest_pain_blood_pressure_interaction', 'cholesterol_diagnosis_interaction',
#                 'ldl_hdl_cholesterol_interaction', 'stress_pain_interaction', 'family_history_diagnosis_interaction',
#                 'blood_sugar_fatigue_interaction', 'chest_pain_diagnosis_interaction'
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
#                 age=age, gender=gender, chest_pain_type=chest_pain_type, resting_blood_pressure=resting_blood_pressure,
#                 cholesterol=cholesterol, max_heart_rate=max_heart_rate, exercise_angina=exercise_angina,
#                 blood_sugar=blood_sugar, shortness_of_breath=shortness_of_breath, fatigue=fatigue, dizziness=dizziness,
#                 chest_pain_frequency=chest_pain_frequency, heart_rate_variability=heart_rate_variability,
#                 pulse_pressure=pulse_pressure, ldl_hdl_ratio=ldl_hdl_ratio, stress_level=stress_level,
#                 family_history=family_history, diagnosis=result
#             )
#
#             # Huấn luyện lại mô hình với dữ liệu mới từ DB (nếu cần)
#             # data = load_data_from_db()
#             # if len(data) > 100:  # Tránh huấn luyện lại khi dữ liệu chưa đủ lớn
#             #     train_model(data)
#
#             # Trả kết quả về dưới dạng JSON
#             return jsonify({
#                 'diagnosis': result,
#                 'blood_sugar': blood_sugar_str,
#                 'shortness_of_breath': shortness_of_breath_str,
#                 'fatigue': fatigue_str,
#                 'dizziness': dizziness_str
#             })
#
#         # Nếu phương thức là GET, hiển thị form
#         return render_template('predict.html')
#
#     except Exception as e:
#         print(f"Error occurred: {str(e)}")
#         return jsonify({'error': f'Có lỗi xảy ra: {str(e)}'}), 500

@app.route('/predict_heart', methods=['POST', 'GET'])
def predict_heart():
    try:
        if request.method == 'POST':
            # Load model and scaler
            model = joblib.load('models/random_forest_model_20250208_175102.joblib')
            scaler = joblib.load('models/scaler_20250208_175102.joblib')
            age=int(request.form['age']),
            cholesterol=int(request.form['cholesterol']),
            resting_blood_pressure=int(request.form['resting_blood_pressure']),
            max_heart_rate=int(request.form['max_heart_rate']),
            exercise_angina_encoded=int(request.form['exercise_angina']),
            blood_sugar=int(request.form['blood_sugar']),
            # Create input DataFrame with categorical values
            input_data = pd.DataFrame([{
                'age': int(request.form['age']),
                'gender': 'M' if request.form['gender'] == 'M' else 'F',
                'chest_pain_type': int(request.form['chest_pain_type']),
                'resting_blood_pressure': int(request.form['resting_blood_pressure']),
                'cholesterol': int(request.form['cholesterol']),
                'max_heart_rate': int(request.form['max_heart_rate']),
                'exercise_angina': 'Y' if request.form['exercise_angina'] == 'Y' else 'N',
                'blood_sugar': {2: 'Very High', 0: 'Normal', 1: 'High'}[int(request.form['blood_sugar'])],
                'shortness_of_breath': {2: 'Severe', 0: 'None', 1: 'Moderate'}[int(request.form['shortness_of_breath'])],
                'fatigue': {1: 'Often', 0: 'Never', 2: 'Sometime'}[int(request.form['fatigue'])],
                'dizziness': {0: 'Never', 1: 'Occasional', 2: 'Often'}[int(request.form['dizziness'])],
                'chest_pain_frequency': int(request.form['chest_pain_frequency']),
                'heart_rate_variability': int(request.form['heart_rate_variability']),
                'pulse_pressure': int(request.form['pulse_pressure']),
                'ldl_hdl_ratio': float(request.form['ldl_hdl_ratio']),
                'stress_level': int(request.form['stress_level']),
                'family_history': 'Y' if int(request.form['family_history']) == 1 else 'N'
            }])

            # Store original string values for response
            blood_sugar_str = convert_blood_sugar(int(request.form['blood_sugar']))
            shortness_of_breath_str = convert_shortness_of_breath(int(request.form['shortness_of_breath']))
            fatigue_str = convert_fatigue(int(request.form['fatigue']))
            dizziness_str = convert_dizziness(int(request.form['dizziness']))

            # Preprocess the input data
            processed_data = preprocess_data(input_data)

            # Scale features
            features_scaled = scaler.transform(processed_data)

            # Make prediction
            prediction = model.predict(features_scaled)[0]
            result = 1 if prediction == 1 else 0

            # Save to database
            save_to_db(
                age=int(request.form['age']),
                gender=request.form['gender'],
                chest_pain_type=int(request.form['chest_pain_type']),
                resting_blood_pressure=int(request.form['resting_blood_pressure']),
                cholesterol=int(request.form['cholesterol']),
                max_heart_rate=int(request.form['max_heart_rate']),
                exercise_angina=request.form['exercise_angina'],
                blood_sugar=int(request.form['blood_sugar']),
                shortness_of_breath=int(request.form['shortness_of_breath']),
                fatigue=int(request.form['fatigue']),
                dizziness=int(request.form['dizziness']),
                chest_pain_frequency=int(request.form['chest_pain_frequency']),
                heart_rate_variability=int(request.form['heart_rate_variability']),
                pulse_pressure=int(request.form['pulse_pressure']),
                ldl_hdl_ratio=float(request.form['ldl_hdl_ratio']),
                stress_level=int(request.form['stress_level']),
                family_history=int(request.form['family_history']),
                diagnosis=result
            )
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
            return jsonify({
                'diagnosis': result,
                'blood_sugar': blood_sugar_str,
                'shortness_of_breath': shortness_of_breath_str,
                'fatigue': fatigue_str,
                'dizziness': dizziness_str
            })

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

# hàm thực hiện cross validation
def perform_cross_validation(data):
    """
    Thực hiện cross-validation trên dữ liệu trước khi huấn luyện mô hình chính thức
    """
    try:
        # Tiền xử lý dữ liệu và tạo đặc trưng tương tác
        processed_data = preprocess_data(data)

        # Tách features và target
        feature_columns = [
            'age', 'gender', 'chest_pain_type', 'resting_blood_pressure', 'cholesterol',
            'max_heart_rate', 'exercise_angina', 'blood_sugar', 'shortness_of_breath',
            'fatigue', 'dizziness', 'chest_pain_frequency', 'heart_rate_variability',
            'pulse_pressure', 'ldl_hdl_ratio', 'stress_level', 'family_history',
            'age_blood_pressure_interaction', 'cholesterol_blood_pressure_interaction',
            'max_heart_rate_age_interaction', 'chest_pain_blood_pressure_interaction',
            'cholesterol_diagnosis_interaction', 'ldl_hdl_cholesterol_interaction',
            'stress_pain_interaction', 'family_history_diagnosis_interaction',
            'blood_sugar_fatigue_interaction', 'chest_pain_diagnosis_interaction'
        ]

        X = processed_data[feature_columns]
        y = data['diagnosis']  # Sử dụng target từ dữ liệu gốc

        # Khởi tạo các công cụ cần thiết
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        scaler = StandardScaler()
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=5
        )

        # Khởi tạo lists để lưu kết quả
        metrics = {
            'accuracies': [],
            'precisions': [],
            'recalls': [],
            'f1_scores': []
        }

        # Thực hiện cross-validation
        for fold, (train_idx, val_idx) in enumerate(cv.split(X, y), 1):
            # Chia dữ liệu
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

            # Chuẩn hóa dữ liệu
            X_train_scaled = scaler.fit_transform(X_train)
            X_val_scaled = scaler.transform(X_val)

            # Huấn luyện và dự đoán
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_val_scaled)

            # Tính toán và lưu các metrics
            metrics['accuracies'].append(accuracy_score(y_val, y_pred))
            metrics['precisions'].append(precision_score(y_val, y_pred, zero_division=0))
            metrics['recalls'].append(recall_score(y_val, y_pred, zero_division=0))
            metrics['f1_scores'].append(f1_score(y_val, y_pred, zero_division=0))

            # In kết quả của fold hiện tại
            print(f"\nKết quả fold {fold}:")
            print(f"Accuracy: {metrics['accuracies'][-1]:.3f}")
            print(f"Precision: {metrics['precisions'][-1]:.3f}")
            print(f"Recall: {metrics['recalls'][-1]:.3f}")
            print(f"F1-score: {metrics['f1_scores'][-1]:.3f}")

        # Tính toán kết quả tổng hợp
        results = {}
        for metric_name in metrics:
            base_name = metric_name[:-3]  # Remove 'ies' from the end
            results[f'{base_name}_mean'] = np.mean(metrics[metric_name])
            results[f'{base_name}_std'] = np.std(metrics[metric_name])

        # In kết quả tổng hợp
        print("\nKết quả cross-validation tổng hợp:")
        print(f"Accuracy: {results['accuracy_mean']:.3f} (±{results['accuracy_std']:.3f})")
        print(f"Precision: {results['precision_mean']:.3f} (±{results['precision_std']:.3f})")
        print(f"Recall: {results['recall_mean']:.3f} (±{results['recall_std']:.3f})")
        print(f"F1-score: {results['f1_mean']:.3f} (±{results['f1_std']:.3f})")

        return results

    except Exception as e:
        print(f"Lỗi khi thực hiện cross-validation: {e}")
        traceback.print_exc()  # In ra stack trace để debug
        return None
@app.route("/datauser")
def datauser():
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Fetch results as dictionary

        # Query to get all patients
        cursor.execute("SELECT * FROM patients_data_mining")
        patients = cursor.fetchall()

        # Close the connection
        cursor.close()
        conn.close()
        print('Dữ liệu:',patients)
        return render_template('datauser.html', patients=patients)

    except Error as e:
        return f"Error connecting to MySQL database: {e}"

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
# Chạy ứng dụng Flask
if __name__ == '__main__':
    app.run(debug=True)
