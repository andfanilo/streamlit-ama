# Streamlit AMA

A Streamlit app for users to send questions, all stored into Firebase.

## Local setup

Create a `.streamlit/secrets.toml` file. You will need to store the following variables:
* `api_key`: Generated from web app setup in Firebase project. Used for REST Auth
* `secret_account_key`: Firebase JSON secret key. Generate one as JSON and copy it as one-liner
