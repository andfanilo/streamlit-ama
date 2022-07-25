import streamlit as st

from google.cloud import firestore
from google.cloud.firestore import Client


@st.experimental_singleton
def get_db():
    db = firestore.Client.from_service_account_json("key.json")
    return db


def post_message(db: Client, input_name, input_message):
    payload = {
        "name": input_name,
        "message": input_message,
        "answer": None,
    }
    doc_ref = db.collection("messages").document()

    doc_ref.set(payload)
    return


def main():
    st.title("Admin page")
    db = get_db()

    all_messages = db.collection("messages")

    for doc in all_messages.stream():
        st.json(doc.to_dict())


if __name__ == "__main__":
    st.set_page_config(page_title="Fanilo's AMA Admin", page_icon=":glasses:")
    main()
