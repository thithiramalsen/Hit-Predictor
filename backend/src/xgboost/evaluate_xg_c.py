import pandas as pd
import joblib
import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Paths
MODEL_PATH = os.path.join("..", "..", "models", "classification", "xgb_classifier.joblib")
X_TEST_PATH = os.path.join("..", "..", "data", "X_test_cls.csv")
Y_TEST_PATH = os.path.join("..", "..", "data", "y_test_cls.csv")
REPORT_PATH = os.path.join("..", "..", "models", "classification", "confusion_matrix.png")

# Load model and test data
clf = joblib.load(MODEL_PATH)
X_test = pd.read_csv(X_TEST_PATH)
y_test = pd.read_csv(Y_TEST_PATH).values.ravel()

# Predictions
y_pred = clf.predict(X_test)

# Metrics
print("Classification Evaluation:")
print(f"Accuracy : {accuracy_score(y_test, y_pred):.3f}")
print(f"Precision: {precision_score(y_test, y_pred):.3f}")
print(f"Recall   : {recall_score(y_test, y_pred):.3f}")
print(f"F1 Score : {f1_score(y_test, y_pred):.3f}")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Non-Hit", "Hit"])
disp.plot(cmap="Blues")
plt.title("Hit vs Non-Hit Confusion Matrix")
plt.savefig(REPORT_PATH)
plt.show()
