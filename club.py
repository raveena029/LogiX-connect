import streamlit as st
import mysql.connector
import pandas as pd

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
st.markdown('<p class="header">Executive Cabinet Details</p>', unsafe_allow_html=True)

# Create a form for user input
with st.sidebar:
    st.subheader("Navigation Options")
    option = st.radio('Select an option:', ('Show Details', 'Add Details', 'Update Details', 'Delete Details'))

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
        club_type = st.selectbox('Select Club Type:', [None, 'department', 'cultural', 'technical'], index=0)

        if club_type == 'department':
            department_input = st.text_input(label='Enter the Department:')
            club_name_input = st.text_input(label='Enter the Club Name:')
        elif club_type in ['cultural', 'technical']:
            club_name_input = st.text_input(label='Enter the Club Name:')

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
        except mysql.connector.Error as e:
            st.error(f"Error connecting to MySQL database: {e}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

elif option == 'Add Details':
    # Add code for update details here
    st.write("Add Details Option Selected")
    with st.form(key='update_form'):
        club_type = st.selectbox('Select Club Type:', [None, 'department', 'cultural', 'technical'], index=0)
        submit_button = st.form_submit_button(label='Update')
        if club_type is not None:
            if club_type == 'department':
                department_input = st.text_input(label='Enter the Department:')
                club_name_input = st.text_input(label='Enter the Club Name:')
            elif club_type in ['cultural', 'technical']:
                club_name_input = st.text_input(label='Enter the Club Name:')
            faculty_name_input = st.text_input(label='Enter the name of faculty Advisor:')
            club_email_input = st.text_input(label='Enter the email of the club:')
            club_poc_input = st.text_input(label='Enter the Name of Point of Contact of the Club:')
            poc_email_input = st.text_input(label='Enter the email of Point of Contact of the Club:')
        

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
                    if club_type == 'department':
                        query = "insert into department_club(Department,faculty_advisor,club_name,club_email,club_poc,poc_email) values(%s,%s,%s,%s,%s,%s)"
                        cursor.execute(query, (department_input, faculty_name_input, club_name_input, club_email_input, club_poc_input, poc_email_input))
                    elif club_type in ['cultural', 'technical']:
                        query = "insert into club(club_name,club_email,faculty_advisor,poc_name,club_type,poc_email) values(%s,%s,%s,%s,%s,%s)"
                        cursor.execute(query, (club_name_input, club_email_input, faculty_name_input, club_poc_input, club_type, poc_email_input))

                    conn.commit()
                    st.success("Details added successfully!")

            except mysql.connector.Error as e:
                st.error(f"Error connecting to MySQL database: {e}")

            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()

elif option == 'Update Details':
    # Update details option
    st.write("Update Details Option Selected")
    with st.form(key='update_form'):
        club_type = st.selectbox('Select Club Type:', [None, 'department', 'cultural', 'technical'], index=0)
        field_input = st.selectbox('Enter the field to update:', [None, 'club_name', 'club_email','faculty_advisor','poc_name','poc_email'], index=0)
        data_input = st.text_input(label='Enter the data to add:')
        filter_field_input = st.selectbox('Enter the filter field(primary key or some other attribute)', [None, 'club_name', 'club_email','faculty_advisor','poc_name','poc_email'], index=0)
        filter_data_input = st.text_input(label='Enter the filter data (to match the filter field):')
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
                            conn.commit()
                        if cursor.rowcount == 0:
                            st.error("No such record exists.")
                        else:
                            conn.commit()
                            st.success("Details updated successfully!")
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
                            conn.commit()
                            st.success("Details updated for all records!")

        except mysql.connector.Error as e:
            st.error(f"Error connecting to MySQL database: {e}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

else:
    # Add code for delete details here
    st.write("Delete Details Option Selected")
    with st.form(key='delete_form'):
        club_type = st.selectbox('Select Club Type:', [None, 'department', 'cultural', 'technical'], index=0)
        field_input = st.selectbox('Enter the field to update:', [None, 'club_name', 'club_email','faculty_advisor','poc_name','poc_email'], index=0)
        data_input = st.text_input(label='Enter the data to match:')
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
                            conn.commit()
                            st.success("Details deleted successfully!")
                    else:
                        if club_type == 'department':
                            query = "delete from department_club"
                            cursor.execute(query)
                        elif club_type in ['cultural', 'technical']:
                            query = "delete from club"
                            cursor.execute(query)
                        if cursor.rowcount == 0:
                            st.error("No such record exists.")
                        else:
                            conn.commit()
                            st.success("Details Deleted for all records!")

        except mysql.connector.Error as e:
            st.error(f"Error connecting to MySQL database: {e}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
