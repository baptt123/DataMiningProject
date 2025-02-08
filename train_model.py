#
#
# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import accuracy_score, classification_report
# import joblib
# import os
#
#
# def train_and_save_model():
#     # Đọc dữ liệu
#     data = pd.read_csv('data/heart_disease_data.csv')
#
#     # Chuyển đổi dữ liệu phân loại
#     data['gender'] = data['gender'].map({'M': 1, 'F': 0})
#     data['exercise_angina'] = data['exercise_angina'].map({'Y': 1, 'N': 0})
#
#     # Chọn đặc trưng
#     X = data[['age', 'gender', 'chest_pain_type', 'resting_blood_pressure',
#               'cholesterol', 'max_heart_rate', 'exercise_angina', 'blood_sugar']]
#     y = data['diagnosis']
#
#     # Chia tập dữ liệu
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
#     # Chuẩn hóa dữ liệu
#     scaler = StandardScaler()
#     X_train_scaled = scaler.fit_transform(X_train)
#     X_test_scaled = scaler.transform(X_test)
#
#     # Huấn luyện mô hình Random Forest
#     rf_model = RandomForestClassifier(
#         n_estimators=100,
#         random_state=42,
#         max_depth=5
#     )
#     rf_model.fit(X_train_scaled, y_train)
#
#     # Dự đoán và đánh giá
#     y_pred = rf_model.predict(X_test_scaled)
#     print("Độ chính xác:", accuracy_score(y_test, y_pred))
#     print("\nBáo cáo chi tiết:")
#     print(classification_report(y_test, y_pred, zero_division=1))
#
#     # Tạo thư mục để lưu model nếu chưa tồn tại
#     os.makedirs('model', exist_ok=True)
#
#     # Lưu model
#     joblib.dump(rf_model, 'model/heart_disease_rf_model.joblib')
#     joblib.dump(scaler, 'model/heart_disease_scaler.joblib')
#
#     print("Đã lưu model và scaler thành công!")
#
#
# def load_and_predict(new_data):
#     # Tải model và scaler
#     rf_model = joblib.load('model/heart_disease_rf_model.joblib')
#     scaler = joblib.load('model/heart_disease_scaler.joblib')
#
#     # Chuẩn hóa dữ liệu
#     new_data_scaled = scaler.transform(new_data)
#
#     # Dự đoán
#     prediction = rf_model.predict(new_data_scaled)
#     return prediction
#
#
# # Ví dụ sử dụng
# if __name__ == '__main__':
#     # Huấn luyện và lưu model
#     train_and_save_model()
#
#     # Ví dụ dự đoán
#     example_data = pd.DataFrame([
#         [55, 1, 2, 130, 250, 150, 1, 1]  # Một ví dụ về dữ liệu bệnh nhân
#     ], columns=['age', 'gender', 'chest_pain_type', 'resting_blood_pressure',
#                 'cholesterol', 'max_heart_rate', 'exercise_angina', 'blood_sugar'])
#
#     prediction = load_and_predict(example_data)
#     print("Kết quả dự đoán:", prediction)
#
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
import os
from datetime import datetime

def preprocess_data(data):
    # Create a copy of the data
    df = data.copy()

    # Convert categorical variables to numeric using LabelEncoder
    le = LabelEncoder()
    categorical_columns = ['gender', 'exercise_angina', 'blood_sugar', 'shortness_of_breath',
                          'fatigue', 'dizziness', 'family_history']

    for col in categorical_columns:
        df[col] = le.fit_transform(df[col])

    # Remove any rows with age > 120 (likely errors)
    df = df[df['age'] <= 120]

    # Remove extreme outliers in cholesterol (e.g., > 1000)
    df = df[df['cholesterol'] <= 1000]

    return df

