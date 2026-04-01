import streamlit as st
import requests

# Set up the UI
st.set_page_config(page_title="OpenStoryboard AI", layout="wide")
st.title("🎬 OpenStoryboard: AI Video Pipeline")

# The Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
hf_token = st.text_input("Enter your free Hugging Face Token:", type="password")

user_input = st.text_area("Paste your archive text, lore, or game design notes here:")

if st.button("Generate Storyboard") and hf_token and user_input:
    headers = {"Authorization": f"Bearer {hf_token}"}
    
    # The prompt instructing the open-source model what to do
    prompt = f"<s>[INST] Turn this text into a 3-scene video storyboard. Provide a voiceover script and a visual generation prompt for each scene:\n\n{user_input} [/INST]"
    
    with st.spinner("Processing through Open-Source AI..."):
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 500}})
            
            if response.status_code == 200:
                st.success("Storyboard Generated!")
                response_json = response.json()
                # Ensure the model sent back the right format before trying to split it
                if isinstance(response_json, list) and 'generated_text' in response_json[0]:
                    output_text = response_json[0]['generated_text'].split('[/INST]')[1]
                    st.write(output_text)
                else:
                    st.error("The AI woke up but sent the wrong format. Click Generate again.")
            else:
                # This will print the EXACT reason the API failed
                st.error(f"API Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"A connection error occurred: {e}")
