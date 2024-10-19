import streamlit as st
from PIL import Image

# Page layout and configuration - must be the first command
st.set_page_config(page_title="Image Song Recommender", layout="centered")

# Custom CSS to enhance the UI design
st.markdown("""
    <style>
        .stApp {
            background-color:black;
            font-family: 'Arial', sans-serif;
        }
        .title {
            font-size: 60px;
            color: #ff4b4b;
            text-align: center;
            font-weight: bold;
        }
        .subtitle {
            font-size: 30px;
            text-align: center;
            margin-top: -20px;
        }
        .section-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .file-upload {
            text-align: center;
            font-size: 20px;
        }
        .song-results {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        }
        .song-title {
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Header section with title and subtitle
st.markdown('<div class="title">🎵 Image Vibes Recommender 🎵</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Discover the perfect songs for your Instagram stories!</div>', unsafe_allow_html=True)

# Image uploader section
st.markdown('<div class="section-title">Step 1: Upload an Image</div>', unsafe_allow_html=True)
uploaded_image = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

# Show uploaded image and continue processing
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Language selection
    st.markdown('<div class="section-title">Step 2: Select Language</div>', unsafe_allow_html=True)
    language = st.selectbox("Select Language", ("English", "Hindi"))

    # Artist selection
    st.markdown('<div class="section-title">Step 3: Select Top 5 Artists</div>', unsafe_allow_html=True)
    artists = st.multiselect("Choose Artists", ["Artist1", "Artist2", "Artist3", "Artist4", "Artist5"])

    # Year selection (optional)
    st.markdown('<div class="section-title">Step 4: Select Year (Optional)</div>', unsafe_allow_html=True)
    year = st.text_input("Enter Year (optional)")

    # Find songs button
    if st.button("Find Songs"):
        # Display placeholder song recommendations
        st.markdown('<div class="section-title">Top 5 Song Recommendations</div>', unsafe_allow_html=True)
        for i in range(1, 6):
            st.markdown(f"""
                <div class="song-results">
                    <div class="song-title">Artist {i} - Song {i}</div>
                    <div>Description: Placeholder description for song {i}</div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.markdown('<div class="file-upload">Please upload an image to get started.</div>', unsafe_allow_html=True)
