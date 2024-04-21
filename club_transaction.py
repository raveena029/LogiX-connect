import streamlit as st
import mysql.connector
import pandas as pd
import time

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
st.markdown('<p class="header">Club Details</p>', unsafe_allow_html=True)

# Create a form for user input
with st.sidebar:
    st.subheader("Navigation Options")
    option = st.radio('Select an option:', ('Show Details', 'Add Details', 'Update Details', 'Delete Details', 'Extract POC Details'))

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

club_type = None  # Initially set club_type to None

if option == 'Show Details':
    st.write("Show Details Option Selected")
    with st.form(key='my_form'):
        club_name_input = st.text_input(label='Enter the Club Name:')
        club_type = st.selectbox('Select Club Type:', [None, 'department', 'cultural', 'technical'], index=0)

        if club_type == 'department':
            department_input = st.text_input(label='Enter the Department:')

        submit_button = st.form_submit_button(label='Submit')

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
                if club_type is not None:
                    if club_type == 'department':
                        if department_input and club_name_input:
                            query = "SELECT * FROM department_club WHERE department=%s and club_name=%s"
                            cursor.execute(query, (department_input, club_name_input))
                        elif department_input:
                            query = "SELECT * FROM department_club WHERE department=%s"
                            cursor.execute(query, (department_input,))
                        else:
                            query = "SELECT * FROM department_club"
                            cursor.execute(query)
                    elif club_type in ['cultural', 'technical']:
                        if club_name_input:
                            query = f"SELECT * FROM club WHERE club_name=%s and club_type=%s"
                            cursor.execute(query, (club_name_input, club_type))
                        else:
                            query = f"SELECT * FROM club WHERE club_type=%s"
                            cursor.execute(query, (club_type,))
                    rows = cursor.fetchall()

                    # Create a DataFrame from fetched data
                    df = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])

                    # Display data in tabular form
                    st.table(df)
                else:
                    try:
                        if club_name_input:
                            # Check if the club name exists in department_club or club table
                            query_dept = "SELECT * FROM department_club WHERE club_name=%s"
                            cursor.execute(query_dept, (club_name_input,))
                            dept_rows = cursor.fetchall()

                            query_club = "SELECT * FROM club WHERE club_name=%s"
                            cursor.execute(query_club, (club_name_input,))
                            club_rows = cursor.fetchall()

                            if dept_rows:
                                dept_df = pd.DataFrame(dept_rows, columns=[i[0] for i in cursor.description])
                                st.write("Found in Department Club:")
                                st.table(dept_df)
                            elif club_rows:
                                club_df = pd.DataFrame(club_rows, columns=[i[0] for i in cursor.description])
                                st.write("Found in Club:")
                                st.table(club_df)
                            else:
                                st.warning("No records found for the club name.")
                        else:
                            st.warning("Please enter a club name or club type.")
                    except mysql.connector.Error as e:
                        st.error(f"Error querying MySQL database: {e}")

        except mysql.connector.Error as e:
            st.error(f"Error connecting to MySQL database: {e}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

elif option == 'Add Details':
    st.write("Add Details Option Selected")
    with st.form(key='update_form'):
        club_type = st.selectbox('Select Club Type:', [None, 'department', 'cultural', 'technical'], index=0)
        submit_button = st.form_submit_button(label='Add Details')
        if club_type is not None:
            if club_type == 'department':
                department_input = st.text_input(label='Enter the Department:')
                club_name_input = st.text_input(label='Enter the Club Name:')
            elif club_type in ['cultural', 'technical']:
                club_name_input = st.text_input(label='Enter the Club Name:')
            faculty_name_input = st.text_input(label='Enter the name of faculty Advisor:')
            club_email_input = st.text_input(label='Enter the email of the club:')
            club_poc_input = st.text_input(label='Enter the Name of Point of Contact of the Club:')
            poc_netid_input = st.text_input(label='Enter the netid of Point of Contact of the Club:')
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
                    cursor.execute("START TRANSACTION")  # Start a transaction

                    # Check if the form is submitted
                    if submit_button:
                        if club_type == 'department':
                            query_check = "SELECT * FROM department_club WHERE department=%s and club_name=%s"
                            cursor.execute(query_check, (department_input, club_name_input))
                            existing_record = cursor.fetchone()
                            if existing_record:
                                st.warning("Record already exists. Consider updating the existing record.")
                            else:
                                query_insert = "INSERT INTO department_club (Department, faculty_advisor, club_name, club_email, poc_name, poc_netid) VALUES (%s, %s, %s, %s, %s, %s)"
                                cursor.execute(query_insert, (department_input, faculty_name_input, club_name_input, club_email_input, club_poc_input, poc_netid_input))
                        elif club_type in ['cultural', 'technical']:
                            query = "insert into club(club_name,club_email,faculty_advisor,poc_name,club_type,poc_netid) values(%s,%s,%s,%s,%s,%s)"
                            cursor.execute(query, (club_name_input, club_email_input, faculty_name_input, club_poc_input, club_type, poc_netid_input))

                        if auto_commit or commit_changes:
                            conn.commit()
                            st.success("Details added successfully!")

            except mysql.connector.Error as e:
                st.error(f"Error connecting to MySQL database: {e}")
                conn.rollback()  # Rollback the transaction on error

            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()

elif option == 'Update Details':
    st.write("Update Details Option Selected")
    with st.form(key='update_form'):
        club_type = st.selectbox('Select Club Type:', [None, 'department', 'cultural', 'technical'], index=0)
        field_input = st.selectbox('Enter the field to update:', [None, 'club_name', 'club_email','faculty_advisor','poc_name','poc_netid'], index=0)
        data_input = st.text_input(label='Enter the data to add:')
        filter_field_input = st.selectbox('Enter the filter field (primary key or some other attribute)', [None, 'club_name', 'club_email','faculty_advisor','poc_name','poc_netid'], index=0)
        filter_data_input = st.text_input(label='Enter the filter data (to match the filter field):')
        auto_commit = st.checkbox("Save-changes")
        commit_changes = st.checkbox("Commit Changes Permanently")
        submit_button = st.form_submit_button(label='Update')

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
                if submit_button and club_type is not None:
                    # Check if filter field and data are provided
                    if filter_field_input and filter_data_input:
                        if club_type == 'department':
                            query = f"update department_club set {field_input}=%s where {filter_field_input}=%s"
                            cursor.execute(query, (data_input, filter_data_input))
                        elif club_type in ['cultural', 'technical']:
                            query = f"update club set {field_input}=%s where {filter_field_input}=%s"
                            cursor.execute(query, (data_input, filter_data_input))
                        if cursor.rowcount == 0:
                            st.error("No such record exists.")
                        else:
                            if auto_commit or commit_changes:
                                conn.commit()
                                st.success("Changes committed successfully!")
                            else:
                                st.success("Details updated. Check 'Commit Changes' to commit.")
                    else:
                        if club_type == 'department':
                            query = f"update department_club set {field_input}=%s "
                            cursor.execute(query, (data_input,))
                        elif club_type in ['cultural', 'technical']:
                            query = f"update club set {field_input}=%s "
                            cursor.execute(query, (data_input,))
                        if cursor.rowcount == 0:
                            st.error("No such record exists.")
                        else:
                            if auto_commit or commit_changes:
                                conn.commit()
                                st.success("Changes committed successfully!")
                            else:
                                st.success("Details updated for all records. Check 'Commit Changes' to commit.")

        except mysql.connector.Error as e:
            st.error(f"Error connecting to MySQL database: {e}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


elif option == 'Delete Details':
    st.write("Delete Details Option Selected")
    with st.form(key='delete_form'):
        club_type = st.selectbox('Select Club Type:', [None, 'department', 'cultural', 'technical'], index=0)
        field_input = st.selectbox('Enter the field to update:', [None, 'club_name', 'club_email','faculty_advisor','poc_name','poc_netid'], index=0)
        data_input = st.text_input(label='Enter the data to match:')
        submit_button = st.form_submit_button(label='Delete')
        auto_commit = st.checkbox("Save-Changes")
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
                cursor.execute("SET autocommit = 0")  # Set autocommit to 0

                # Check if the form is submitted
                if submit_button and club_type is not None:
                    # Check if field and data are provided
                    if field_input and data_input:
                        if club_type == 'department':
                            query = f"delete from department_club where {field_input}=%s"
                            cursor.execute(query, (data_input,))
                        elif club_type in ['cultural', 'technical']:
                            query = f"delete from club where {field_input}=%s"
                            cursor.execute(query, (data_input,))
                        if cursor.rowcount == 0:
                            st.error("No such record exists.")
                        else:
                            if auto_commit or commit_changes:
                                conn.commit()
                                st.success("Details deleted successfully!")

        except mysql.connector.Error as e:
            st.error(f"Error connecting to MySQL database: {e}")
            conn.rollback()  # Rollback the transaction on error

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

else:
    st.write("Extract POC Details")
    club_type_input = st.selectbox('Select Club Type:', [None, 'department', 'cultural', 'technical'], index=0)
    if club_type_input:
        poc_option = st.selectbox('Select POC Attribute:', [None, 'club_name', 'poc_name', 'poc_netid'], index=0)
        if poc_option:
            poc_data = st.text_input(label=f'Enter the {poc_option}:')
            if poc_data:
                extract_button = st.button('Extract')
                if extract_button:
                    try:
                        conn = mysql.connector.connect(
                            host="localhost",
                            user="root",
                            password="104020",
                            database="proj"
                        )
                        if conn.is_connected():
                            cursor = conn.cursor()

                            if club_type_input == 'department':
                                query = f"SELECT s.net_id as net_id, s.name as name,s.phone_no as phone_no,s.major as major,s.year as year,c.club_name as poc_of_club FROM student s NATURAL JOIN department_club c where s.net_id = c.poc_netid and {poc_option} = %s"
                                cursor.execute(query, (poc_data,))
                            else:
                                query = f"SELECT s.net_id as net_id, s.name as name,s.phone_no as phone_no,s.major as major,s.year as year,c.club_name as poc_of_club FROM student s NATURAL JOIN club c where s.net_id = c.poc_netid and {poc_option} = %s"
                                cursor.execute(query, (poc_data, club_type_input))

                            poc_rows = cursor.fetchall()
                            if poc_rows:
                                poc_df = pd.DataFrame(poc_rows, columns=[i[0] for i in cursor.description])
                                st.table(poc_df)
                            else:
                                st.error("No records found.")

                    except mysql.connector.Error as e:
                        st.error(f"Error connecting to MySQL database: {e}")

                    finally:
                        if conn.is_connected():
                            cursor.close()
                            conn.close()
            else:
                st.warning("Please enter the required details.")
        else:
            st.warning("Please select a POC Attribute.")
    else:
        st.warning("Please enter the Club Type.")
