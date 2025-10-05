import pandas as pd
import numpy as np
import joblib
import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, precision_recall_curve, f1_score, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Paths
MODEL_PATH = os.path.join("models", "xgboost", "model_xg_c.joblib")
PREPROC_PATH = os.path.join("models", "xgboost", "preprocessor_xg_c.joblib")
X_TEST_PATH = os.path.join("..", "..", "data", "X_test_cls.csv")
Y_TEST_PATH = os.path.join("..", "..", "data", "y_test_cls.csv")
REPORT_PATH = os.path.join("..", "..", "models", "classification", "confusion_matrix.png")

# Load model and test data
clf = joblib.load(MODEL_PATH)
X_test = pd.read_csv(X_TEST_PATH)
y_test = pd.read_csv(Y_TEST_PATH).values.ravel()

# Load and apply preprocessor
preproc = joblib.load(os.path.join("models", "xgboost", "preprocessor_xg_c.joblib"))
X_test_preproc = preproc.transform(X_test)

# Predictions
y_pred = clf.predict(X_test_preproc)

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


y_probs = clf.predict_proba(X_test_preproc)[:, 1]  # predicted probabilities for "Hit"
precisions, recalls, thresholds = precision_recall_curve(y_test, y_probs)

f1_scores = np.where((precisions + recalls) > 0,
                     2 * (precisions * recalls) / (precisions + recalls),
                     0)
best_idx = f1_scores[:-1].argmax()  # ignore the last precision=1 point
best_threshold = thresholds[best_idx]


print("Best threshold:", best_threshold)
print("Best F1:", f1_scores[best_idx])


# Apply best threshold
y_pred_best = (y_probs >= best_threshold).astype(int)

print("\nRe-evaluated with Best Threshold:")
print(f"Accuracy : {accuracy_score(y_test, y_pred_best):.3f}")
print(f"Precision: {precision_score(y_test, y_pred_best):.3f}")
print(f"Recall   : {recall_score(y_test, y_pred_best):.3f}")
print(f"F1 Score : {f1_score(y_test, y_pred_best):.3f}")

# Confusion matrix at best threshold
cm_best = confusion_matrix(y_test, y_pred_best)
disp_best = ConfusionMatrixDisplay(confusion_matrix=cm_best, display_labels=["Non-Hit", "Hit"])
disp_best.plot(cmap="Purples")
plt.title(f"Confusion Matrix (Threshold={best_threshold:.2f})")
plt.show()
