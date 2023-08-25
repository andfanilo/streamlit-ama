import json
import streamlit as st

from google.cloud import firestore
from google.oauth2 import service_account
from streamlit_elements import elements
from streamlit_elements import html
from streamlit_elements import mui


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
    return [m.to_dict() for m in all_messages]


def main():
    if "page" not in st.session_state:
        st.session_state.page = 0

    with st.sidebar:
        entered_pwd = st.text_input("Enter Password", type="password")
    if entered_pwd != st.secrets["admin_password"]:
        st.error("Enter correct password", icon="🚨")
        st.stop()

    def handle_change(_, page):
        st.session_state.page = page - 1

    all_messages = get_all_messages()

    st.title(":balloon: Fanilo's AMA | Admin dashboard")

    with elements("main"):
        mui.Divider()

        message = all_messages[st.session_state.page]["message"]
        author = all_messages[st.session_state.page]["name"]
        author = author if author != "" else "anonymous"

        with mui.Box(
            sx={
                "my": 3,
                "p": 3,
                "bgcolor": "background.paper",
                "boxShadow": 1,
                "borderRadius": 2,
            }
        ):
            mui.Typography(message)
            mui.Typography(
                f"by {author}",
                typography="subtitle2",
                fontWeight="light",
                textAlign="right",
                sx={"mt": 3},
            )

        mui.Pagination(count=len(all_messages), defaultPage=1, onChange=handle_change)

    with st.expander("Show all questions"):
        st.write(all_messages)


if __name__ == "__main__":
    st.set_page_config(page_title="Fanilo's AMA | Admin", page_icon=":balloon:")
    main()
