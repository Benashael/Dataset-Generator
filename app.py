import streamlit as st
import pandas as pd
import random
import base64
    
st.set_page_config(
    page_title="Dataset Generator App",
    page_icon="📂",
    layout="wide"
)
page=st.sidebar.radio("**Select a Page**", ["Home Page", "Automatic Dataset", "Custom Dataset"])

# Page 1: Introduction
if page == "Home Page":
    # Introduction
    st.title("Welcome to the Dataset Generator App")
    st.write("This app allows you to generate datasets for various purposes. It consists of two pages:")  

    # Page 2 Description
    st.header("Custom Dataset Generator Page")
    st.write("On this page, you can customize your dataset by specifying the number of fields, field names, and values. "
             "You can generate a dataset with a maximum of 10 fields and 50 rows. After generating the dataset, "
             "you can download it.")

    # Page 3 Description
    st.header("Automatic Dataset Generator Page")
    st.write("This page enables you to generate datasets based on your original dataset. You can select fields from "
             "your dataset, specify the number of rows (up to 500), and generate a dataset with randomly sampled values. "
             "You can also download the generated dataset.")

    st.write("To get started, use the sidebar navigation to access the respective pages.")
  
# Page 2: Automatic Dataset Generator
elif page == "Automatic Dataset":
    st.title("Automatic Dataset Generator Page")
    
    # Load your original dataset
    original_dataset = pd.read_excel("https://github.com/Benashael/Dataset-Generator/blob/main/data.xlsx", header=0)  
    
    # Input fields
    st.write("Select the fields you want to include in the generated dataset:")
    selected_fields = st.multiselect("Select fields from your dataset", original_dataset.columns)
    
    # Input number of rows (max 500)
    num_rows = st.number_input("Enter the number of rows (max 500)", min_value=1, max_value=500)
    
    # Generate the dataset
    if st.button("Generate Automatic Dataset"):
        if not selected_fields:
            st.warning("Please select at least one field.")
        else:
            # Randomly sample rows from the original dataset
            generated_df = original_dataset[selected_fields].sample(n=num_rows, replace=True)
            st.dataframe(generated_df)
    
            # Download the dataset using st.download_button
            csv = generated_df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # Encode to base64
            href = f"data:file/csv;base64,{b64}"
            st.download_button(
                label="Download Dataset",
                data=href,
                key="page2_download",
                file_name="generated_auto_dataset.csv",
            )

# Page 3: Manual Dataset Generator
elif page == "Custom Dataset":
    st.title("Custom Dataset Generator Page")

    # Input number of fields (max 10)
    num_fields = st.number_input("Enter the number of fields (max 10)", min_value=1, max_value=10)

    # Initialize an empty list to store field names
    field_names = []

    # Collect field names one by one with unique keys
    for i in range(num_fields):
        field_name = st.text_input(f"Enter Field Name {i + 1}", key=f"field_name_{i}")
        field_names.append(field_name)
        
        if i < num_fields - 1:
            st.write(f"Field {i + 1} name: {field_name}")
            st.write("Please enter the name for the next field before proceeding.")

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
        st.dataframe(generated_df)

        # Download the dataset using st.download_button
        csv = generated_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # Encode to base64
        href = f"data:file/csv;base64,{b64}"

        try:
            st.download_button(
                label="Download Dataset",
                data=href,
                key="page3_download",
                file_name="generated_dataset.csv",
            )
        except st.DuplicateWidgetID:
            st.warning("An error occurred while trying to download the dataset. Please try again.")

