# import mysql.connector
# import pandas as pd
# import numpy as np
# import joblib
# import os
# from flask import Flask, render_template
# from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
# from mlxtend.frequent_patterns import apriori, association_rules
#
# app = Flask(__name__)
#
# # Thông tin kết nối cơ sở dữ liệu
# db_config = {
#     'user': 'root',
#     'password': 'your_password',
#     'host': 'localhost',
#     'database': 'your_database',
# }
#
#
# # Lấy dữ liệu từ cơ sở dữ liệu
# def fetch_data_from_db():
#     try:
#         with mysql.connector.connect(**db_config) as conn:
#             with conn.cursor() as cursor:
#                 query = """
#                     SELECT
#                         patient_id,
#                         age,
#                         CASE
#                             WHEN gender = 'M' THEN 'Nam'
#                             WHEN gender = 'F' THEN 'Nữ'
#                             ELSE gender
#                         END as gender,
#                         chest_pain_type,
#                         resting_blood_pressure,
#                         cholesterol,
#                         max_heart_rate,
#                         CASE
#                             WHEN exercise_angina = 'Y' THEN 'Có'
#                             WHEN exercise_angina = 'N' THEN 'Không'
#                             ELSE exercise_angina
#                         END as exercise_angina,
#                         blood_sugar,
#                         diagnosis
#                     FROM patients_data_mining
#                     ORDER BY patient_id
#                 """
#                 cursor.execute(query)
#                 data = cursor.fetchall()
#         return data
#     except Exception as e:
#         raise Exception(f"Lỗi khi load dữ liệu từ db: {str(e)}")
#
#
# # Áp dụng L-Diversity để bảo vệ quyền riêng tư
# def apply_l_diversity(df, quasi_identifiers, sensitive_attribute, l_value=2):
#     # Phân nhóm dữ liệu theo các thuộc tính nhận dạng (quasi-identifiers)
#     grouped = df.groupby(quasi_identifiers)
#
#     for group, group_data in grouped:
#         # Kiểm tra tính đa dạng của thuộc tính nhạy cảm trong mỗi nhóm
#         unique_values = group_data[sensitive_attribute].nunique()
#
#         # Nếu số lượng giá trị khác nhau ít hơn L, thay đổi hoặc xóa nhóm này
#         if unique_values < l_value:
#             # Bạn có thể áp dụng các chiến lược bảo vệ quyền riêng tư ở đây (ví dụ: thay đổi, xóa bản ghi)
#             print(f"Nhóm {group} không đủ {l_value} đa dạng cho thuộc tính nhạy cảm.")
#
#     return df
#
#
# # Chuyển dữ liệu thành dạng nhị phân cho khai phá luật kết hợp
# def create_binary_data(df):
#     for col in df.columns:
#         df[col] = df[col].apply(lambda x: 1 if x > df[col].mean() else 0)
#     return df
#
#
# # Sinh luật kết hợp từ dữ liệu
# def generate_association_rules(data):
#     df = pd.DataFrame(data, columns=['patient_id', 'age', 'gender', 'chest_pain_type',
#                                      'resting_blood_pressure', 'cholesterol', 'max_heart_rate',
#                                      'exercise_angina', 'blood_sugar', 'diagnosis'])
#
#     # Áp dụng L-Diversity để đảm bảo tính riêng tư
#     df = apply_l_diversity(df, ['age', 'gender', 'chest_pain_type'], 'diagnosis', l_value=2)
#
#     # Chuyển dữ liệu thành dạng nhị phân
#     binary_data = create_binary_data(df.drop(columns=['patient_id']))  # Bỏ cột patient_id không cần thiết cho Apriori
#
#     # Áp dụng Apriori để tìm các itemsets phổ biến
#     frequent_itemsets = apriori(binary_data, min_support=0.1, use_colnames=True)
#
#     # Tạo các luật kết hợp
#     rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
#
#     if len(rules) > 0:
#         return rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
#     else:
#         return None
#
#
# # Chuẩn bị đặc trưng cho từng bệnh nhân và dự đoán
# def prepare_features(row):
#     model = joblib.load('model/heart_disease_rf_model.joblib')
#     scaler = joblib.load('model/heart_disease_scaler.joblib')
#
#     patient_id, age, gender, chest_pain_type, resting_blood_pressure, cholesterol, max_heart_rate, exercise_angina, blood_sugar, diagnosis = row
#     gender_encoded = 1 if gender == 'Nam' else 0
#     exercise_angina_encoded = 1 if exercise_angina == 'Có' else 0
#
#     chest_pain_type_encoded = chest_pain_type  # Thay đổi mã hóa tùy theo cách bạn lưu trữ giá trị này
#
#     features = pd.DataFrame([[age, gender_encoded, chest_pain_type_encoded,
#                               resting_blood_pressure, cholesterol,
#                               max_heart_rate, exercise_angina_encoded, blood_sugar]],
#                             columns=['age', 'gender', 'chest_pain_type',
#                                      'resting_blood_pressure', 'cholesterol',
#                                      'max_heart_rate', 'exercise_angina', 'blood_sugar'])
#     features_scaled = scaler.transform(features)
#     prediction = model.predict(features_scaled)[0]
#     return {
#         'patient_id': patient_id,
#         'age': age,
#         'gender': gender,
#         'chest_pain_type': chest_pain_type,
#         'resting_blood_pressure': resting_blood_pressure,
#         'cholesterol': cholesterol,
#         'max_heart_rate': max_heart_rate,
#         'exercise_angina': exercise_angina,
#         'blood_sugar': blood_sugar,
#         'prediction': int(prediction),
#         'diagnosis': diagnosis
#     }
#
#
# # Tính toán các chỉ số hiệu suất của mô hình
# def calculate_metrics(true_labels, predicted_labels):
#     accuracy = accuracy_score(true_labels, predicted_labels)
#     precision = precision_score(true_labels, predicted_labels, average='binary', pos_label=1, zero_division=0)
#     recall = recall_score(true_labels, predicted_labels, average='binary', pos_label=1, zero_division=0)
#     f1 = f1_score(true_labels, predicted_labels, average='binary', pos_label=1, zero_division=0)
#     cm = confusion_matrix(true_labels, predicted_labels)
#
#     return accuracy, precision, recall, f1, cm
#
#
# # Chuyển đổi confusion matrix thành DataFrame
# def convert_cm_to_df(cm):
#     cm_df = pd.DataFrame(cm, columns=["Predicted Negative", "Predicted Positive"],
#                          index=["True Negative", "True Positive"])
#     return cm_df
#
#
# # Route chính để xuất báo cáo PDF
# @app.route('/exportpdf')
# def export_pdf():
#     try:
#         data = fetch_data_from_db()
#         results = [prepare_features(row) for row in data]
#
#         true_labels = [row['diagnosis'] for row in results]  # Lấy nhãn thực tế
#         predicted_labels = [row['prediction'] for row in results]  # Lấy nhãn dự đoán
#
#         # Tính toán các chỉ số hiệu suất
#         accuracy, precision, recall, f1, cm = calculate_metrics(true_labels, predicted_labels)
#         cm_df = convert_cm_to_df(cm)
#
#         # Sinh ra các luật kết hợp
#         rules = generate_association_rules(data)
#
#         if rules is not None:
#             rules_html = rules.to_html()
#         else:
#             rules_html = "Không có luật kết hợp nào tìm thấy."
#
#         return render_template('exportpdf.html', data=results, accuracy=accuracy,
#                                precision=precision, recall=recall, f1=f1, cm=cm_df.to_html(),
#                                rules=rules_html)
#     except Exception as e:
#         return f"Lỗi khi lấy dữ liệu hoặc sinh luật kết hợp: {str(e)}"
#
#
# if __name__ == "__main__":
#     app.run(debug=True)
