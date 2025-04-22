import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import re 

#Set the page configuration
st.set_page_config(page_title="WU Directory", layout="wide")

#Create a title and subheader
st.title('Directory at Westminster University')
st.write("This is an enhanced alternative to the employee [directory](https://westminsteru.edu/campus-directory/index.html) at Westminster University." )

#Read in and display the data
data = pd.read_csv('WU_directory.csv') 

#Create a selectbox for departments
department_list = data['Department'].unique().tolist()
department_list.insert(0, 'All')
department = st.selectbox(label = 'Choose one department from below:', options = department_list)

#Create a check box for roles
col1, col2, col3, col4 = st.columns([0.2,0.2,0.2,0.4])
with col1:
    st.text("Type of Role:") 
with col2:
    role_faculty = st.checkbox('Faculty', value=1)
with col3:
    role_staff = st.checkbox('Staff', value=1)

#Create a check box for contract
col1, col2, col3, col4 = st.columns([0.2,0.2,0.2,0.4])
with col1:
    st.text("Type of Contract:") 
with col2:
    contract_fulltime = st.checkbox('Full-time', value=1)
with col3:
    contract_parttime = st.checkbox('Part-time', value=1)

#Create a check box for position
col1, col2, col3, col4 = st.columns([0.2,0.2,0.2,0.4])
with col1:
    st.text("Type of Position:")
with col2:
    position_associate = st.checkbox('Associate Professor', value=1)
with col3:
    position_assistant = st.checkbox('Assistant Professor', value=1)
with col4:
    position_professor = st.checkbox('Professor', value=1)

# Add search functionality
st.write("## Search by Name")
col1, col2 = st.columns([0.8, 0.2])
with col1:
    search_query = st.text_input("Enter name to search:", "")
with col2:
    use_regex = st.checkbox("Use Regex", value=False)

#Filter the data based on the department selected and role checkboxes
filtered_data = data.copy()

# Create a role filter based on checkboxes
if role_faculty and role_staff:
    role_filter = True
elif role_faculty:
    role_filter = filtered_data['Role'] == 'Faculty'
elif role_staff:
    # Only show staff
    role_filter = filtered_data['Role'] == 'Staff'
else:
    role_filter = False

# Create a contract filter based on checkboxes
if contract_fulltime and contract_parttime:
    contract_filter = True
elif contract_fulltime:
    contract_filter = filtered_data['Contract'] == 'FULL-TIME'
elif contract_parttime:
    contract_filter = filtered_data['Contract'] == 'PART-TIME'
else:
    contract_filter = False

if position_associate and position_assistant and position_professor:
    position_filter = True
elif position_associate:
    position_filter = filtered_data['Position'] == 'Associate Professor'
elif position_assistant:
    position_filter = filtered_data['Position'] == 'Assistant Professor'
elif position_professor:
    position_filter = filtered_data['Position'] == 'Professor'
else:
    position_filter = False

# Apply department filter
if department != 'All':
    filtered_data = filtered_data.query(f'Department == "{department}"')

# Apply role filter
if not (role_faculty and role_staff):  
    if role_filter is False:  
        filtered_data = filtered_data[filtered_data['Role'].isna()]  
    else:
        filtered_data = filtered_data[role_filter]

# Apply contract filter
if not (contract_fulltime and contract_parttime):  
    if contract_filter is False: 
        filtered_data = filtered_data[filtered_data['Contract'].isna()]  
    else:
        filtered_data = filtered_data[contract_filter]

# Apply position filter
if not (position_associate and position_assistant and position_professor):
    if position_filter is False:
        filtered_data = filtered_data[filtered_data['Position'].isna()]
    else:
        filtered_data = filtered_data[position_filter]

# Apply name search filter
if search_query:
    try:
        if use_regex:
            # Use regex pattern matching if regex mode is enabled
            filtered_data = filtered_data[filtered_data['Name'].str.contains(search_query, case=False, regex=True)]
        else:
            # Use simple case-insensitive substring matching if regex mode is disabled
            filtered_data = filtered_data[filtered_data['Name'].str.contains(search_query, case=False, regex=False)]
    except Exception as e:
        st.error(f"Search error: {e}")

# Display the filtered data
st.dataframe(filtered_data, hide_index=True)