import streamlit as st
import mysql.connector
import pandas as pd

# Set up the header
st.header("Show Executive Cabinet Details")

# Create a form for user input
with st.form(key='my_form'):
    position_input = st.text_input(label='Enter the Position:')
    department_input = st.text_input(label='Enter the Department:')
    year_input = st.text_input(label='Enter the Year:')

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
                if position_input and department_input and year_input:
                    query = "SELECT * FROM executive_cabinet WHERE position=%s AND major=%s AND year=%s"
                    cursor.execute(query, (position_input, department_input, year_input))
                elif position_input and department_input:
                    query = "SELECT * FROM executive_cabinet WHERE position=%s AND major=%s"
                    cursor.execute(query, (position_input, department_input))
                elif position_input and year_input:
                    query = "SELECT * FROM executive_cabinet WHERE position=%s AND year=%s"
                    cursor.execute(query, (position_input, year_input))
                elif department_input and year_input:
                    query = "SELECT * FROM executive_cabinet WHERE major=%s AND year=%s"
                    cursor.execute(query, (department_input, year_input))
                elif position_input:
                    query = "SELECT * FROM executive_cabinet WHERE position=%s"
                    cursor.execute(query, (position_input,))
                elif department_input:
                    query = "SELECT * FROM executive_cabinet WHERE major=%s"
                    cursor.execute(query, (department_input,))
                elif year_input:
                    query = "SELECT * FROM executive_cabinet WHERE year=%s"
                    cursor.execute(query, (year_input,))
                else:
                    query = "SELECT * FROM executive_cabinet"
                    cursor.execute(query)

                rows = cursor.fetchall()

                # Create a DataFrame from fetched data
                df = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])

                if df.empty:
                    st.warning("The table does not have the specified attributes.")
                else:
                    # Display data in tabular form
                    st.table(df)

    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL database: {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
