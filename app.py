import streamlit as st
import zipfile
import tarfile
import os
import tempfile
import shutil
import pandas as pd
from testNotebook import execute_notebooks_in_directory

def extract_file(file, extract_path):
    if file.name.endswith('.zip'):
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    elif file.name.endswith('.tar') or file.name.endswith('.tar.gz'):
        with tarfile.open(fileobj=file, mode='r:*') as tar_ref:
            tar_ref.extractall(extract_path)

def display_results(log_data):
    # Extract only the notebook name from the full path
    for entry in log_data:
        entry['notebook'] = os.path.basename(entry['notebook'])
    
    df = pd.DataFrame(log_data)
    st.dataframe(df.style.applymap(color_status, subset=['status']))
    # Provide an option to download the log as a CSV file
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download log as CSV",
        data=csv,
        file_name='execution_log.csv',
        mime='text/csv',
    )

def color_status(val):
    color = 'green' if val == 'PASS' else 'red' if val == 'FAIL' else 'grey'
    return f'color: {color}'

def main():
    st.title('Notebook Execution App')
    
    # Language selection
    language = st.selectbox('Select Language / Choisir la langue', ('English 🇬🇧', 'Français 🇫🇷'))
    
    # Display the corresponding instruction file based on the selected language
    if language == 'English 🇬🇧':
        instruction_file = "instruction_en.md"
    else:
        instruction_file = "instruction_fr.md"
    
    with open(instruction_file, "r") as f:
        instructions = f.read()
    st.markdown(instructions)
    
    uploaded_file = st.file_uploader("Upload a zip file containing notebooks and datasets", type=["zip", "tar", "tar.gz"])
    
    if uploaded_file is not None:
        with tempfile.TemporaryDirectory() as tmpdir:
            extract_path = os.path.join(tmpdir, "extracted")
            os.makedirs(extract_path, exist_ok=True)
            extract_file(uploaded_file, extract_path)
            
            if 'log_data' not in st.session_state:
                st.write("Executing notebooks...")
                st.session_state.log_data = execute_notebooks_in_directory(extract_path)
                
                # Clean up the extracted directory after analysis
                shutil.rmtree(extract_path)
            
            st.write("Execution Results:")
            display_results(st.session_state.log_data)

if __name__ == "__main__":
    main()
