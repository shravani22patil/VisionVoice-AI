import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import PIL.Image
import io
import re

# --- PAGE CONFIG ---
st.set_page_config(page_title="VisionVoice AI", page_icon="🎙️", layout="wide")

# --- UI STYLING (Unified Glassmorphism & Fixed Buttons) ---
st.markdown("""
    <style>
    /* 1. Global Background */
    .stApp {
        background-color: #0E1117;
        color: #E6EDF3;
    }
    header {visibility: hidden;} 
    footer {visibility: hidden;}
    
    /* 2. Glassmorphism Card with Fade-In Animation */
    .res-card {
        padding: 25px;
        border-radius: 15px;
        background: rgba(22, 27, 34, 0.8);
        backdrop-filter: blur(12px);
        border: 1px solid #30363D;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        animation: fadeIn 0.8s ease-in;
        color: #E6EDF3;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* 3. Fixing File Uploader (No more white-on-white) */
    [data-testid="stFileUploader"] button {
        background-color: #161B22 !important;
        color: #FFFFFF !important;
        border: 1px solid #30363D !important;
    }
    
    [data-testid="stFileUploader"] button div {
        color: white !important;
    }

    [data-testid="stFileUploader"] section {
        color: rgba(255, 255, 255, 0.8) !important;
    }

    [data-testid="stFileUploader"] button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid #00d4ff !important;
    }

    /* 4. Button & Input Styling */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(88, 166, 255, 0.4);
        border: 1px solid #58A6FF;
    }

    div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: #161B22 !important;
        border: 1px solid #30363D !important;
        border-radius: 10px !important;
    }

    /* 5. Custom Loading Spinner */
    .stSpinner > div {
        border-top-color: #58A6FF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: CONFIG ---

with st.sidebar:
    st.title("⚙️ Configuration")
    
    # Check if the secret exists, otherwise fallback to empty string
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
    
    if api_key:
        genai.configure(api_key=api_key)
        st.success("API Key Loaded!")
    else:
        st.warning("Please add GEMINI_API_KEY to Streamlit Secrets.")

# --- CORE LOGIC ---
def analyze_image(img, lang):
    if not api_key.strip():
        st.error("Please provide a valid API Key!")
        return None, None
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Prompt generalized for all images/documents as requested
    prompt = f"""
    Act as a professional technical analyst. 
    Provide a comprehensive analysis of this image/document in {lang}.
    If it contains objects: Identify them and provide technical specs.
    If it is a document: Perform OCR and summarize key insights.
    Ensure the output is informative and innovative.
    Format with clean markdown bolding.
    """
    
    with st.spinner(f"AI is analyzing in {lang}..."):
        try:
            response = model.generate_content([prompt, img])
            raw_text = response.text 

            # REGEX SANITIZATION LAYER: Strips markdown noise for clean audio
            clean_text_for_voice = re.sub(r'[\*\#\_]', '', raw_text)
            
            # Create Audio
            lang_codes = {"English": "en", "Hindi": "hi", "Marathi": "mr"}
            tts = gTTS(text=clean_text_for_voice, lang=lang_codes[lang])
            
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            
            return raw_text, audio_fp
        except Exception as e:
            st.error(f"Analysis failed: {e}")
            return None, None
    
# --- MAIN UI ---
st.title("🎙️ VisionVoice AI")
st.markdown("<p style='color: #8B949E; margin-bottom: 25px;'>Focused Technical Prototype: Visual Reasoning to Neural Speech Pipeline</p>", unsafe_allow_html=True)

# Layout container
with st.container():
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("### 📤 Input Source")
        uploaded_file = st.file_uploader("Drop your image or document here", type=["jpg", "jpeg", "png"])
        selected_lang = st.selectbox("Narrator Language", ["English", "Hindi", "Marathi"])
        
        if uploaded_file:
            image = PIL.Image.open(uploaded_file)
            st.image(image, caption="Uploaded Content", use_container_width=True)
            
            if st.button("🚀 ANALYZE & NARRATE"):
                text, audio = analyze_image(image, selected_lang)
                if text:
                    st.session_state['text'] = text
                    st.session_state['audio'] = audio

    with col2:
        st.markdown("### 📋 AI Insights")
        if 'text' in st.session_state:
            # Display result in the Glassmorphism card
            st.markdown(f"""
                <div class='res-card'>
                    {st.session_state['text']}
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🔊 Voice Summary")
            st.audio(st.session_state['audio'], format="audio/mp3")
        else:
            st.info("Awaiting input for multimodal processing...")
