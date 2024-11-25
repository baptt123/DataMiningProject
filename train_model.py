import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report
import joblib
def train_model():
    # Đọc dữ liệu từ file CSV
    data = pd.read_csv('heart_disease_data.csv')

    # Xử lý dữ liệu (chuyển đổi giá trị phân loại thành số)
    data['gender'] = data['gender'].map({'M': 1, 'F': 0})
    data['exercise_angina'] = data['exercise_angina'].map({'Y': 1, 'N': 0})

    # Chọn đầu vào (features) và đầu ra (target)
    X = data[['age', 'gender', 'chest_pain_type', 'resting_blood_pressure',
              'cholesterol', 'max_heart_rate', 'exercise_angina', 'blood_sugar']]
    y = data['diagnosis']

    # Chia dữ liệu thành tập huấn luyện và kiểm tra
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Khởi tạo và huấn luyện mô hình Naive Bayes
    model = GaussianNB()
    model.fit(X_train, y_train)

    # Lưu mô hình vào file
    joblib.dump(model, 'naive_bayes_model.pkl')
    print("Mô hình đã được lưu vào 'naive_bayes_model.pkl'")

    # Dự đoán trên tập kiểm tra
    y_pred = model.predict(X_test)

    # Đánh giá mô hình
    print("Độ chính xác:", accuracy_score(y_test, y_pred))
    print("Báo cáo phân loại:\n", classification_report(y_test, y_pred))
    # Tải lại mô hình đã lưu
    loaded_model = joblib.load('naive_bayes_model.pkl')
    print("\nĐã tải lại mô hình từ file.")
    y_loaded_pred = loaded_model.predict(X_test)

    # Kiểm tra kết quả dự đoán với mô hình đã tải
    print("Độ chính xác với mô hình đã tải:", accuracy_score(y_test, y_loaded_pred))
if __name__ == '__main__':
    train_model()