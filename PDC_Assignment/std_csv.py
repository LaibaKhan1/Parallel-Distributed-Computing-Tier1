import pandas as pd


# Create student_info.csv
student_info = {
    'student_id': range(1, 101),  # 100 students
    'name': [f'Student_{i}' for i in range(1, 101)],
    'age': [18 + (i % 5) for i in range(1, 101)]
}

df_info = pd.DataFrame(student_info)
df_info.to_csv('student_info.csv', index=False)
print("Created 'student_info.csv'.")

# Create student_fees.csv
import random

student_fees = {
    'student_id': range(1, 101),
    'fee_paid': [random.randint(5000, 20000) for _ in range(100)],
    'fee_due': [20000 - random.randint(5000, 20000) for _ in range(100)]
}

df_fees = pd.DataFrame(student_fees)
df_fees.to_csv('student_fees.csv', index=False)
print("Created 'student_fees.csv'.")
