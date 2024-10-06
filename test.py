import streamlit as st
import pandas as pd
import time

st.title('CSV vs Parquet Read/Write Speed Test')

# File upload
uploaded_file = st.file_uploader("Upload a CSV or Parquet file", type=["csv", "parquet"])

# Check if a file has been uploaded
if uploaded_file is not None:
    # Determine file type
    file_type = uploaded_file.name.split('.')[-1]
    
    # Read file and time the operation
    start_time = time.time()
    
    if file_type == 'csv':
        st.write("Reading CSV...")
        data = pd.read_csv(uploaded_file)
    elif file_type == 'parquet':
        st.write("Reading Parquet...")
        data = pd.read_parquet(uploaded_file)
    
    read_time = time.time() - start_time
    st.write(f"Read Time: {read_time:.5f} seconds")
    
    st.write(data.head())  # Display the first few rows of the data

    # Measure write time
    if st.button('Write and Measure Time'):
        st.write("Writing the file back...")
        write_start_time = time.time()
        
        if file_type == 'csv':
            data.to_csv('output.csv', index=False)
        elif file_type == 'parquet':
            data.to_parquet('output.parquet', index=False)
        
        write_time = time.time() - write_start_time
        st.write(f"Write Time: {write_time:.5f} seconds")

        st.success("File written successfully!")
