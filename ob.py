import streamlit as st
import mysql.connector
import pandas as pd


# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Set up the header
st.markdown(
    """
    <style>
    .header {
        background-color: #0072b8;
        padding: 1rem;
        color: white;
        text-align: center;
        font-size: 2rem;
    }
    </style>
    """
    , unsafe_allow_html=True
)
st.markdown('<p class="header">Office Bearers Details</p>', unsafe_allow_html=True)

def authenticate(password):
    if password == "admin123":  # Replace "admin123" with the actual password
        st.success("Welcome, admin!")
        st.session_state.logged_in = True
    else:
        st.session_state.logged_in = False
        st.error("You are not authorised to make changes!!!")

def logout():
    st.session_state.logged_in = False

# Create a form for user input
with st.sidebar:
    st.subheader("Navigation Options")
    option = st.radio('Select an option:', ('Show Details', 'Add Details', 'Update Details', 'Delete Details'))

    if option in ['Add Details', 'Update Details', 'Delete Details'] and not st.session_state.logged_in:
        password = st.text_input("Enter Password:", type="password")
        if st.button('Login'):
            authenticate(password)

# Set a background color for the main page
st.markdown(
    """
    <style>
    body {
        background-color: #f0f5f5;
    }
    </style>
    """
    , unsafe_allow_html=True
)

