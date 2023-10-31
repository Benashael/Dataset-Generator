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
page=st.sidebar.radio("**Select a Page**", ["Home Page", "Automatic Dataset Generator", "Custom Dataset Generator", "Dataset for Classification (ML)", "Dataset for Regression (ML)", "Dataset for Clustering (ML)", "Dataset for Association (ML)", "About"])

# Page 1: Introduction
if page == "Home Page":
    # Introduction
    st.title("Welcome to the Dataset Generator App")
    st.write("This app allows you to generate datasets for various purposes. It consists of six pages:")  

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
    st.write("This page enables you to generate datasets used for Classification (ML) tasks. "
             "Here, you can select the type of output (binary class or multi-class) and choose a specific dataset for download.")

    # Page 5 Description
    st.header("Dataset for Regression (ML) Page")
    st.write("This page enables you to generate datasets used for Regression (ML) tasks. "
             "Here, you can choose a specific regression dataset for download.")

    # Page 6 Description
    st.header("Dataset for Clustering (ML) Page")
    st.write("This page enables you to generate datasets used for Clustering (ML) tasks. "
             "At each dataset, you can find the column in name 'Cluster' as the last column. "
             "Here, you can choose a specific clustered dataset for download.")
    
    # Page 7 Description
    st.header("Dataset for Association (ML) Page")
    st.write("This page enables you to generate datasets used for Association (ML) tasks. "
             "Each dataset used here as different kind of association rules. "
             "Here, you can choose a specific association dataset for download.")
    
    # Tips
    st.header("Additional Tips")
    st.markdown("""
    1. **Interactive User Interface**: The app is designed to be user-friendly with interactive elements like buttons, select boxes, and data display. Follow the prompts to create and download your datasets effortlessly.
    """)
    
    st.markdown("""
    2. **Data Validation**: Ensure that you enter valid data types for field names and values. The app provides feedback on data validation to assist you in the process.
    """)
    
    st.markdown("""
    3. **Error Handling**: In case of errors or issues, the app is equipped with error-handling mechanisms to guide you through a smooth experience.
    """)
    
    st.markdown("""
    4. **Dataset Preview**: After generating a dataset, it will be displayed for your review. You can explore the data to make sure it meets your requirements.
    """)
    
    st.markdown("""
    5. **Download in CSV Format**: When you're satisfied with the generated dataset, click the 'Download Dataset' button to download it in CSV format using base64 encoding.
    """)

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
        "2. The field name entered must be of character data type."
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

# Page 4: Dataset for Regression (ML)
elif page == "Dataset for Regression (ML)":
    st.title("Dataset for Regression (ML) Page")

    # Select regression dataset
    selected_dataset = st.selectbox("Select a regression dataset:", ("Car Price Dataset", "Electricity Dataset", "House Price Dataset"))

    dataset_paths = {
            "Car Price Dataset": "Datasets for ML/Regression/car_price_data.csv",
            "Electricity Dataset": "Datasets for ML/Regression/electricity_data.csv",
            "House Price Dataset": "Datasets for ML/Regression/house_price_data.csv", 
        }

    option = st.radio("Select dataset generation option:", ("Entire Dataset", "Random Number of Rows with selected Fields"))
        
    if option == "Entire Dataset":
        # Display the entire dataset
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
        
    else:
        if st.button("Generate Dataset"):
            dataset_url = dataset_paths[selected_dataset]

            # Load and display the selected dataset
            dataset = pd.read_csv(dataset_url)
        
            st.write("Select the fields you want to include in the generated dataset:")
            selected_fields = st.multiselect("Select field names", dataset.columns)
            
            # Generate random number of rows up to 500
            num_rows = st.number_input("Select the number of rows (1-500):", min_value=1, max_value=500, value=10)
            random_rows = dataset[selected_fields].sample(n=num_rows, replace=True)
            
            st.subheader("Generated Dataset:")
            st.dataframe(random_rows)
    
            # Download the dataset using base64 encoding
            csv =random_rows.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # Encode to base64
            href = f'data:file/csv;base64,{b64}'
            st.markdown(f'<a href="{href}" download="generated_dataset.csv">Click here to download Generated Dataset</a>', unsafe_allow_html=True)
    
            st.header("Dataset Overview")
                
            # Dataset Shape
            st.subheader("Entire Dataset Shape:")
            st.write(dataset.shape)
            
            st.subheader("Dataset Shape:")
            st.write(random_rows.shape)
    
            # Column Names
            st.subheader("Column Names:")
            st.write(random_rows.columns)
    
            # Data Types
            st.subheader("Data Types:")
            st.write(random_rows.dtypes)
    
            # Summary Statistics
            st.subheader("Summary Statistics:")
            st.write(random_rows.describe())
            
            # Data Head
            st.subheader("Data Head:")
            st.write(random_rows.head())
    
            # Data Tail
            st.subheader("Data Tail:")
            st.write(random_rows.tail())

# Page 5: Dataset for Clustering (ML)
elif page == "Dataset for Clustering (ML)":
    st.title("Dataset for Clustering (ML) Page")

    # Select regression dataset
    selected_dataset = st.selectbox("Select a clustered dataset:", ("Sample Dataset 1", "Sample Dataset 2", "Sample Dataset 3"))

    dataset_paths = {
            "Sample Dataset 1": "Datasets for ML/Clustering/clustered_data_1.csv",
            "Sample Dataset 2": "Datasets for ML/Clustering/clustered_data_2.csv",
            "Sample Dataset 3": "Datasets for ML/Clustering/clustered_data_3.csv", 
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

# Page 6: Dataset for Association (ML)
elif page == "Dataset for Association (ML)":
    st.title("Dataset for Association (ML) Page")

    # Select association dataset
    selected_dataset = st.selectbox("Select a association dataset:", ("Bakery Dataset", "Basket Analysis Dataset", "Groceries Dataset"))

    dataset_paths = {
            "Bakery Dataset": "Datasets for ML/Association/bakery_data.csv",
            "Basket Analysis Dataset": "Datasets for ML/Association/basket_analysis_data.csv",
            "Groceries Dataset": "Datasets for ML/Association/groceries_data.csv", 
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

# Page 7: About
elif page == "About":
    st.title("🚀 About the Dataset Generator App")
    st.markdown("""
    Thank you for exploring the Dataset Generator app, a powerful tool designed to simplify the process of creating custom, automatic and machine learning datasets for your data needs! 🎉

    With this app, you can effortlessly generate datasets for various purposes, whether it's for machine learning, data analysis, or testing. Whether you need binary or multi-class datasets, we've got you covered.
    The app is built using Streamlit and Python, making it easy and user-friendly. It's brought to you by Team AI Hub and is here to help you with your data adventures.

    Ready to create and explore your datasets? Let's get started and unlock the possibilities of your data! 💡
    """)
    st.markdown("""
    *_Regards,_*
    
    *_Team AI Hub_*
    """)

