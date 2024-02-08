import streamlit as st

from cdc_bot.ingest import get_index

st.header("Chat with the CDC Dataset💬 📚")
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question!",
        }
    ]


@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Indexing documents, - hang tight!"):
        return get_index()


index = load_data()

chat_engine = index.as_chat_engine(chat_mode="context", verbose=True)

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)
