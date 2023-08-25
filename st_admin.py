import json

import firebase_admin
import pandas as pd
import requests
import streamlit as st
from firebase_admin import credentials
from firebase_admin import firestore

from models import Schema


def get_schema():
    return [
        Schema.date.value,
        Schema.name.value,
        Schema.message.value,
        Schema.answer.value,
    ]


@st.cache_resource
def get_db():
    db = firestore.client()
    return db


@st.cache_data(ttl=60)
def get_all_messages():
    db = get_db()
    all_messages = db.collection("messages").order_by(Schema.date.value).stream()
    df = pd.DataFrame([m.to_dict() for m in all_messages])
    df = df[get_schema()]
    return df


@st.cache_data(ttl=60)
def login(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={ st.secrets['api_key'] }"
    headers = {"Content-Type": "application/json"}
    data = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    return response_data


def main():
    if "auth_status" not in st.session_state:
        st.session_state["auth_status"] = None

    with st.sidebar.form("auth"):
        entered_email = st.text_input("Enter Email")
        entered_pwd = st.text_input("Enter Password", type="password")
        if st.form_submit_button("Login", type="primary"):
            st.session_state["auth_status"] = login(entered_email, entered_pwd)

    if st.session_state["auth_status"] is None:
        st.info("Please Login", icon="🔑")
        st.stop()

    if "error" in st.session_state["auth_status"]:
        st.error(
            f'Login Error: {st.session_state["auth_status"]["error"]["message"]}',
            icon="🚨",
        )
        st.stop()

    all_messages = get_all_messages()

    st.title(":balloon: Fanilo's AMA | Admin dashboard")

    st.dataframe(all_messages, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Fanilo's AMA | Admin", page_icon=":balloon:", layout="wide"
    )

    key_dict = json.loads(st.secrets["secret_account_key"])
    creds = credentials.Certificate(key_dict)

    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(creds)

    main()
