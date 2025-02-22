import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Page Configuration
st.set_page_config(page_title="💿 Data Sweeper", layout="wide")

# Custom Styling
st.markdown(
    """
    <style>
        .main { background-color: #f4f4f4; }
        .stButton>button { border-radius: 8px; padding: 10px 20px; }
        .stDownloadButton>button { background-color: #0073e6; color: white; border-radius: 8px; }
        .stFileUploader { border: 2px dashed #0073e6; padding: 10px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Section
st.markdown("""
    <h1 style='text-align: center; color: #0073e6;'>💿 Data Sweeper</h1>
    <h4 style='text-align: center; color: #333;'>Effortlessly clean, transform, and convert CSV & Excel files</h4>
""", unsafe_allow_html=True)

st.markdown("---")

# File Upload Section
uploaded_files = st.file_uploader("📤 Upload your CSV or Excel files:", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    st.markdown("---")
    
    for file in uploaded_files:
        file_name = file.name
        file_ext = os.path.splitext(file_name)[-1].lower()
        
        try:
            # Load Data
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file, engine='openpyxl')
            else:
                st.error(f"❌ Unsupported file type: {file_ext}")
                continue
            
            # Display File Information
            st.markdown(f"### 📄 {file_name}")
            st.write(f"**File Type:** {file_ext}  |  **Size:** {file.size / 1024:.2f} KB  |  **Shape:** {df.shape[0]} x {df.shape[1]}")
            
            # Data Preview
            with st.expander("👀 Preview Data"):
                st.dataframe(df.head())

            # Data Cleaning
            st.subheader("🧹 Data Cleaning")
            clean_duplicates = st.checkbox(f"Remove Duplicates from {file_name}")
            fill_missing = st.checkbox(f"Fill Missing Values for {file_name}")

            if clean_duplicates:
                df.drop_duplicates(inplace=True)
                st.success("✅ Duplicates removed!")
            
            if fill_missing:
                df.fillna(df.mean(numeric_only=True), inplace=True)
                st.success("✅ Missing values filled!")

            # Column Selection
            st.subheader("🎯 Select Columns")
            selected_columns = st.multiselect(f"Choose columns for {file_name}", df.columns, default=df.columns)
            df = df[selected_columns]

            # Data Visualization
            st.subheader("📊 Data Visualization")
            if st.checkbox(f"Show Bar Chart for {file_name}"):
                st.bar_chart(df.select_dtypes(include=['number']).iloc[:, :2])

            # File Conversion & Download
            st.subheader("📁 Convert & Download")
            conversion_type = st.radio(f"Convert {file_name} to:", ["CSV", "Excel"], horizontal=True)

            if st.button(f"🚀 Convert {file_name} to {conversion_type}"):
                buffer = BytesIO()
                new_file_name = file_name.replace(file_ext, f".{conversion_type.lower()}")
                mime_type = "text/csv" if conversion_type == "CSV" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                else:
                    df.to_excel(buffer, index=False, engine='openpyxl')
                
                buffer.seek(0)
                st.download_button("⬇ Download File", data=buffer, file_name=new_file_name, mime=mime_type)
                st.success(f"🎉 {file_name} converted to {conversion_type} successfully!")
        
        except Exception as e:
            st.error(f"⚠ Error processing {file_name}: {e}")

st.markdown("---")
st.success("🚀 All files processed successfully!")
