# Streamlit AMA

A Streamlit app for users to send questions, all stored into Firebase.

## Local setup

Create a `.streamlit/secrets.toml` file. You will need to store the following variables:
* `project_name`: id of the Firebase project
* `admin_password`: if running `st_admin.py`, a password to the app
* `textkey`: Firebase JSON secret key. Generate one as JSON and copy it as one-liner. 
