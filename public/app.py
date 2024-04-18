from flask import Flask, request, jsonify
import joblib
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
import numpy as np

rf_model, tfidf_vectorizer_words_rf, tfidf_vectorizer_chars_rf = joblib.load(
    'rf_model_and_vectorizers.pkl')
lr_model, tfidf_vectorizer_words_lr, tfidf_vectorizer_chars_lr = joblib.load(
    'lr_model_and_vectorizers.pkl')
xgb_model, tfidf_vectorizer_words_xgb, tfidf_vectorizer_chars_xgb = joblib.load(
    'xgb_model_and_vectorizers.pkl')


app = Flask(__name__)
CORS(app)


@app.route('/classify', methods=['POST'])
def classify_comment():
    comment_text = request.json['comment']
    print(f"Input comment: {comment_text}")

    X_words_rf = tfidf_vectorizer_words_rf.transform([comment_text])
    X_chars_rf = tfidf_vectorizer_chars_rf.transform([comment_text])
    X_rf = hstack([X_words_rf, X_chars_rf])
    # Matching Training Shape
    X_extra_feature_rf = np.ones((1, 1))
    X_rf = hstack([X_rf, X_extra_feature_rf])

    X_words_lr = tfidf_vectorizer_words_lr.transform([comment_text])
    X_chars_lr = tfidf_vectorizer_chars_lr.transform([comment_text])
    X_lr = hstack([X_words_lr, X_chars_lr])
    # Matching Training Shape
    X_extra_feature_lr = np.ones((1, 1))
    X_lr = hstack([X_lr, X_extra_feature_lr])

    X_words_xgb = tfidf_vectorizer_words_xgb.transform([comment_text])
    X_chars_xgb = tfidf_vectorizer_chars_xgb.transform([comment_text])
    X_xgb = hstack([X_words_xgb, X_chars_xgb])
    # Matching Training Shape
    X_extra_feature_xgb = np.ones((1, 1))
    X_xgb = hstack([X_xgb, X_extra_feature_xgb])

    # Predictions
    rf_prediction = rf_model.predict(X_rf)[0]
    lr_prediction = lr_model.predict(X_lr)[0]
    xgb_prediction = xgb_model.predict(X_xgb)[0]

    # Convert to text label
    rf_result = 'Harmful' if rf_prediction == 1 else 'Non-harmful'
    lr_result = 'Harmful' if lr_prediction == 1 else 'Non-harmful'
    xgb_result = 'Harmful' if xgb_prediction == 1 else 'Non-harmful'

    return jsonify({'Random Forest': rf_result, 'Logistic Regression': lr_result, 'XGBoost': xgb_result})


if __name__ == '__main__':
    app.run(debug=True)