# Check if logged in or 'Show Details' selected
if 'logged_in' in st.session_state and (st.session_state.logged_in or option == 'Show Details'):
    if option == 'Show Details':
        st.write("Show Details Option Selected")
        with st.form(key='my_form'):
            position_input = st.text_input(label='Enter the Position:')
            major_input = st.text_input(label='Enter the Major:')
            year_input = st.text_input(label='Enter the Year:')
            submit_button = st.form_submit_button(label='Submit')
            pos="position"
            maj="major"
            y="year"
            # Connect to the database
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="104020",
                    database="proj"
                )
                if conn.is_connected():
                    cursor = conn.cursor()

                    # Check if the form is submitted
                    if submit_button:
                        # Determine the query based on input columns
                        if position_input and major_input and year_input:
                            query = "SELECT * FROM office_bearers WHERE position=%s AND major=%s AND year=%s"
                            cursor.execute(query, (position_input, major_input, year_input))
                            updated_rows = cursor.fetchall()
                            df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                            num_rows_updated = len(df_updated)
                            query = "call display_ob_three(%s,%s,%s,%s,%s,%s)"
                            cursor.execute(query, (pos,position_input, maj,major_input,y, year_input))
                        elif position_input and major_input:
                            query = "SELECT * FROM office_bearers WHERE position=%s AND major=%s"
                            cursor.execute(query, (position_input, major_input))
                            updated_rows = cursor.fetchall()
                            df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                            num_rows_updated = len(df_updated)
                            query = "call display_ob_two(%s,%s,%s,%s)"
                            cursor.execute(query, (pos,position_input, maj,major_input))
                        elif position_input and year_input:
                            query = "SELECT * FROM office_bearers WHERE position=%s AND year=%s"
                            cursor.execute(query, (position_input, year_input))
                            updated_rows = cursor.fetchall()
                            df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                            query = "call display_ob_two(%s,%s,%s,%s)"
                            cursor.execute(query, (pos,position_input, y,year_input))
                        elif major_input and year_input:
                            query = "SELECT * FROM office_bearers WHERE major=%s AND year=%s"
                            cursor.execute(query, (major_input, year_input))
                            updated_rows = cursor.fetchall()
                            df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                            num_rows_updated = len(df_updated)
                            query = "call display_ob_two(%s,%s,%s,%s)"
                            cursor.execute(query, (maj,major_input,y, year_input))
                        elif position_input:
                            query = "SELECT * FROM office_bearers WHERE position=%s"
                            cursor.execute(query, (position_input,))
                            updated_rows = cursor.fetchall()
                            df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                            num_rows_updated = len(df_updated)
                            query = "call display_ob_one(%s,%s)"
                            cursor.execute(query, (pos,position_input,))
                        elif major_input:
                            query = "SELECT * FROM office_bearers WHERE major=%s"
                            cursor.execute(query, (major_input,))
                            updated_rows = cursor.fetchall()
                            df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                            num_rows_updated = len(df_updated)
                            query = "call display_ob_one(%s,%s)"
                            cursor.execute(query, (maj,major_input,))
                        elif year_input:
                            query = "SELECT * FROM office_bearers WHERE year=%s"
                            cursor.execute(query, (year_input,))
                            updated_rows = cursor.fetchall()
                            df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                            num_rows_updated = len(df_updated)
                            query = "call display_ob_one(%s,%s)"
                            cursor.execute(query, (y,year_input,))
                        else:
                            query = "SELECT * FROM office_bearers"
                            cursor.execute(query)
                            updated_rows = cursor.fetchall()
                            df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                            num_rows_updated = len(df_updated)
                            query = "call display_ob_all()"
                            cursor.execute(query)
                        st.success(f"Number of rows displayed successfully: {num_rows_updated}")

                        rows = cursor.fetchall()

                        # Create a DataFrame from fetched data
                        df = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])

                        if df.empty:
                            st.warning("The table does not have the specified attributes")
                        else:
                            # Display data in tabular form
                            st.table(df)
                            

            except mysql.connector.Error as e:
                st.error(f"Error connecting to MySQL database: {e}")

            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
    elif option == 'Add Details':
        st.write("Add Details Option Selected")
        with st.form(key='update_form'):
            netid_input= st.text_input(label='Enter the netid')
            name_input= st.text_input(label='Enter the name')
            position_input = st.text_input(label='Enter the Position:')
            major_input = st.text_input(label='Enter the Major:')
            year_input = st.text_input(label='Enter the Year:')
            phone_input=  st.text_input(label='Enter the phone')
            email_input=  st.text_input(label='Enter the email')
            auto_commit = st.checkbox("Save Changes")
            commit_changes = st.checkbox("Commit Changes Permanently")
            submit_button = st.form_submit_button(label='Update')
            pos="position"
            maj="major"
            y="year"
            # Connect to the database
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="104020",
                    database="proj"
                )
                if conn.is_connected():
                    cursor = conn.cursor()
                    cursor.execute("START TRANSACTION")

                    # Check if the form is submitted
                    if submit_button:
                        # Update the details in the database
                        result=1
                        query = "call insert_into_ob(%s, %s, %s, %s, %s,%s,%s)"
                        cursor.execute(query, (netid_input,name_input,position_input, major_input, year_input,phone_input,email_input))
                        if auto_commit or commit_changes:
                            conn.commit()
                            st.write("Number of rows inserted sucessfully: ", result)
                        else:
                            st.warning("Details will be rolled back unless you check 'Commit Changes'.")
                        logout()
                        #authenticate(password)
                        st.success("Details added successfully!")

            except mysql.connector.Error as e:
                st.error(f"Error connecting to MySQL database: {e}")
                if conn.is_connected():
                    conn.rollback()  
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
    elif option == 'Update Details':
        st.write("Update Details Option Selected")
        with st.form(key='update_form'):
            field_input = st.text_input(label='Enter the field to update (e.g., position, major, year):')
            data_input = st.text_input(label='Enter the data to add:')
            filter_field_input = st.text_input(label='Enter the filter field (primary key or other field):')
            filter_data_input = st.text_input(label='Enter the filter data (to match the filter field):')
            submit_button = st.form_submit_button(label='Update')
            auto_commit = st.checkbox("Save Changes")
            commit_changes = st.checkbox("Commit Changes Permanently")
            # Connect to the database
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="104020",
                    database="proj"
                )
                if conn.is_connected():
                    cursor = conn.cursor()
                    cursor.execute("START TRANSACTION") 
                    # Check if the form is submitted
                    if submit_button:
                        # Check if filter field and data are provided
                        if filter_field_input and filter_data_input:
                            query=f"SELECT * FROM office_bearers WHERE {filter_field_input} = %s"
                            cursor.execute(query,(filter_data_input,))
                            updated_rows = cursor.fetchall()
                            df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                            # Count the number of rows in the DataFrame
                            num_rows_updated = len(df_updated)
                            # Update the details in the database based on the filter
                            query = "call update_ob(%s,%s,%s,%s)"
                            cursor.execute(query, (field_input,data_input, filter_field_input,filter_data_input))
                            if cursor.rowcount == 0:
                                st.error("No such record exists.")
                            else:
                                if auto_commit or commit_changes:
                                    conn.commit()
                                    st.success(f"Number of rows updated successfully: {num_rows_updated}")
                                else:
                                    st.warning("Details  will be rolled back unless you check 'Commit Changes'.")
                            logout()
                            #authenticate(password)
                        else:
                            # Update all records if no filter is provided
                            query="SELECT * FROM office_bearers"
                            cursor.execute(query,())
                            updated_rows = cursor.fetchall()
                            # Store the updated data in a DataFrame
                            df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                            # Count the number of rows in the DataFrame
                            num_rows_updated = len(df_updated)
                            query ="call update_ob_for_all(%s,%s)"
                            cursor.execute(query, (field_input,data_input))
                            if auto_commit or commit_changes:
                                conn.commit()
                                st.success(f"Number of rows updated successfully: {num_rows_updated}")
                            else:
                                st.warning("Details updated but will be rolled back unless you check 'Commit Changes'.")
                        logout()
                        #authenticate(password)

            except mysql.connector.Error as e:
                st.error(f"Error connecting to MySQL database: {e}")
                if conn.is_connected():
                    conn.rollback() 
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
    elif option == 'Delete Details':
        st.write("Delete Details Option Selected")
        with st.form(key='delete_form'):
            position_input = st.text_input(label='Enter the Position:')
            major_input = st.text_input(label='Enter the Major:')
            year_input = st.text_input(label='Enter the Year:')
            pos="position"
            maj="major"
            y="year"
            auto_commit = st.checkbox("Save Changes")
            commit_changes = st.checkbox("Commit Changes Permanently")
            submit_button = st.form_submit_button(label='Delete')

            # Connect to the database
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="104020",
                    database="proj"
                )
                if conn.is_connected():
                    cursor = conn.cursor()
                    cursor.execute("START TRANSACTION")
                    # Check if the form is submitted
                    if submit_button:
                        # Determine the query based on input columns
                        if position_input and major_input and year_input:
                            query=f"SELECT * FROM office_bearers WHERE position= %s and major=%s and year=%s"
                            cursor.execute(query,(position_input,major_input,year_input))
                            updated_rows = cursor.fetchall()
                            df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                            num_rows_updated = len(df_updated)
                            query = "call delete_ob_three(%s,%s,%s,%s,%s,%s)"
                            cursor.execute(query, (pos,position_input,maj, major_input, y,year_input))
                        elif position_input and major_input:
                            query=f"SELECT * FROM office_bearers WHERE position= %s and major=%s"
                            cursor.execute(query,(position_input,major_input))
                            updated_rows = cursor.fetchall()
                            df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                            num_rows_updated = len(df_updated)
                            query = "call delete_ob_two(%s,%s,%s,%s)"
                            cursor.execute(query, (pos,position_input, maj,major_input))
                        elif position_input and year_input:
                            query=f"SELECT * FROM office_bearers WHERE position= %s and year=%s"
                            cursor.execute(query,(position_input,year_input))
                            updated_rows = cursor.fetchall()
                            df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                            num_rows_updated = len(df_updated)
                            query = "call delete_ob_two(%s,%s,%s,%s)"
                            cursor.execute(query, (pos,position_input,y, year_input))
                        elif major_input and year_input:
                            query=f"SELECT * FROM office_bearers WHERE major=%s and year=%s"
                            cursor.execute(query,(major_input,year_input))
                            updated_rows = cursor.fetchall()
                            df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                            num_rows_updated = len(df_updated)
                            query = "call delete_ob_two(%s,%s,%s,%s)"
                            cursor.execute(query, (maj,major_input, y,year_input))
                        elif position_input:
                            query=f"SELECT * FROM office_bearers WHERE position= %s"
                            cursor.execute(query,(position_input,))
                            updated_rows = cursor.fetchall()
                            df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                            num_rows_updated = len(df_updated)
                            query = "call delete_ob_one(%s,%s)"
                            cursor.execute(query, (pos,position_input))
                        elif major_input:
                            query=f"SELECT * FROM office_bearers WHERE major=%s" 
                            cursor.execute(query,(major_input,))
                            updated_rows = cursor.fetchall()
                            df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                            num_rows_updated = len(df_updated)
                            query = "call delete_ob_one(%s,%s)"
                            cursor.execute(query, (maj,major_input))
                        elif year_input:
                            query=f"SELECT * FROM office_bearers WHERE year=%s"
                            cursor.execute(query,(year_input,))
                            updated_rows = cursor.fetchall()
                            df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                            num_rows_updated = len(df_updated)
                            query = "call delete_ob_one(%s,%s)"
                            cursor.execute(query, (y,year_input))
                        else:
                            query="SELECT * FROM office_bearers"
                            cursor.execute(query,())
                            updated_rows = cursor.fetchall()
                            df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                            num_rows_updated = len(df_updated)
                            query = "call delete_all_ob()"
                            cursor.execute(query)
                        if auto_commit or commit_changes:
                            conn.commit()
                            st.success(f"Number of rows deleted successfully: {num_rows_updated}")
                        else:
                            st.warning("Details deleted but will be rolled back unless you check 'Commit Changes'.")
                        logout()
                        #authenticate(password)  # Commit the transaction

            except mysql.connector.Error as e:
                st.error(f"Error connecting to MySQL database: {e}")
                if conn.is_connected():
                    conn.rollback()

            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
else:
    st.warning("You are not logged in. Please log in to perform operations.")
