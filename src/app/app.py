import streamlit as st
import requests

# OAuth login (to be implemented)
# ...


def main():
    st.title("FastAPI Streamlit Demo")

    # Demo GET request
    if st.button("Get Data"):
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            data = response.json()
            st.success(f"API says: {data['message']}")
        else:
            st.error("Could not connect to the backend API.")


if __name__ == "__main__":
    main()