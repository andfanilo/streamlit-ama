import json
import streamlit as st
from datetime import datetime

from google.cloud import firestore
from google.cloud.firestore import Client
from google.oauth2 import service_account


@st.cache_resource
def get_db():
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project=st.secrets["project_name"])

    return db


def post_message(db: Client, input_name, input_message):
    payload = {
        "name": input_name,
        "message": input_message,
        "answer": "",
        "date": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
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
        "Answers may appear in a future [Youtube 5k AMA video](https://www.youtube.com/@andfanilo/)"
    )

    db = get_db()

    with st.form(key="form"):
        input_name = st.text_input("Your name (optional)", help="Can be anonymous")
        input_message = st.text_area("Your message")

        if st.form_submit_button("Submit form", disabled=(input_message=="")):
            post_message(db, input_name, input_message)
            st.success("Your message was posted!")
            st.balloons()


if __name__ == "__main__":
    st.set_page_config(page_title="Fanilo's AMA", page_icon=":balloon:")
    main()
