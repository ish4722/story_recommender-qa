import streamlit as st
from PIL import Image
from io import BytesIO
import base64
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import description_page
import music

# Page layout and configuration
st.set_page_config(page_title="Image Song Recommender", layout="wide")

model = SentenceTransformer('all-mpnet-base-v2')
def get_embedding(text):
    return model.encode(text)

def compute_similarity(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]

def rank_songs(top_n=5):
    similarities = []
    song_descriptions=description_page.refined_discription_music()
    image_description=music.refined_description_call()
    image_embedding= get_embedding(image_description)

    for song_description in song_descriptions:
        song_embedding = get_embedding(song_description)
        
        similarity = compute_similarity(image_embedding, song_embedding)
        similarities.append((song_description, similarity))

    # Sort songs by similarity in descending order and return the top N
    sorted_songs = sorted(similarities, key=lambda x: x[1], reverse=True)
    return sorted_songs[:top_n]





# Custom CSS for background and design
st.markdown("""
    <style>
        .stApp {
            background-color: #343434; /* ChatGPT-like background */
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
        .history-block {
            border: 2px solid #ff4b4b;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 15px;
            background-color: #f9f9f9;
        }
        .image-container {
            text-align: center;
            margin-bottom: 10px;
        }
        .history-title {
            font-size: 20px;
            font-weight: bold;
            text-align: center;
            color: #ff4b4b;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for storing song and image history
st.sidebar.title("Song & Image History")
if "song_history" not in st.session_state:
    st.session_state.song_history = []  # Initialize song history in session state

# Function to convert image to base64 string
def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Display history of previously recommended songs and images in a block format
st.sidebar.subheader("History")
if len(st.session_state.song_history) > 0:
    for entry in st.session_state.song_history:
        image_base64 = entry.get('image_base64', '')
        songs = entry.get('songs', [])
        image_name = entry.get('image_name', 'Unknown Image')

        st.sidebar.markdown(f"""
            <div class="history-block">
                <div class="history-title">Image: {image_name}</div>
                <div class="image-container">
                    <img src="data:image/jpeg;base64,{image_base64}" alt="{image_name}" width="100%">
                </div>
                <div class="history-title">Recommended Songs:</div>
                <ul>
                    {''.join([f"<li>{song}</li>" for song in songs])}
                </ul>
            </div>
        """, unsafe_allow_html=True)

# Header section with title and subtitle
st.markdown('<div class="title">🎵 Image Vibes Recommender 🎵</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Discover the perfect songs for your Instagram stories!</div>', unsafe_allow_html=True)

# Image uploader section
st.markdown('<div class="section-title">Step 1: Upload an Image</div>', unsafe_allow_html=True)
uploaded_image = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

# Artist options based on language selection
artist_options = {
    "English": [
        "Taylor Swift", "Ed Sheeran", "The Weeknd", "Justin Bieber", 
        "Dua Lipa", "Ariana Grande", "Billie Eilish", "Doja Cat", 
        "Olivia Rodrigo", "Harry Styles"
    ],
    "Hindi": [
        "Arijit Singh", "Neha Kakkar", "Badshah", "Shreya Ghoshal", 
        "Jubin Nautiyal", "Darshan Raval", "Yo Yo Honey Singh", 
        "Guru Randhawa", "Raftaar", "B Praak"
    ],
    "Punjabi": [
        "Sidhu Moose Wala", "Diljit Dosanjh", "Guru Randhawa", "Ammy Virk", 
        "Jassi Gill", "Karan Aujla", "AP Dhillon", "B Praak", 
        "Garry Sandhu", "Raftaar"
    ]
}

# Show uploaded image and continue processing
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.session_state['uploaded_image'] = uploaded_image

    # Convert image to base64 for display in history blocks
    image_base64 = image_to_base64(image)

    # Language selection
    st.markdown('<div class="section-title">Step 2: Select Language</div>', unsafe_allow_html=True)
    language = st.selectbox("Select Language", ("English", "Hindi", "Punjabi"))

    # Artist selection based on the selected language
    st.markdown('<div class="section-title">Step 3: Select Top 5 Artists</div>', unsafe_allow_html=True)
    artists = st.multiselect("Choose Artists", artist_options[language])

    # Year selection (optional)
    st.markdown('<div class="section-title">Step 4: Select Year (Optional)</div>', unsafe_allow_html=True)
    year = st.text_input("Enter Year (optional)")

    # Find songs button
    if st.button("Find Songs"):
        # Check if the user has selected any artists
        if len(artists) == 0:
            # Show error pop-up if no artist is selected
            st.error("Please select at least one artist before proceeding!")
        else:
            # Generate placeholder song recommendations
            st.markdown('<div class="section-title">Top 5 Song Recommendations</div>', unsafe_allow_html=True)
            recommended_songs = []
            for i in rank_songs():
                song_name = i;  # Random artist from the selection
                st.markdown(f"""
                    <div class="song-results">
                        <div class="song-title">{i}</div>
                        # <div>Description: Placeholder description for song {i}</div>
                    </div>
                """, unsafe_allow_html=True)
                recommended_songs.append(i)

            # Store the song and image information in session state for history in a block format
            st.session_state.song_history.append({
                "image_name": uploaded_image.name,
                "image_base64": image_base64,
                "songs": recommended_songs
            })

# Clear history button (will not clear on new uploads, only if clicked)
if st.sidebar.button("Clear History"):
    st.session_state.song_history = []  # Clear song history
    #st.experimental_rerun()  # Refresh the app
