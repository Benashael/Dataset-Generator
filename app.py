import streamlit as st
import pandas as pd
import numpy as np
import random
import base64
    
st.set_page_config(
    page_title="Dataset Generator App",
    page_icon="📂",
    layout="wide"
)
page=st.sidebar.radio("**Select a Page**", ["Home Page", "Automatic Dataset Generator", "Custom Dataset Generator", "Dataset for Classification (ML)", "Dataset for Regression (ML)", "Dataset for Clustering (ML)"])

# Page 1: Introduction
if page == "Home Page":
    # Introduction
    st.title("Welcome to the Dataset Generator App")
    st.write("This app allows you to generate datasets for various purposes. It consists of two pages:")  

    # Page 2 Description
    st.header("Automatic Dataset Generator Page")
    st.write("This page enables you to generate datasets based on your original dataset. You can select fields from "
             "your dataset, specify the number of rows (up to 500), and generate a dataset with randomly sampled values. "
             "You can also download the generated dataset.")
    
    # Page 3 Description
    st.header("Custom Dataset Generator Page")
    st.write("On this page, you can customize your dataset by specifying the number of fields, field names, and values. "
             "You can generate a dataset with a maximum of 10 fields and 50 rows. After generating the dataset, "
             "you can download it.")

    # Page 4 Description
    st.header("Dataset for Classification (ML) Page")
    st.write("This page enables you to generate datasets used for Classification (ML) tasks."
             "Here, you can select the type of output (binary class or multi-class) and choose a specific dataset for download."
            )

    
    # Page 5 Description

    # Page 6 Description

    st.write("To get started, use the sidebar navigation to access the respective pages.")
  
# Page 2: Automatic Dataset Generator
elif page == "Automatic Dataset Generator":
    st.title("Automatic Dataset Generator Page")
    
    # Load your original dataset
    original_dataset = pd.read_csv("data.csv")  
    
    # Input fields
    st.write("Select the fields you want to include in the generated dataset:")
    selected_fields = st.multiselect("Select field names", original_dataset.columns)
    
    # Input number of rows (max 500)
    num_rows = st.number_input("Enter the number of rows (max 500)", min_value=1, max_value=500)
    
    # Generate the dataset
    if st.button("Generate Automatic Dataset"):
        if not selected_fields:
            st.warning("Please select at least one field.")
        else:
            # Randomly sample rows from the original dataset
            generated_df = original_dataset[selected_fields].sample(n=num_rows, replace=True)
            st.subheader("Generated Dataset:")
            st.dataframe(generated_df)
    
            # Download the dataset using st.button and base64
            csv = generated_df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # Encode to base64
            href = f'data:file/csv;base64,{b64}'
            st.markdown(f'<a href="{href}" download="generated_dataset.csv">Click here to download Generated Dataset</a>', unsafe_allow_html=True)
            
            st.header("Dataset Overview")
            
            # Dataset Shape
            st.subheader("Dataset Shape:")
            st.write(generated_df.shape)
    
            # Column Names
            st.subheader("Column Names:")
            st.write(generated_df.columns)
    
            # Data Types
            st.subheader("Data Types:")
            st.write(generated_df.dtypes)
    
            # Summary Statistics
            st.subheader("Summary Statistics:")
            st.write(generated_df.describe())

