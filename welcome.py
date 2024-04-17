import streamlit as st
import os
import importlib.util

# Function to import and execute the content of a Python file
def import_and_execute_python_file(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)

    # Load the module
    spec = importlib.util.spec_from_file_location("module_name", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Call a specific function from the module if needed
    if hasattr(module, "run"):
        module.run()

if __name__ == "__main__":
    st.set_page_config(page_title="Option Menu", layout="wide")

    # Constant title with customization
    st.markdown("<h1 style='text-align: center; color: #FD3843;'>Logix Connect</h1>", unsafe_allow_html=True)

    # Option menu
    selected_page = st.sidebar.selectbox("Navigation", ["Club", "Office Bearers", "Executive Cabinet", "Class Representatives", "About Us"],
                                         index=0)
    
    # Import and execute the selected page
    if selected_page == "Club":
        st.title("Club")
        import_and_execute_python_file("club_display.py")
    elif selected_page == "Office Bearers":
        st.title("Office Bearers")
        import_and_execute_python_file("ob_display.py")
    elif selected_page == "Executive Cabinet":
        st.title("Executive Cabinet")
        import_and_execute_python_file("ec_python.py")
    elif selected_page == "Class Representatives":
        st.title("Class Representatives")
        import_and_execute_python_file("senate_display.py")
    elif selected_page == "About Us":
        st.title("About Us")
        import_and_execute_python_file("about.py")
