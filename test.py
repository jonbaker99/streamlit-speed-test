import streamlit as st
import pandas as pd
import time
import numpy as np

st.title('CSV vs Parquet Read/Write Speed Test')

# Option to upload a file or generate source data
data_source = st.radio(
    "Choose the source of your data:",
    ('Upload a file', 'Generate random data')
)

# Function to generate random data
def generate_data(rows, cols):
    columns = [f'col_{i}' for i in range(cols)]
    return pd.DataFrame(np.random.randint(0, 100, size=(rows, cols)), columns=columns)

# Capture uploaded file or generate random data
if data_source == 'Upload a file':
    uploaded_file = st.file_uploader("Upload a CSV or Parquet file", type=["csv", "parquet"])
    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1]
        if file_type == 'csv':
            st.write("Reading CSV...")
            source_data = pd.read_csv(uploaded_file)
        elif file_type == 'parquet':
            st.write("Reading Parquet...")
            source_data = pd.read_parquet(uploaded_file)
        st.write(source_data.head())
else:
    # Generate random data
    rows = st.number_input("Enter the number of rows", min_value=100, max_value=100000, value=1000, step=100)
    cols = st.number_input("Enter the number of columns", min_value=3, max_value=100, value=10, step=1)
    source_data = generate_data(rows, cols)
    st.write(source_data.head())

# Test CSV and Parquet Write/Read Performance
if st.button('Run Tests'):
    test_results = []

    # Test CSV Write
    csv_write_start_time = time.time()
    source_data.to_csv('test_data.csv', index=False)
    csv_write_time = time.time() - csv_write_start_time

    # Test CSV Read
    csv_read_start_time = time.time()
    pd.read_csv('test_data.csv')
    csv_read_time = time.time() - csv_read_start_time

    # Log CSV results
    test_results.append(['CSV', csv_write_time, csv_read_time])

    # Test Parquet Write
    parquet_write_start_time = time.time()
    source_data.to_parquet('test_data.parquet', index=False)
    parquet_write_time = time.time() - parquet_write_start_time

    # Test Parquet Read
    parquet_read_start_time = time.time()
    pd.read_parquet('test_data.parquet')
    parquet_read_time = time.time() - parquet_read_start_time

    # Log Parquet results
    test_results.append(['Parquet', parquet_write_time, parquet_read_time])

    # Display results in a table
    st.write("## Performance Results")
    results_df = pd.DataFrame(test_results, columns=['Format', 'Write Time (s)', 'Read Time (s)'])
    st.write(results_df)
