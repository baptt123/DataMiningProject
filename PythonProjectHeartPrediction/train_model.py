

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

    # Chuyển đổi dữ liệu phân loại
    data['gender'] = data['gender'].map({'M': 1, 'F': 0})
    data['exercise_angina'] = data['exercise_angina'].map({'Y': 1, 'N': 0})

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

    # Chuẩn hóa dữ liệu
    new_data_scaled = scaler.transform(new_data)

    # Dự đoán
    prediction = rf_model.predict(new_data_scaled)
    return prediction


# Ví dụ sử dụng
if __name__ == '__main__':
    # Huấn luyện và lưu model
    train_and_save_model()

    # Ví dụ dự đoán
    example_data = pd.DataFrame([
        [55, 1, 2, 130, 250, 150, 1, 1]  # Một ví dụ về dữ liệu bệnh nhân
    ], columns=['age', 'gender', 'chest_pain_type', 'resting_blood_pressure',
                'cholesterol', 'max_heart_rate', 'exercise_angina', 'blood_sugar'])

    prediction = load_and_predict(example_data)
    print("Kết quả dự đoán:", prediction)

