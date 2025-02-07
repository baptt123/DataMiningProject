import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os


def train_and_save_model():
    # Đọc dữ liệu
    data = pd.read_csv('data/heart_disease_data.csv')

    # Tiền xử lý dữ liệu: mã hóa các cột categorical
    data['gender'] = data['gender'].map({'M': 1, 'F': 0})
    data['exercise_angina'] = data['exercise_angina'].map({'Y': 1, 'N': 0})
    # Thêm các cột categorical và one-hot encode nó
    data['shortness_of_breath'] = data['shortness_of_breath'].map({'None': 0, 'Mild': 1, 'Moderate': 2, 'Severe': 3})
    data['fatigue'] = data['fatigue'].map({'Never': 0, 'Sometimes': 1, 'Often': 2})
    data['dizziness'] = data['dizziness'].map({'Never': 0, 'Occasional': 1, 'Often': 2})
    data['family_history'] = data['family_history'].map({'Y': 1, 'N': 0})

    # Chọn đặc trưng
    X = data[['age', 'gender', 'chest_pain_type', 'resting_blood_pressure',
              'cholesterol', 'max_heart_rate', 'exercise_angina', 'blood_sugar',
              'shortness_of_breath', 'fatigue', 'dizziness', 'chest_pain_frequency',
              'heart_rate_variability', 'pulse_pressure', 'ldl_hdl_ratio', 'stress_level', 'family_history']]
    print("Feature columns in train_model:", X.columns)  # Debugging: Print feature names
    y = data['diagnosis']

    # Chia tập dữ liệu
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Chuẩn hóa dữ liệu
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Huấn luyện mô hình Random Forest
    rf_model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=5
    )
    rf_model.fit(X_train_scaled, y_train)

    # Dự đoán và đánh giá
    y_pred = rf_model.predict(X_test_scaled)
    print("Độ chính xác:", accuracy_score(y_test, y_pred))
    print("\nBáo cáo chi tiết:")
    print(classification_report(y_test, y_pred, zero_division=1))

    # Tạo thư mục để lưu model nếu chưa tồn tại
    os.makedirs('model', exist_ok=True)

    # Lưu model
    joblib.dump(rf_model, 'model/heart_disease_rf_model.joblib')
    joblib.dump(scaler, 'model/heart_disease_scaler.joblib')

    print("Đã lưu model và scaler thành công!")


def load_and_predict(new_data):
    # Tải model và scaler
    rf_model = joblib.load('model/heart_disease_rf_model.joblib')
    scaler = joblib.load('model/heart_disease_scaler.joblib')
    # Gán lại tên cột
    # Tiền xử lý new_data:
    # Assuming the same encoding as in train_and_save_model
    if 'gender' in new_data.columns:
        new_data['gender'] = new_data['gender'].map({'M': 1, 'F': 0})
    if 'exercise_angina' in new_data.columns:
        new_data['exercise_angina'] = new_data['exercise_angina'].map({'Y': 1, 'N': 0})
    if 'shortness_of_breath' in new_data.columns:
        new_data['shortness_of_breath'] = new_data['shortness_of_breath'].map({'None': 0, 'Mild': 1, 'Moderate': 2, 'Severe': 3})
    if 'fatigue' in new_data.columns:
        new_data['fatigue'] = new_data['fatigue'].map({'Never': 0, 'Sometimes': 1, 'Often': 2})
    if 'dizziness' in new_data.columns:
        new_data['dizziness'] = new_data['dizziness'].map({'Never': 0, 'Occasional': 1, 'Often': 2})
    if 'family_history' in new_data.columns:
        new_data['family_history'] = new_data['family_history'].map({'Y': 1, 'N': 0})

    # Giữ lại những cột cần thiết
    required_columns = ['age', 'gender', 'chest_pain_type', 'resting_blood_pressure',
                       'cholesterol', 'max_heart_rate', 'exercise_angina', 'blood_sugar',
                       'shortness_of_breath', 'fatigue', 'dizziness', 'chest_pain_frequency',
                       'heart_rate_variability', 'pulse_pressure', 'ldl_hdl_ratio', 'stress_level', 'family_history']
    # Lọc ra các cột trong new_data
    new_data = new_data[required_columns]
    # Chuẩn hóa dữ liệu
    try:
        new_data_scaled = scaler.transform(new_data)
    except ValueError as e:
        print(f"Lỗi khi chuẩn hóa dữ liệu: {e}")
        print("Kiểm tra lại dữ liệu đầu vào và scaler.")
        return None  # hoặc xử lý lỗi khác tùy theo yêu cầu

    # Dự đoán
    try:
        prediction = rf_model.predict(new_data_scaled)
        return prediction
    except ValueError as e:
        print(f"Lỗi khi dự đoán: {e}")
        print("Kiểm tra lại dữ liệu đầu vào và model.")
        return None

# Ví dụ sử dụng
if __name__ == '__main__':
    # Huấn luyện và lưu model
    #  Bạn nên chạy cái này một lần để tạo model.
    train_and_save_model()


    # Ví dụ dự đoán
    example_data = pd.DataFrame([
        [55, 'M', 2, 130, 250, 150, 'Y', 1, 'None', 'Sometimes', 'Occasional', 3, 35, 45, 2.8, 7, 'Y']  # Thêm dữ liệu cho các cột mới
    ], columns=['age', 'gender', 'chest_pain_type', 'resting_blood_pressure',
                'cholesterol', 'max_heart_rate', 'exercise_angina', 'blood_sugar',
                'shortness_of_breath', 'fatigue', 'dizziness', 'chest_pain_frequency',
                'heart_rate_variability', 'pulse_pressure', 'ldl_hdl_ratio', 'stress_level', 'family_history'])

    prediction = load_and_predict(example_data)
    if prediction is not None:  # Kiểm tra xem dự đoán có thành công không
        print("Kết quả dự đoán:", prediction)
