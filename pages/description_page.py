import streamlit as st
import google.generativeai as genai
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# Show title and description.
st.title("📷 Image Description Refiner")
st.write(
    "The model will generate a description for the uploaded image, "
    "and this description will be refined by the Gemini model. You will need to provide your Gemini API key."
)

# Sidebar for storing image and description blocks
st.sidebar.title("📝 Saved Descriptions")
if "saved_descriptions" not in st.session_state:
    st.session_state.saved_descriptions = []

def add_to_sidebar(image, description):
    """Adds an image and its description to the session state"""
    st.session_state.saved_descriptions.append((image, description))

def remove_from_sidebar(index):
    """Removes an image and its description from the session state based on index"""
    del st.session_state.saved_descriptions[index]

# Ask the user for their Gemini API key.
gemini_key = st.text_input("Gemini API Key", type="password")

if not gemini_key:
    st.info("Please provide your Gemini API key to continue.", icon="🗝️")
else:
    # Configure the Google Gemini API
    genai.configure(api_key=gemini_key)

    # Check if the image exists in session state
    if "uploaded_image" not in st.session_state or st.session_state.uploaded_image is None:
        st.error("No image uploaded! Please upload an image in the main app first.")
    else:
        # Access the uploaded image from session state
        uploaded_image = st.session_state.uploaded_image
        image = Image.open(uploaded_image).convert('RGB')
        st.image(image, caption="Image from demo.py", use_column_width=True)

        # Load BLIP model for generating the initial caption
        st.write("Generating initial caption using BLIP...")
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model_blip = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

        # Preprocess the image and generate a caption
        inputs = processor(image, return_tensors="pt")
        out = model_blip.generate(**inputs)
        initial_caption = processor.decode(out[0], skip_special_tokens=True)

        st.write(f"**Initial Caption:** {initial_caption}")

        # Set up the Gemini model to refine the initial description
        gemini_model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=(
                "You are an expert in analyzing visual content and emotions."
                " For the given description, refine it into a more detailed and expressive description in 50-60 words, capturing the emotions, background, and key elements such as gestures, facial expressions, and environment."
                " The description should evoke the mood and context to inform a musical recommendation. Keep the language vivid and precise."
            )
        )

        # Feed the initial caption to Gemini for refinement
        st.write("Refining the caption with Gemini...")
        full_prompt = f"Description: {initial_caption}"
        response = gemini_model.generate_content([full_prompt])

        # Extract the refined description
        refined_description = None
        try:
            candidate = response.candidates[0]
            refined_description = candidate.content.parts[0].text
        except (IndexError, AttributeError) as e:
            st.error(f"Error extracting description: {e}")

        if refined_description:
            st.write(f"**Refined Description:** {refined_description}")
            # Add option to save the image and description in the sidebar
            if st.button("Save to Sidebar"):
                add_to_sidebar(uploaded_image, refined_description)
        else:
            st.warning("No description generated.")

# Display the saved descriptions in the sidebar with a delete button
for idx, (img, desc) in enumerate(st.session_state.saved_descriptions):
    st.sidebar.image(img, caption="Saved Image", use_column_width=True)
    st.sidebar.write(f"**Description:** {desc}")
    # Add a delete button for each block
    if st.sidebar.button(f"❌ Delete Description {idx+1}", key=f"delete_{idx}"):
        remove_from_sidebar(idx)
        # st.experimental_rerun()  # Rerun to refresh the sidebar after deletion
    st.sidebar.markdown("---")
