import streamlit as st
from huggingface_hub import InferenceClient

# Set up the UI
st.set_page_config(page_title="OpenStoryboard AI", layout="wide")
st.title("🎬 OpenStoryboard: AI Video Pipeline")

hf_token = st.text_input("Enter your free Hugging Face Token:", type="password")
user_input = st.text_area("Paste your archive text, lore, or game design notes here:")

if st.button("Generate Storyboard") and hf_token and user_input:
    # Using the official client handles all the messy backend routing automatically
    client = InferenceClient(api_key=hf_token)
    
    prompt = f"Turn this text into a 3-scene video storyboard. Provide a voiceover script and a visual generation prompt for each scene:\n\n{user_input}"
    
    with st.spinner("Processing through the Official SDK..."):
        try:
            # We are using Qwen 2.5, which is currently Hugging Face's most supported open model
            messages = [{"role": "user", "content": prompt}]
            response = client.chat_completion(
                model="Qwen/Qwen2.5-72B-Instruct", 
                messages=messages, 
                max_tokens=500
            )
            
            st.success("Storyboard Generated!")
            st.write(response.choices[0].message.content)
            
        except Exception as e:
            st.error(f"A connection error occurred: {e}")
