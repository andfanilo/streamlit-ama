import json

import pandas as pd
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account

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
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project=st.secrets["project_name"])
    return db


@st.cache_resource
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
    main()
