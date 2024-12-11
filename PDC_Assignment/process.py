import pandas as pd
import random
import time
from concurrent.futures import ProcessPoolExecutor
import numpy as np

# Step 1: Create CSV Files
def create_csv_files():
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
    student_fees = {
        'student_id': range(1, 101),
        'fee_paid': [random.randint(5000, 20000) for _ in range(100)],
        'fee_due': [20000 - random.randint(5000, 20000) for _ in range(100)]
    }

    df_fees = pd.DataFrame(student_fees)
    df_fees.to_csv('student_fees.csv', index=False)
    print("Created 'student_fees.csv'.")

# Step 2: Define Processing Functions
def process_serial(df):
    df['total_fee'] = df['fee_paid'] + df['fee_due']
    df['has_due'] = df['fee_due'] > 0
    return df

def process_chunk(chunk):
    chunk['total_fee'] = chunk['fee_paid'] + chunk['fee_due']
    chunk['has_due'] = chunk['fee_due'] > 0
    return chunk

def parallel_process(df, num_workers=4):
    # Split DataFrame into chunks
    chunks = np.array_split(df, num_workers)
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        processed_chunks = list(executor.map(process_chunk, chunks))
    return pd.concat(processed_chunks)

# Step 3: Main Execution
def main():
    # Create CSV files
    create_csv_files()

    # Read CSV files
    df_info = pd.read_csv('student_info.csv')
    df_fees = pd.read_csv('student_fees.csv')

    # Combine DataFrames on 'student_id'
    df_combined = pd.merge(df_info, df_fees, on='student_id')
    print("Combined DataFrames.")

    # Serial Processing
    start_time_serial = time.time()
    df_serial = process_serial(df_combined.copy())
    end_time_serial = time.time()
    serial_time = end_time_serial - start_time_serial
    print("Serial processing completed.")

    # Parallel Processing
    start_time_parallel = time.time()
    df_parallel = parallel_process(df_combined.copy(), num_workers=4)
    end_time_parallel = time.time()
    parallel_time = end_time_parallel - start_time_parallel
    print("Parallel processing completed.")

    # Display Execution Times
    print(f"Serial Processing Time: {serial_time:.4f} seconds")
    print(f"Parallel Processing Time: {parallel_time:.4f} seconds")

    # Verify Results
    if df_serial.equals(df_parallel):
        print("Both serial and parallel processing results are identical.")
    else:
        print("There is a difference between serial and parallel processing results.")

if __name__ == "__main__":
    main()
