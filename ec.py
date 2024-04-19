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
    option = st.radio('Select an option:', ('Show Details','Add Details' ,'Update Details', 'Delete Details'))

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

if option == 'Show Details':
    with st.form(key='my_form'):
        position_input = st.text_input(label='Enter the Position:')
        major_input = st.text_input(label='Enter the Major:')
        year_input = st.text_input(label='Enter the Year:')
        pos="position"
        maj="major"
        y="year"
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
                if submit_button:
                    # Determine the query based on input columns
                    if position_input and major_input and year_input:
                        query = "call display_ec_three(%s,%s,%s,%s,%s,%s)"
                        cursor.execute(query, (pos,position_input, maj,major_input,y, year_input))
                    elif position_input and major_input:
                        query = "call display_ec_two(%s,%s,%s,%s)"
                        cursor.execute(query, (pos,position_input, maj,major_input))
                    elif position_input and year_input:
                        query = "call display_ec_two(%s,%s,%s,%s)"
                        cursor.execute(query, (pos,position_input, y,year_input))
                    elif major_input and year_input:
                        query = "call display_ec_two(%s,%s,%s,%s)"
                        cursor.execute(query, (maj,major_input,y, year_input))
                    elif position_input:
                        query = "call display_ec_one(%s,%s)"
                        cursor.execute(query, (pos,position_input,))
                    elif major_input:
                        query = "call display_ec_one(%s,%s)"
                        cursor.execute(query, (maj,major_input,))
                    elif year_input:
                        query = "call display_ec_one(%s,%s)"
                        cursor.execute(query, (y,year_input,))
                    else:
                        query = "call display_ec_all()"
                        cursor.execute(query)

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
    # Add code for update details here
    st.write("Add Details Option Selected")
    with st.form(key='update_form'):
        netid_input= st.text_input(label='Enter the netid')
        name_input= st.text_input(label='Enter the name')
        position_input = st.text_input(label='Enter the Position:')
        major_input = st.text_input(label='Enter the Major:')
        year_input = st.text_input(label='Enter the Year:')
        phone_input=  st.text_input(label='Enetr the phone')
        email_input=  st.text_input(label='Enetr the email')
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
                if submit_button:
                    # Update the details in the database
                    query = "call insert_into_ec(%s, %s, %s, %s, %s,%s,%s)"
                 
                    cursor.execute(query, (netid_input,name_input,position_input, major_input, year_input,phone_input,email_input))
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
        field_input = st.text_input(label='Enter the field to update (e.g., position, major, year):')
        data_input = st.text_input(label='Enter the data to add:')
        filter_field_input = st.text_input(label='Enter the filter field (primary key or other field):')
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
                if submit_button:
                    # Check if filter field and data are provided
                    if filter_field_input and filter_data_input:
                        # Update the details in the database based on the filter
                        query = "call update_ec(%s,%s,%s,%s)"
                        cursor.execute(query, (field_input,data_input, filter_field_input,filter_data_input))
                        if cursor.rowcount == 0:
                            st.error("No such record exists.")
                        else:
                            conn.commit()
                            st.success("Details updated successfully!")
                    else:
                        # Update all records if no filter is provided
                        query ="call update_ec_for_all(%s,%s)"
                        cursor.execute(query, (field_input,data_input))
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
        position_input = st.text_input(label='Enter the Position:')
        major_input = st.text_input(label='Enter the Major:')
        year_input = st.text_input(label='Enter the Year:')
        pos="position"
        maj="major"
        y="year"
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
                if submit_button:
                    # Determine the query based on input columns
                    if position_input and major_input and year_input:
                        query = "call delete_ec_three(%s,%s,%s,%s,%s,%s)"
                        cursor.execute(query, (pos,position_input,maj, major_input, y,year_input))
                    elif position_input and major_input:
                        query = "call delete_ec_two(%s,%s,%s,%s)"
                        cursor.execute(query, (pos,position_input, maj,major_input))
                    elif position_input and year_input:
                        query = "call delete_ec_two(%s,%s,%s,%s)"
                        cursor.execute(query, (pos,position_input,y, year_input))
                    elif major_input and year_input:
                        query = "call delete_ec_two(%s,%s,%s,%s)"
                        cursor.execute(query, (maj,major_input, y,year_input))
                    elif position_input:
                        query = "call delete_ec_one(%s,%s)"
                        cursor.execute(query, (pos,position_input))
                    elif major_input:
                        query = "call delete_ec_one(%s,%s)"
                        cursor.execute(query, (maj,major_input))
                    elif year_input:
                        query = "call delete_ec_one(%s,%s)"
                        cursor.execute(query, (y,year_input))
                    else:
                        query = "call delete_all_ec()"
                        cursor.execute(query)


                    conn.commit()  # Commit the transaction

                    st.success("Details deleted successfully!")

        except mysql.connector.Error as e:
            st.error(f"Error connecting to MySQL database: {e}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
