import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report


def train_model():
    # Đọc dữ liệu
    data = pd.read_csv('heart_disease_data.csv')

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

    # Huấn luyện mô hình Naive Bayes
    model = GaussianNB()
    model.fit(X_train_scaled, y_train)

    # Dự đoán và đánh giá
    y_pred = model.predict(X_test_scaled)

    print("Độ chính xác:", accuracy_score(y_test, y_pred))
    print("\nBáo cáo chi tiết:")
    print(classification_report(y_test, y_pred, zero_division=1))

    return model


# Chạy mô hình
if __name__ == '__main__':
    train_model()
