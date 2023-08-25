# Streamlit AMA

A Streamlit app for users to send questions, all stored into Firebase.

## Local setup

Create a `.streamlit/secrets.toml` file. You will need to store the following variables:
* `admin_password`: if running `st_admin.py`, a password to the app
* `secret_account_key`: Firebase JSON secret key. Generate one as JSON and copy it as one-liner
