print("================================")
print(" STUDENT PROBLEM PREDICTION ")
print("================================")

name = input("Enter Student Name: ")

study = float(input("Daily Study Hours: "))
sleep = float(input("Daily Sleep Hours: "))
attendance = float(input("Attendance Percentage: "))
marks = float(input("Previous Exam Marks: "))

print("\n--------- STUDENT DETAILS ---------")
print("Name:", name)
print("Study Hours:", study)
print("Sleep Hours:", sleep)
print("Attendance:", attendance)
print("Previous Marks:", marks)
# Lagrange Interpolation Method

def lagrange(x, y, value):

    n = len(x)
    result = 0

    for i in range(n):
        term = y[i]

        for j in range(n):
            if i != j:
                term = term * (value - x[j]) / (x[i] - x[j])

        result += term

    return result


print("\n--- LAGRANGE INTERPOLATION ---")

x = [1, 2, 4]

y = []

for i in range(3):
    marks = float(input(f"Enter marks of Test {x[i]}: "))
    y.append(marks)

predicted = lagrange(x, y, 3)

print("\nPredicted Marks of Test 3:", round(predicted, 2))
# GAUSSIAN ELIMINATION METHOD

def gaussian_elimination(A, B):

    n = len(B)

    for i in range(n):

        for j in range(i + 1, n):

            ratio = A[j][i] / A[i][i]

            for k in range(n):
                A[j][k] = A[j][k] - ratio * A[i][k]

            B[j] = B[j] - ratio * B[i]

    solution = [0] * n

    for i in range(n - 1, -1, -1):

        total = B[i]

        for j in range(i + 1, n):
            total -= A[i][j] * solution[j]

        solution[i] = total / A[i][i]

    return solution


print("\n--- GAUSSIAN ELIMINATION ---")

A = [
    [2, 7, 6],
    [4, 8, 7],
    [3, 9, 8]
]

B = [54, 71, 73]

weights = gaussian_elimination(A, B)

print("Calculated Weights:", weights)

predicted_score = (
    weights[0] * study
    + weights[1] * (attendance / 10)
    + weights[2] * (marks / 10)
)

predicted_score = max(0, min(100, predicted_score))

print("Estimated Academic Performance:",
      round(predicted_score, 2))

if predicted_score >= 75:
    print("Academic Risk: LOW")

elif predicted_score >= 50:
    print("Academic Risk: MEDIUM")

else:
    print("Academic Risk: HIGH")

# NEWTON DIVIDED DIFFERENCE

def newton_interpolation(x, y, value):

    n = len(x)
    table = [[0 for j in range(n)] for i in range(n)]

    for i in range(n):
        table[i][0] = y[i]

    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = (
                table[i + 1][j - 1] - table[i][j - 1]
            ) / (x[i + j] - x[i])

    result = table[0][0]
    product = 1

    for i in range(1, n):
        product *= (value - x[i - 1])
        result += table[0][i] * product

    return result


print("\n--- NEWTON INTERPOLATION ---")

days = [1, 2, 3, 4]
marks_data = [60, 65, 70, 75]

future_marks = newton_interpolation(
    days, marks_data, 5
)

print("Previous Marks:", marks_data)
print("Predicted Next Test Marks:", round(future_marks, 2))
# TRAPEZOIDAL RULE

def trapezoidal_rule(x, y):

    n = len(x) - 1

    h = (x[-1] - x[0]) / n

    result = y[0] + y[-1]

    for i in range(1, n):
        result += 2 * y[i]

    return (h / 2) * result


print("\n--- WEEKLY STUDY ANALYSIS ---")

days = [0, 1, 2, 3, 4, 5, 6]

study_hours = [2, 3, 2, 4, 3, 5, 4]

total_hours = trapezoidal_rule(days, study_hours)

print("Daily Study Hours:", study_hours)

print("Approximate Weekly Study Hours:",
      round(total_hours, 2))
# STUDENT PROBLEM ANALYSIS

print("\n================================")
print("       STUDENT PROBLEM ANALYSIS")
print("================================")

problems = []

if study < 3:
    problems.append("Low Study Hours")

if sleep < 7:
    problems.append("Insufficient Sleep")

if attendance < 75:
    problems.append("Low Attendance")

if marks < 50:
    problems.append("Low Academic Performance")

if len(problems) == 0:
    print("No major academic problem detected!")
else:
    print("Problems Identified:")

    for problem in problems:
        print("-", problem)

print("\nRECOMMENDATIONS")

if study < 3:
    print("- Increase daily study hours.")

if sleep < 7:
    print("- Maintain a healthy sleep schedule.")

if attendance < 75:
    print("- Improve class attendance.")

if marks < 50:
    print("- Focus on revision and practice.")

print("================================")
# STUDENT PERFORMANCE GRAPH

import matplotlib.pyplot as plt

tests = ["Test 1", "Test 2", "Test 3", "Test 4", "Test 5"]
marks_graph = [60, 65, 70, 75, 80]

plt.figure(figsize=(8, 5))

plt.plot(tests, marks_graph, marker='o')

plt.title("Student Performance Analysis")
plt.xlabel("Tests")
plt.ylabel("Marks")

plt.ylim(0, 100)
plt.grid(True)

plt.show()