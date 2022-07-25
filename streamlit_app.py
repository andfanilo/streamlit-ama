import streamlit as st

from google.cloud import firestore
from google.cloud.firestore import Client


@st.experimental_singleton
def get_db():
    db = firestore.Client.from_service_account_json("key.json")
    return db


def post_message(db: Client, input_name, input_message, is_private):
    payload = {
        "name": input_name,
        "message": input_message,
        "isPrivate": is_private,
        "answer": None,
    }
    doc_ref = db.collection("messages").document()

    doc_ref.set(payload)
    return


def main():
    st.title("Fanilo's AMA")

    db = get_db()

    with st.form(key="form"):
        input_name = st.text_input("Your name (optional)", help="can be anonymous")
        input_message = st.text_area("Your question?")
        is_private = st.checkbox("Hide your message from the public board", False)

        if st.form_submit_button("Submit form"):
            post_message(db, input_name, input_message, is_private)
            st.success("Your message was posted!")
            st.balloons()


if __name__ == "__main__":
    st.set_page_config(page_title="Fanilo's AMA", page_icon=":balloon:")
    main()
