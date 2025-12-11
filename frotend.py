import streamlit as st  
import requests

API_URL = "http://localhost:8000/predict"
st.title("Check The News is Right or Rumor")

st.markdown("Enter your News below")

# input Feilds
text = st.text_input('Enter your News',value='About the American President')


if st.button("Predict Premium Category"):
    input_data = {
        "text":text
    }
    try:
        response = requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            result = response.json()
            # st.success(f"Predict about the News:{result['Predicted News']}**")
            st.success(f"Predict about the News: {result['Result']}")

        else:
            st.error(f"API error:{response.status_code}-{response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the FastAPI server,Make sure it's running on port 8080.")            
    