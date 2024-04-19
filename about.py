import streamlit as st

class AboutUsPage:
    def __init__(self):
        self.content = {
            "title": "About Our Project",
            "summary": "Our project aims to streamline club management within the university by providing a comprehensive platform for managing department clubs, general clubs, office bearers, and executive cabinet members.",
            "sections": [
                {
                    "title": "Our Mission",
                    "content": "Our mission is to create a user-friendly and efficient system that simplifies club management tasks, enhances communication, and fosters collaboration among club members."
                },
                {
                    "title": "Key Features",
                    "content": "1. Management of department clubs, general clubs, office bearers, and executive cabinet members.\n2. Integration of email functionality for easy communication.\n3. Secure user authentication and role-based access control.\n4. User-friendly interface with intuitive navigation.\n5. Comprehensive reporting and analytics tools."
                }
            ]
        }

    def render(self):
        st.title(self.content['title'])
        st.markdown("---")
        st.write(self.content['summary'])
        st.markdown("---")
        for section in self.content["sections"]:
            st.header(section['title'])
            st.write(section['content'])
        st.markdown(
            """
            <style>
                .st-eb {
                    background-color: #f0f2f6;
                    border-radius: 5px;
                    padding: 10px;
                }
            </style>
            """
            , unsafe_allow_html=True
        )

about_us_page = AboutUsPage()
about_us_page.render()
