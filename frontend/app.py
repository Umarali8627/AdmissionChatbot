import requests
import streamlit as st


st.set_page_config(page_title="Admission Chatbot", page_icon=":mortar_board:", layout="centered")

DEFAULT_API_BASE = "http://127.0.0.1:8000"


def ask_chatbot(api_base_url: str, user_input: str) -> str:
    response = requests.get(
        f"{api_base_url.rstrip('/')}/chat/ask",
        params={"user_input": user_input},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return payload.get("result", "No response returned from API.")


st.title("Admission Chatbot")
st.caption("Streamlit frontend for your FastAPI admission assistant.")

with st.sidebar:
    st.subheader("API Settings")
    api_base_url = st.text_input("Backend URL", value=DEFAULT_API_BASE)
    st.markdown("Make sure FastAPI is running before sending messages.")
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask about admissions, programs, fees, deadlines...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = ask_chatbot(api_base_url, prompt)
            except requests.RequestException as exc:
                answer = (
                    "Could not reach the backend API. "
                    f"Please verify the URL and backend status.\n\nError: `{exc}`"
                )
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