def create_interaction_features(df):
    interactions = pd.DataFrame()
    # Add new interaction features
    interactions['age_blood_pressure_interaction'] = df['age'] * df['resting_blood_pressure']
    interactions['cholesterol_blood_pressure_interaction'] = df['cholesterol'] * df['resting_blood_pressure']
    interactions['max_heart_rate_age_interaction'] = df['max_heart_rate'] / df['age']
    interactions['chest_pain_blood_pressure_interaction'] = df['chest_pain_type'] * df['resting_blood_pressure']
    interactions['cholesterol_diagnosis_interaction'] = df['cholesterol'] * df['family_history']
    interactions['ldl_hdl_cholesterol_interaction'] = df['ldl_hdl_ratio'] * df['cholesterol']
    interactions['stress_pain_interaction'] = df['stress_level'] * df['chest_pain_frequency']
    interactions['family_history_diagnosis_interaction'] = df['family_history']
    interactions['blood_sugar_fatigue_interaction'] = df['blood_sugar'] * df['fatigue']
    interactions['chest_pain_diagnosis_interaction'] = df['chest_pain_frequency']

    return interactions

def save_model(model, scaler, feature_names, metrics, save_dir='models'):
    # Create directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Generate timestamp for unique model naming
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save the model
    model_path = os.path.join(save_dir, f'random_forest_model_{timestamp}.joblib')
    scaler_path = os.path.join(save_dir, f'scaler_{timestamp}.joblib')
    metadata_path = os.path.join(save_dir, f'model_metadata_{timestamp}.txt')

    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)

    # Save feature names and metrics
    with open(metadata_path, 'w') as f:
        f.write("Model Metadata\n")
        f.write("==============\n\n")
        f.write("Feature Names:\n")
        for feature in feature_names:
            f.write(f"- {feature}\n")

        f.write("\nModel Performance:\n")
        f.write(f"Accuracy: {metrics['accuracy']:.4f}\n")
        f.write("\nClassification Report:\n")
        f.write(metrics['classification_report'])

    print(f"\nModel saved successfully!")
    print(f"Model path: {model_path}")
    print(f"Scaler path: {scaler_path}")
    print(f"Metadata path: {metadata_path}")

    return model_path, scaler_path, metadata_path

def train_evaluate_model(data_path):
    # Read the data
    df = pd.read_csv(data_path)

    # Preprocess the data
    df_processed = preprocess_data(df)

    # Create interaction features
    interactions = create_interaction_features(df_processed)

    # Combine original features with interaction features
    feature_columns = ['age', 'gender', 'chest_pain_type', 'resting_blood_pressure',
                      'cholesterol', 'max_heart_rate', 'exercise_angina', 'blood_sugar',
                      'shortness_of_breath', 'fatigue', 'dizziness', 'chest_pain_frequency',
                      'heart_rate_variability', 'pulse_pressure', 'ldl_hdl_ratio',
                      'stress_level', 'family_history']

    X = pd.concat([df_processed[feature_columns], interactions], axis=1)
    y = df_processed['diagnosis']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Apply StandardScaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Convert back to DataFrame to keep column names
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns)

    # Initialize and train the Random Forest model with adjusted parameters
    rf_model = RandomForestClassifier(
        n_estimators=200,  # Increased number of trees
        max_depth=10,      # Increased max depth
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42
    )
    rf_model.fit(X_train_scaled, y_train)

    # Make predictions
    y_pred = rf_model.predict(X_test_scaled)

    # Calculate metrics
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'classification_report': classification_report(y_test, y_pred)
    }

    # Print metrics
    print("Model Performance Metrics:")
    print("-------------------------")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print("\nClassification Report:")
    print(metrics['classification_report'])

    # Create confusion matrix visualization
    plt.figure(figsize=(8, 6))
    sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()

    # Feature importance analysis
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\nTop 15 Most Important Features:") # Increased to show more features
    print(feature_importance.head(15))

    # Plot feature importance
    plt.figure(figsize=(14, 8))  # Increased figure size
    sns.barplot(x='importance', y='feature', data=feature_importance.head(15))
    plt.title('Top 15 Feature Importance')
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.tight_layout()
    plt.show()

    # Save the model and related components
    model_path, scaler_path, metadata_path = save_model(
        rf_model,
        scaler,
        X.columns,
        metrics
    )

    return rf_model, scaler, feature_importance, model_path, scaler_path

def load_model(model_path, scaler_path):
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

# Run the model
if __name__ == "__main__":
    data_path = "data/heart_disease_data_updated_5_2_25.csv"  # Replace with your data path
    model, scaler, feature_importance, model_path, scaler_path = train_evaluate_model(data_path)