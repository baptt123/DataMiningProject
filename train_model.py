import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report
def train_model():
    # Đọc dữ liệu từ file
    file_path = 'patient.csv'
    data = pd.read_csv(file_path)

    # Loại bỏ cột không cần thiết
    data = data.drop(columns=['patient_id'])

    # Mã hóa cột 'gender'
    data['gender'] = data['gender'].map({'Male': 0, 'Female': 1})

    # Xác định đầu vào X và nhãn y
    X = data.drop(columns=['diagnosis'])
    y = data['diagnosis']

    # Chia dữ liệu thành tập huấn luyện và kiểm tra
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

    # Huấn luyện mô hình Naive Bayes
    model = GaussianNB()
    model.fit(X_train, y_train)
    print('Train thành công ')
    save_model=joblib.dump(model, 'model_train.pkl')
    print('Đã lưu model')
    # Dự đoán trên tập kiểm tra
    y_pred = model.predict(X_test)

    # Đánh giá mô hình
    print("\nĐộ chính xác:")
    print(accuracy_score(y_test, y_pred))
    print("\nBáo cáo phân loại:")
    print(classification_report(y_test, y_pred))

if __name__=='__main__':
    train_model()