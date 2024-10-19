# import streamlit as st
# from openai import OpenAI

# # Show title and description.
# st.title("📄 image answering")
# st.write(
#     "Upload a document below and ask a question about it – GPT will answer! "
#     "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
# )

# # Ask user for their OpenAI API key via `st.text_input`.
# # Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# # via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
# openai_api_key = st.text_input("OpenAI API Key", type="password")
# if not openai_api_key:
#     st.info("Please add your OpenAI API key to continue.", icon="🗝️")
# else:

#     # Create an OpenAI client.
#     client = OpenAI(api_key=openai_api_key)

#     # Let the user upload a file via `st.file_uploader`.
#     uploaded_file = st.file_uploader(
#         "Upload a document (.txt or .md)", type=("txt", "md")
#     )

#     # Ask the user for a question via `st.text_area`.
#     question = st.text_area(
#         "Now ask a question about the document!",
#         placeholder="Can you give me a short summary?",
#         disabled=not uploaded_file,
#     )

#     if uploaded_file and question:

#         # Process the uploaded file and question.
#         document = uploaded_file.read().decode()
#         messages = [
#             {
#                 "role": "user",
#                 "content": f"Here's a document: {document} \n\n---\n\n {question}",
#             }
#         ]

#         # Generate an answer using the OpenAI API.
#         stream = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=messages,
#             stream=True,
#         )

#         # Stream the response to the app using `st.write_stream`.
#         st.write_stream(stream)

# custom_css = """
# .title {
#     font-size: 70px;
#     font-family: 'Courier New', Courier, monospace;
# }

# .headline {
#     font-size: 40px;
#     font-family: 'Courier New', Courier, monospace;
# }

# .text-input {
#     font-size: 20px;
# }
# """


import streamlit as st
import google.generativeai as genai
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# Show title and description.
st.title("📷 Image Description Refiner")
st.write(
    "Upload an image below, and the model will generate a description. "
    "This description will then be refined by the Gemini model. You will need to provide your Gemini API key."
)

# Ask the user for their Gemini API key.
gemini_key = st.text_input("Gemini API Key", type="password")

if not gemini_key:
    st.info("Please provide your Gemini API key to continue.", icon="🗝️")
else:
    # Configure the Google Gemini API
    genai.configure(api_key=gemini_key)

    # Let the user upload an image
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    if uploaded_image:
        # Display the uploaded image
        image = Image.open(uploaded_image).convert('RGB')
        st.image(image, caption="Uploaded Image", use_column_width=True)

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
        else:
            st.warning("No description generated.")
