
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# Sample student dataset
# Features: Attendance, Study Hours, Previous Marks, Assignment Marks
X = np.array([
    [90, 5, 85, 90],
    [80, 4, 75, 80],
    [70, 3, 65, 70],
    [60, 2, 55, 60],
    [95, 6, 90, 95],
    [50, 1, 45, 50],
    [85, 5, 80, 85],
    [75, 3, 70, 75],
    [65, 2, 60, 65],
    [40, 1, 35, 40],
    [88, 4, 82, 88],
    [72, 3, 68, 72],
    [55, 2, 50, 55],
    [92, 6, 88, 92],
    [78, 4, 73, 78],
    [68, 3, 63, 68],
    [82, 5, 78, 82],
    [45, 1, 40, 45],
    [97, 7, 95, 98],
    [58, 2, 52, 58]
])

# Target: Final exam marks out of 100
y = np.array([
    88, 78, 68, 58, 94,
    48, 83, 72, 63, 38,
    86, 70, 53, 92, 76,
    65, 80, 43, 98, 56
])

# Train model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)


def predict_performance(attendance, study_hours,
                        previous_marks, assignment_marks):

    features = np.array([[
        attendance,
        study_hours,
        previous_marks,
        assignment_marks
    ]])

    prediction = model.predict(features)[0]
    prediction = round(float(np.clip(prediction, 0, 100)), 2)

    if prediction >= 75:
        category = "Excellent"
    elif prediction >= 60:
        category = "Good"
    elif prediction >= 40:
        category = "Average"
    else:
        category = "Needs Improvement"

    return {
        "predicted_marks": prediction,
        "category": category
    }
