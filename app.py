import streamlit as st
import requests

# Set up the UI
st.set_page_config(page_title="OpenStoryboard AI", layout="wide")
st.title("🎬 OpenStoryboard: AI Video Pipeline")

# The NEW Hugging Face Router API setup
API_URL = "https://router.huggingface.co/v1/chat/completions"
hf_token = st.text_input("Enter your free Hugging Face Token:", type="password")

user_input = st.text_area("Paste your archive text, lore, or game design notes here:")

if st.button("Generate Storyboard") and hf_token and user_input:
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }
    
    # The prompt instructing the open-source model what to do
    prompt = f"Turn this text into a 3-scene video storyboard. Provide a voiceover script and a visual generation prompt for each scene:\n\n{user_input}"
    
    # The updated payload using Zephyr
    payload = {
        "model": "HuggingFaceH4/zephyr-7b-beta",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500
    }
    
    with st.spinner("Processing through Open-Source AI..."):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                st.success("Storyboard Generated!")
                response_json = response.json()
                
                if 'choices' in response_json and len(response_json['choices']) > 0:
                    output_text = response_json['choices'][0]['message']['content']
                    st.write(output_text)
                else:
                    st.error("The AI woke up but sent the wrong format. Click Generate again.")
            else:
                st.error(f"API Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"A connection error occurred: {e}")
