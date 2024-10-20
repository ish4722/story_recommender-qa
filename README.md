# 📄 Document question answering template

A simple Streamlit app that answers questions about an uploaded document via OpenAI's GPT-3.5.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://document-question-answering-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run demo.py
   ```


# StorySong_recommender 
### https://drive.google.com/file/d/1VMSFs3oC2jXVQsRVs1lqTKIJiS1sFxIS 


## Project Overview & Problem Statement
In today's fast-paced social media landscape, Instagram users struggle with selecting the perfect song for their stories. With millions of tracks available, manually searching for the right one is time-consuming and often fails to capture the desired emotional tone. Our project aims to solve this issue with an AI-driven song recommender that takes an image as input and suggests songs that match the mood, vibe, and context of the image. By automating this process, we not only save users time but also enhance their storytelling experience, allowing them to pair music with visuals seamlessly.

## How Our Solution Works
## Image Understanding Through AI
We begin by analyzing the uploaded image using BLIP (Bootstrapping Language-Image Pre-training), an advanced image captioning model. This model generates a contextual description of the image, capturing the essential visual components.

## Emotionally Rich Descriptions
Once the initial caption is generated, we elevate it with Google’s Gemini VLM (Vision-Language Model). This model provides a detailed, emotionally-driven description that captures nuanced elements such as facial expressions, gestures, and the overall atmosphere of the image. This refined description is rich with emotional context, ensuring that the song selection resonates deeply with the visual content.

## Song Lyrics Analysis
On the musical side, we analyze song lyrics from the top artists, breaking them down using Google's Gemini model to generate concise descriptions of each song. These descriptions focus on genre, tempo, emotional themes, and vibe, providing an understanding of the song’s essence beyond just words.

## Embedding and Similarity Matching
To match the song to the image, we convert both the refined image description and the song descriptions into vector embeddings using a pre-trained SentenceTransformer model. We then use cosine similarity to rank the songs based on their alignment with the image’s emotional tone. This allows us to recommend the top 5 songs that match the mood and context of the image.

## Real-Time Recommendations
Our system is designed for efficiency. By using embeddings and similarity matching, we can deliver real-time recommendations, making it easy for users to instantly receive music suggestions that enhance their visual stories.

## Technical Innovation

## AI-Powered Visual and Emotional Analysis
We leverage state-of-the-art AI models—BLIP and Gemini—to extract and refine rich visual and emotional cues from an image. This sophisticated pipeline transforms basic image captioning into a process that deeply understands the image’s emotional narrative.

## Deep Lyrical Understanding
Our system doesn’t just consider the music but also dives into the emotional depth of song lyrics. Using natural language processing (NLP), we ensure that the song’s narrative aligns with the emotional tone of the image, providing a multi-layered matching experience.

## Seamless User Experience
By combining the visual and emotional analysis with instant recommendations, our system delivers a fluid, intuitive user experience. With one image upload, users receive songs that amplify the emotion and vibe they want to share on social media.

## Challenges and Limitations
While our solution is highly innovative, we face significant challenges due to resource constraints and computational limitations. Our project relies on large-scale AI models like *LLama 11B* and *LLama 8B, with billions of parameters, which require extensive memory and processing power. However, platforms like **Google Colab, **Kaggle, and **Jupyter Notebooks* offer limited GPU and memory resources, leading to frequent *computational errors* and *long processing times*. These limitations force us to work with smaller datasets and optimize our code, sacrificing speed and scalability. With better infrastructure, our solution could achieve far greater potential.

All major code is included in demo file.It is receiving image description from description_page.py and receiving music discription from music.py.After that demo file provides a song recommendation.
User can also see the image explaination on description.py by entering a gemini api key.(we missed to add it on env file).
