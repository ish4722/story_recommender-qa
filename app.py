import streamlit as st
from PIL import Image

# Set page configuration
st.set_page_config(page_title="Image Song Recommender", layout="wide")

# Custom CSS for background and design
st.markdown("""
    <style>
        .stApp {
            background-color: #343434;
            font-family: 'Arial', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# Navigation between pages
def navigate_to(page_name):
    st.session_state.page = page_name

if "page" not in st.session_state:
    st.session_state.page = "landing"

if st.session_state.page == "landing":
    st.title("Discover Music through Your Photos 🎵📸")
    st.markdown("""
        <style>
            .big-title {
                font-size: 70px;
                text-align: center;
                color: #ff4b4b;
                transition: all 0.5s ease;
            }
        </style>
        <div class="big-title">Discover Music through Your Photos 🎵📸</div>
    """, unsafe_allow_html=True)
    
    if st.button("Start"):
        navigate_to("upload")

elif st.session_state.page == "upload":
    st.write("Welcome to the image upload page.")
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    if uploaded_image is not None:
        image = Image.open(uploaded_image).convert('RGB')
        st.image(image, caption="Uploaded Image", use_column_width=True)
        st.session_state.uploaded_image = image
        if st.button("Next"):
            navigate_to("description")

elif st.session_state.page == "description":
    if "uploaded_image" in st.session_state:
        st.image(st.session_state.uploaded_image, caption="Your Image", use_column_width=True)

        gemini_key = st.text_input("Gemini API Key", type="password")
        if not gemini_key:
            st.info("Please provide your Gemini API key to continue.", icon="🗝️")
        else:
            # Load and refine description using the Gemini model
            st.write("Generating refined description using Gemini...")
            # Here we simulate the Gemini integration, replace with actual API calls
            full_prompt = f"Description: {initial_caption}"
            response = gemini_model.generate_content([full_prompt])

            candidate = response.candidates[0]
            refined_description = candidate.content.parts[0].text
            st.write(f"**Refined Description:** {refined_description}")
    else:
        st.error("No image uploaded!")