# Page 3: Manual Dataset Generator
elif page == "Custom Dataset Generator":
    st.title("Custom Dataset Generator Page")

    # Input number of fields (max 10)
    num_fields = st.number_input("Enter the number of fields (max 10)", min_value=1, max_value=10)

    st.markdown(
        "**Please note the following:**"
    )
    st.markdown(
        "1. The field name can be changed by yourself from default field name."
    )
    st.markdown(
        "2. The field name entered must be of string data type."
    )
    
    # Initialize an empty list to store field names
    field_names = []

    # Collect field names one by one with unique keys and validate data type
    for i in range(num_fields):
        default_field_name = f"Field Name {i + 1}"
        field_name = st.text_input(f"Enter Field Name {i + 1}", key=f"field_name_{i}", value=default_field_name)
        if not isinstance(field_name, str):
            st.error("Field names must be of string data type. Please enter a valid field name.")
            break
        field_names.append(field_name)

    st.write("**Field Names**")
    st.write(field_names)
    
    # Input the number of rows
    num_rows = st.number_input("Enter the number of rows", min_value=1, max_value=500)

    # Collect field values for each row with unique keys
    field_values = {field_name: [] for field_name in field_names}
    for i in range(num_rows):
        st.write(f"Record {i + 1}")
        for field_name in field_names:
            field_value = st.text_input(f"Enter the value for {field_name} in Record {i + 1}", key=f"value_{i}_{field_name}")
            field_values[field_name].append(field_value)

    # Generate the dataset
    if st.button("Generate Dataset"):
        data = {field_name: field_values[field_name] for field_name in field_names}
        generated_df = pd.DataFrame(data)
        st.subheader("Generated Dataset:")
        st.dataframe(generated_df)

        # Download the dataset using st.button and base64
        csv = generated_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # Encode to base64
        href = f'data:file/csv;base64,{b64}'
        st.markdown(f'<a href="{href}" download="generated_dataset.csv">Click here to download Generated Dataset</a>', unsafe_allow_html=True)
        
        st.header("Dataset Overview")
        
        # Dataset Shape
        st.subheader("Dataset Shape:")
        st.write(generated_df.shape)

        # Column Names
        st.subheader("Column Names:")
        st.write(generated_df.columns)

        # Data Types
        st.subheader("Data Types:")
        st.write(generated_df.dtypes)

        # Summary Statistics
        st.subheader("Summary Statistics:")
        st.write(generated_df.describe())

# Page 4: Dataset for Classification (ML)
elif page == "Dataset for Classification (ML)":
    st.title("Dataset for Classification (ML) Page")

    # Select type of output (binary class or multi-class)
    output_type = st.radio("Select the type of output:", ("Binary Class", "Multi-Class"))

    if output_type == "Binary Class":
        # Select binary classification dataset
        selected_dataset = st.selectbox("Select a binary classification dataset:", ("Heart Disease Dataset", "Diabetes Dataset"))

        # Define dataset paths (replace with actual dataset paths)
        dataset_paths = {
            "Heart Disease Dataset": "Datasets for ML/Classification/heart_disease_data.csv",
            "Diabetes Dataset": "Datasets for ML/Classification/diabetes_data.csv",
        }

    elif output_type == "Multi-Class":
        # Select multi-class classification dataset
        selected_dataset = st.selectbox("Select a multi-class classification dataset:", ("Iris Dataset", "Acoustic Features Dataset"))

        # Define dataset paths (replace with actual dataset paths)
        dataset_paths = {
            "Iris Dataset": "Datasets for ML/Classification/iris_data.csv",
            "Acoustic Features Dataset": "Datasets for ML/Classification/acoustic_features_data.csv",
        }

    if st.button("Generate Dataset"):
        dataset_url = dataset_paths[selected_dataset]

        # Load and display the selected dataset
        dataset = pd.read_csv(dataset_url)
        st.subheader("Generated Dataset:")
        st.dataframe(dataset)

        # Download the dataset using base64 encoding
        csv =dataset.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # Encode to base64
        href = f'data:file/csv;base64,{b64}'
        st.markdown(f'<a href="{href}" download="generated_dataset.csv">Click here to download Generated Dataset</a>', unsafe_allow_html=True)

        st.header("Dataset Overview")
            
        # Dataset Shape
        st.subheader("Dataset Shape:")
        st.write(dataset.shape)

        # Column Names
        st.subheader("Column Names:")
        st.write(dataset.columns)

        # Data Types
        st.subheader("Data Types:")
        st.write(dataset.dtypes)

        # Summary Statistics
        st.subheader("Summary Statistics:")
        st.write(dataset.describe())
        
        # Data Head
        st.subheader("Data Head:")
        st.write(dataset.head())

        # Data Tail
        st.subheader("Data Tail:")
        st.write(dataset.tail())
