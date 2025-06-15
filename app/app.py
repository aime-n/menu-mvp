import streamlit as st
import requests
import uuid

def main():
    st.title("FastAPI Streamlit Demo")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What is up?", accept_file=False):
        # Display user message in chat message container
        st.chat_message("human").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "human", "content": prompt})

        response = requests.post(
            "http://localhost:8000/chat/invoke",
            json={
                "messages": [{"role": "human", "content": prompt}],
                "thread_id": st.session_state.thread_id
            }
        )

        # Display assistant response in chat message container
        with st.chat_message("ai"):
            if response.status_code == 200:
                response_data = response.json()
                response = response_data["output"]["content"]
            else:
                response = "Error: Could not connect to the backend API."
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "ai", "content": response})


if __name__ == "__main__":
    main()

