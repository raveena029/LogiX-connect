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
st.markdown('<p class="header">Show Class Represenatatives</p>', unsafe_allow_html=True)

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
    st.write("Show Details Option Selected")
    with st.form(key='my_form'):
        name_input = st.text_input(label='Enter the Name:')
        major_input = st.text_input(label='Enter the Major:')
        year_input = st.text_input(label='Enter the Year:')
        maj="major"
        y="year"
        pos="name"
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
                    if name_input and major_input and year_input:
                        query = "SELECT * FROM senate WHERE name=%s AND major=%s AND year=%s"
                        cursor.execute(query, (name_input, major_input, year_input))
                        updated_rows = cursor.fetchall()
                        df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                        num_rows_updated = len(df_updated)
                        st.write(f"Number of rows affected: {num_rows_updated}")
                        st.table(df_updated)
                        cursor.callproc("display_senate_three", (pos,name_input,maj, major_input, y,year_input, 0))  # Pass an OUT parameter
                        cursor.execute("SELECT @_display_senate_three_3")
                        result = cursor.fetchone()[0]
                        conn.commit()
                        st.success(f"Number of rows displayed successfully: {num_rows_updated}")
                    elif name_input and major_input:
                        query = "SELECT * FROM senate WHERE name=%s AND major=%s"
                        cursor.execute(query, (name_input, major_input))
                        updated_rows = cursor.fetchall()
                        df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                        num_rows_updated = len(df_updated)
                        st.write(f"Number of rows affected: {num_rows_updated}")
                        st.table(df_updated)
                        cursor.callproc("display_senate_two", (pos,name_input,maj, major_input ,0))  # Pass an OUT parameter
                        cursor.execute("SELECT @_display_senate_two_2")
                        result = cursor.fetchone()[0]
                        conn.commit()
                        st.success(f"Number of rows displayed successfully: {num_rows_updated}")
                    elif name_input and year_input:
                        query = "SELECT * FROM senate WHERE name=%s AND year=%s"
                        cursor.execute(query, (name_input, year_input))
                        updated_rows = cursor.fetchall()
                        df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                        num_rows_updated = len(df_updated)
                        st.write(f"Number of rows affected: {num_rows_updated}")
                        st.table(df_updated)
                        cursor.callproc("display_senate_two", (pos,name_input,y, year_input, 0))  # Pass an OUT parameter
                        cursor.execute("SELECT @_display_senate_two_2")
                        result = cursor.fetchone()[0]
                        conn.commit()
                        st.success(f"Number of rows displayed successfully: {num_rows_updated}")
                    elif major_input and year_input:
                        query = "SELECT * FROM senate WHERE major=%s AND year=%s"
                        cursor.execute(query, (major_input, year_input))
                        updated_rows = cursor.fetchall()
                        df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                        num_rows_updated = len(df_updated)
                        st.write(f"Number of rows affected: {num_rows_updated}")
                        st.table(df_updated)
                        cursor.callproc("display_senate_two", (maj,major_input, y,year_input, 0))  # Pass an OUT parameter
                        cursor.execute("SELECT @_display_senate_two_2")
                        result = cursor.fetchone()[0]
                        conn.commit()
                        st.success(f"Number of rows displayed successfully: {num_rows_updated}")
                    elif name_input:
                        query = "SELECT * FROM senate WHERE name=%s"
                        cursor.execute(query, (name_input,))
                        updated_rows = cursor.fetchall()
                        df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                        num_rows_updated = len(df_updated)
                        st.write(f"Number of rows affected: {num_rows_updated}")
                        st.table(df_updated)
                        cursor.callproc("display_senate_one", (pos,name_input, 0))  # Pass an OUT parameter
                        cursor.execute("SELECT @_display_senate_one_1")
                        result = cursor.fetchone()[0]
                        conn.commit()
                        st.success(f"Number of rows displayed successfully: {num_rows_updated}")
                    elif major_input:
                        query = "SELECT * FROM senate WHERE major=%s"
                        cursor.execute(query, (major_input,))
                        updated_rows = cursor.fetchall()
                        df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                        num_rows_updated = len(df_updated)
                        st.write(f"Number of rows affected: {num_rows_updated}")
                        st.table(df_updated)
                        cursor.callproc("display_senate_one", (maj,major_input, 0))  # Pass an OUT parameter
                        cursor.execute("SELECT @_display_senate_one_1")
                        result = cursor.fetchone()[0]
                        conn.commit()
                        st.success(f"Number of rows displayed successfully: {num_rows_updated}")
                    elif year_input:
                        query = "SELECT * FROM senate WHERE year=%s"
                        cursor.execute(query, (year_input,))
                        updated_rows = cursor.fetchall()
                        df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                        num_rows_updated = len(df_updated)
                        st.write(f"Number of rows affected: {num_rows_updated}")
                        st.table(df_updated)
                        cursor.callproc("display_senate_one", (y,year_input, 0))  # Pass an OUT parameter
                        cursor.execute("SELECT @_display_senate_one_1")
                        result = cursor.fetchone()[0]
                        conn.commit()
                        st.success(f"Number of rows displayed successfully: {num_rows_updated}")
                    else:
                        query = "SELECT * FROM senate"
                        cursor.execute(query)
                        updated_rows = cursor.fetchall()
                        df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                        num_rows_updated = len(df_updated)
                        st.write(f"Number of rows affected: {num_rows_updated}")
                        st.table(df_updated)
                        cursor.callproc("display_senate_all", (0,))  # Pass an OUT parameter
                        cursor.execute("SELECT @_display_senate_all_0")
                        result = cursor.fetchone()[0]
                        conn.commit()
                        st.success(f"Number of rows displayed successfully: {num_rows_updated}")

                    rows = cursor.fetchall()
                        

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
        major_input = st.text_input(label='Enter the Major:')
        year_input = st.text_input(label='Enter the Year:')
        phone_input=  st.text_input(label='Enetr the phone')
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
                    try:
                        cursor.callproc("insert_into_senate", (netid_input, name_input, phone_input, major_input, year_input, 0))
                        cursor.execute("SELECT @p_rows_affected")
                        result = cursor.fetchone()[0]
                        result=1 
                        conn.commit()
                        st.write("Number of rows inserted sucessfully: ", result)
                        st.success("Details added successfully!")
                    except mysql.connector.Error as e:
                        st.error(f"Error executing procedure: {e}")

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
                        try:
                            # Call the stored procedure
                            query=f"SELECT * FROM senate WHERE {filter_field_input} = %s"
                            cursor.execute(query,(filter_data_input,))
                            updated_rows = cursor.fetchall()
                            cursor.callproc("update_senate", (field_input, data_input, filter_field_input, filter_data_input, 0))
                            # Store the updated data in a DataFrame
                            df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                            # Count the number of rows in the DataFrame
                            num_rows_updated = len(df_updated)
        
                            # Display the updated DataFrame and the number of rows updated
                            #st.write("Updated DataFrame:")
                            #st.write(df_updated)
                            #st.write(f"Number of rows updated: {num_rows_updated}")
                            conn.commit()
                            st.success(f"Number of rows updated successfully: {num_rows_updated}")
                        except mysql.connector.Error as e:
                            st.error(f"Error executing procedure: {e}")


                        finally:
                            if conn.is_connected():
                                cursor.close()
                                conn.close()
                    else:
                        try:
                            # Call the stored procedure
                            cursor.callproc("update_senate",(field_input,0))
                            # Fetch the output parameter value
                            query=f"SELECT * FROM senate"
                            cursor.execute(query,())
                            updated_rows = cursor.fetchall()

                            # Store the updated data in a DataFrame
                            df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                            # Count the number of rows in the DataFrame
                            num_rows_updated = len(df_updated)
                            cursor.callproc("update_senate_for_all", (field_input, data_input, 0))
                            # Display the updated DataFrame and the number of rows updated
                            #st.write("Updated DataFrame:")
                            #st.write(df_updated)
                            #st.write(f"Number of rows updated: {num_rows_updated}")
                            conn.commit()
                            st.success(f"Number of rows updated successfully: {num_rows_updated}")
                        except mysql.connector.Error as e:
                            st.error(f"Error executing procedure: {e}")

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
        name_input = st.text_input(label='Enter the name:')
        major_input = st.text_input(label='Enter the Major:')
        year_input = st.text_input(label='Enter the Year:')
        submit_button = st.form_submit_button(label='Delete')
        y="year"
        maj="major"
        pos="name"
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
                    if name_input and major_input and year_input:
                        query=f"SELECT * FROM senate WHERE name= %s and major=%s and year=%s"
                        cursor.execute(query,(name_input,major_input,year_input))
                        updated_rows = cursor.fetchall()
                        df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                        num_rows_updated = len(df_updated)
                        cursor.callproc("delete_senate_three", (pos,name_input,maj, major_input,y, year_input, 0))  # Pass an OUT parameter
                        cursor.execute("SELECT @_delete_senate_three_3")
                        result = cursor.fetchone()[0]
                        conn.commit()
                        st.success(f"Number of rows deleted successfully: {num_rows_updated}")

                    elif name_input and major_input:
                        query=f"SELECT * FROM senate WHERE name= %s and major=%s"
                        cursor.execute(query,(name_input,major_input))
                        updated_rows = cursor.fetchall()
                        df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                        num_rows_updated = len(df_updated)
                        cursor.callproc("delete_senate_two", (pos,name_input,maj, major_input, 0))  # Pass an OUT parameter
                        cursor.execute("SELECT @_delete_senate_two_2")
                        result = cursor.fetchone()[0]
                        conn.commit()
                        st.success(f"Number of rows deleted successfully: {num_rows_updated}")

                    elif name_input and year_input:
                        query=f"SELECT * FROM senate WHERE name= %s and year=%s"
                        cursor.execute(query,(name_input,year_input))
                        updated_rows = cursor.fetchall()
                        df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                        num_rows_updated = len(df_updated)
                        cursor.callproc("delete_senate_two",(pos,name_input, y,year_input, 0))  # Pass an OUT parameter
                        cursor.execute("SELECT @_delete_senate_two_2")
                        result = cursor.fetchone()[0]
                        conn.commit()
                        st.success(f"Number of rows deleted successfully: {num_rows_updated}")

                    elif major_input and year_input:
                        query=f"SELECT * FROM senate WHERE major=%s and year=%s"
                        cursor.execute(query,(major_input,year_input))
                        updated_rows = cursor.fetchall()
                        df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                        num_rows_updated = len(df_updated)
                        cursor.callproc("delete_senate_two", (maj,major_input,y, year_input, 0))  # Pass an OUT parameter
                        cursor.execute("SELECT @_delete_senate_two_2")
                        result = cursor.fetchone()[0]
                        conn.commit()
                        st.success(f"Number of rows deleted successfully: {num_rows_updated}")

                    elif name_input:
                        query=f"SELECT * FROM senate WHERE name= %s"
                        cursor.execute(query,(name_input))
                        updated_rows = cursor.fetchall()
                        df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                        num_rows_updated = len(df_updated)
                        cursor.callproc("delete_senate_one", (pos,name_input, 0))  # Pass an OUT parameter
                        cursor.execute("SELECT @_delete_senate_one_1")
                        result = cursor.fetchone()[0]
                        conn.commit()
                        st.success(f"Number of rows deleted successfully: {num_rows_updated}")

                    elif major_input:
                        query=f"SELECT * FROM senate WHERE major=%s" 
                        cursor.execute(query,(major_input))
                        updated_rows = cursor.fetchall()
                        df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                        num_rows_updated = len(df_updated)
                        cursor.callproc("delete_senate_one", (maj,major_input, 0))  # Pass an OUT parameter
                        cursor.execute("SELECT @_delete_senate_one_1")
                        result = cursor.fetchone()[0]
                        conn.commit()
                        st.success(f"Number of rows deleted successfully: {num_rows_updated}")

                    elif year_input:
                        query=f"SELECT * FROM senate WHERE year=%s"
                        cursor.execute(query,(year_input))
                        updated_rows = cursor.fetchall()
                        df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                        num_rows_updated = len(df_updated)
                        cursor.callproc("delete_senate_one", (y,year_input, 0))  # Pass an OUT parameter
                        cursor.execute("SELECT @_delete_senate_one_1")
                        result = cursor.fetchone()[0]
                        conn.commit()
                        st.success(f"Number of rows deleted successfully: {num_rows_updated}")

                    else:
                        query=f"SELECT * FROM senate"
                        cursor.execute(query,())
                        updated_rows = cursor.fetchall()
                        df_updated = pd.DataFrame(updated_rows, columns=[i[0] for i in cursor.description])
                        num_rows_updated = len(df_updated)
                        cursor.callproc("delete_all_senate", (0,))  # Pass an OUT parameter
                        cursor.execute("SELECT @_delete_all_senate_0")
                        result = cursor.fetchone()[0]
                        conn.commit()
                        st.success(f"Number of rows deleted successfully: {num_rows_updated}")
        except mysql.connector.Error as e:
            st.error(f"Error connecting to MySQL database: {e}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
