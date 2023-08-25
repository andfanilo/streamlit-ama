import json

import firebase_admin
import pandas as pd
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
    all_messages = db.collection("messages").order_by("date").stream()
    df = pd.DataFrame([m.to_dict() for m in all_messages])
    df = df[get_schema()]
    return df


def main():
    with st.sidebar:
        entered_pwd = st.text_input("Enter Password", type="password")
    if entered_pwd != st.secrets["admin_password"]:
        st.error("Enter correct password", icon="🚨")
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
