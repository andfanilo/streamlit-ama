import json
from datetime import datetime

import firebase_admin
import streamlit as st
from firebase_admin import credentials
from firebase_admin import firestore

from models import Schema

@st.cache_resource
def get_db():
    db = firestore.client()
    return db


def post_message(db, input_name, input_message):
    payload = {
        Schema.name.value: input_name,
        Schema.message.value: input_message,
        Schema.answer.value: "",
        Schema.date.value: datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
    }
    doc_ref = db.collection("messages").document()
    doc_ref.set(payload)
    return


def main():
    st.title("Fanilo's AMA")
    st.markdown(
        "Accepting questions/rants/compliments around content creation/YouTube/Twitter, Streamlit/Python/Data Science libraries, career life/non-invasive personal life in general"
    )
    st.markdown(
        "Answers may appear in a future [Youtube 10k AMA video](https://www.youtube.com/@andfanilo/)"
    )

    db = get_db()

    with st.form(key="form"):
        input_name = st.text_input("Your name (optional)", help="Can be anonymous")
        input_message = st.text_area("Your message")

        if st.form_submit_button("Submit form", type="primary"):
            if not input_message:
                st.error("Please provide a message :balloon:")
                        
            else:
                post_message(db, input_name, input_message)
                st.success("Your message was posted!")
                st.balloons()

    with st.sidebar:
        st.subheader("Where to find me")
        st.link_button("🌐 My socials", "https://andfanilo.com/")
        st.link_button("📧 My email list", "https://andfanilo-newsletter.streamlit.app/")

if __name__ == "__main__":
    st.set_page_config(page_title="Fanilo's AMA", page_icon=":balloon:")

    key_dict = json.loads(st.secrets["secret_account_key"])
    creds = credentials.Certificate(key_dict)

    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(creds)

    main()
