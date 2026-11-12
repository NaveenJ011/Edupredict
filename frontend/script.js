
const API_URL = "http://127.0.0.1:5000";

const form = document.getElementById("predictionForm");
const resultBox = document.getElementById("result");
const analytics = document.getElementById("analytics");
const errorMessage = document.getElementById("errorMessage");

let performanceChart = null;

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    errorMessage.textContent = "";
    resultBox.hidden = true;
    analytics.hidden = true;

    const studentData = {
        attendance: Number(document.getElementById("attendance").value),
        study_hours: Number(document.getElementById("study_hours").value),
        previous_marks: Number(document.getElementById("previous_marks").value),
        assignment_marks: Number(document.getElementById("assignment_marks").value)
    };

    const button = form.querySelector("button");
    button.disabled = true;
    button.textContent = "Predicting...";

    try {
        const response = await fetch(`${API_URL}/api/predict`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(studentData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Prediction failed.");
        }

        document.getElementById("predictedMarks").textContent =
            data.predicted_marks + " / 100";

        document.getElementById("performanceCategory").textContent =
            "Performance: " + data.category;

        resultBox.hidden = false;
        analytics.hidden = false;

        const ctx = document.getElementById("performanceChart");

        if (performanceChart) {
            performanceChart.destroy();
        }

        performanceChart = new Chart(ctx, {
            type: "bar",

            data: {
                labels: [
                    "Attendance",
                    "Study Hours",
                    "Previous Marks",
                    "Assignment Marks",
                    "Predicted Marks"
                ],

                datasets: [{
                    label: "Student Performance",
                    data: [
                        studentData.attendance,
                        (studentData.study_hours / 24) * 100,
                        studentData.previous_marks,
                        studentData.assignment_marks,
                        data.predicted_marks
                    ],

                    backgroundColor: [
                        "#6658e8",
                        "#8d82ef",
                        "#43b5d5",
                        "#54bd91",
                        "#f2a64a"
                    ],

                    borderRadius: 7
                }]
            },

            options: {
                responsive: true,

                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,

                        title: {
                            display: true,
                            text: "Score (normalized to 100)"
                        }
                    }
                }
            }
        });

        resultBox.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

    } catch (error) {
        errorMessage.textContent =
            "Unable to connect to the prediction server. " + error.message;

    } finally {
        button.disabled = false;
        button.textContent = "Predict Performance →";
    }
});
