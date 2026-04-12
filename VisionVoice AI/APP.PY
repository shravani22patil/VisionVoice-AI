import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import PIL.Image
import io
import re

# --- PAGE CONFIG ---
st.set_page_config(page_title="VisionVoice AI", page_icon="🎙️", layout="wide")

# --- UI STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #FF4B4B; color: white; }
    .res-card { padding: 20px; border-radius: 15px; background: white; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: SECRETS & CONFIG ---
with st.sidebar:
    st.title("⚙️ Configuration")
    # In production, use st.secrets["GEMINI_KEY"]
    # Use the actual string from AI Studio
    api_key = "" 
    genai.configure(api_key=api_key)
    st.info("Get a free key at Google AI Studio")

# --- CORE LOGIC ---
def analyze_image(img, lang):
    if not api_key.strip(): # Check if key is empty
        st.error("Please provide an API Key in the sidebar!")
        return None, None
    
    # Use the latest stable model
    model = genai.GenerativeModel('gemini-flash-latest')
    
    prompt = f"""
    Act as a professional technical analyst. Summarize this image in {lang}.
    If it's a GADGET: List name, 3 features, and a maintenance tip.
    If it's a RECEIPT: List store, total, and top 2 expensive items.
    Format with clean markdown bolding.
    """
    
    with st.spinner(f"AI is analyzing in {lang}..."):
        try:
            # 1. Generate content from Gemini
            response = model.generate_content([prompt, img])
            raw_text = response.text 

            # 2. Clean text for the voice engine (No asterisks/hashes)
            clean_text_for_voice = re.sub(r'[\*\#\_]', '', raw_text)
            
            # 3. Create Audio
            lang_codes = {"English": "en", "Hindi": "hi", "Marathi": "mr"}
            tts = gTTS(text=clean_text_for_voice, lang=lang_codes[lang])
            
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            
            return raw_text, audio_fp
        except Exception as e:
            st.error(f"Analysis failed: {e}")
            return None, None
    
# --- MAIN UI ---
st.title("🎙️ VisionVoice AI: Multimodal Explorer")
st.write("Bridging Vision and Audio for Gadgets & Receipts.")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    selected_lang = st.selectbox("Output Language", ["English", "Hindi", "Marathi"])
    
    if uploaded_file:
        image = PIL.Image.open(uploaded_file)
        st.image(image, caption="Uploaded View", use_container_width=True)
        
        if st.button("🚀 Analyze & Speak"):
            text, audio = analyze_image(image, selected_lang)
            st.session_state['text'] = text
            st.session_state['audio'] = audio

with col2:
    if 'text' in st.session_state:
        st.subheader("📝 Analysis Result")
        st.markdown(f"<div class='res-card'>{st.session_state['text']}</div>", unsafe_allow_html=True)
        
        st.subheader("🔊 Audio Summary")
        st.audio(st.session_state['audio'], format="audio/mp3")