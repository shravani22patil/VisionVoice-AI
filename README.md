# 🎙️ VisionVoice AI: Multimodal Product & Receipt Explorer

**VisionVoice AI** is a high-performance multimodal application that bridges the gap between Computer Vision and Audio Synthesis. Built for the 2026 AI ecosystem, it leverages **Gemini 1.5 Flash** and **gTTS** to provide real-time, multilingual technical analysis of gadgets and financial receipts, delivered through a sophisticated "Dark-Glass" interactive interface.

---

## 🚀 Key Features

* **Multimodal Intelligence**: Processes high-resolution image inputs to generate structured text and high-fidelity audio summaries simultaneously.
* **Specialized Domain Logic**: Features custom-tuned prompts for identifying gadgets (features/maintenance) vs. receipts (merchants/totals/itemization).
* **Multilingual Narration**: Supports real-time synthesis in **English**, **Hindi**, and **Marathi** to enhance accessibility.
* **Audio Sanitization Pipeline**: Uses a custom **Regex-based preprocessing layer** to strip Markdown symbols (asterisks, hashes) for a natural, human-like voice experience.
* **Modern Dark-Glass UI**: A custom-CSS dashboard featuring **Glassmorphism**, interactive hover animations, and responsive layouts designed for eye comfort.

---

## 🛠️ Tech Stack

* **LLM Core**: Gemini 1.5 Flash (Google Generative AI SDK) 
* **Interface**: Streamlit (with Custom CSS/HTML Injection) 
* **Speech Engine**: gTTS (Google Text-to-Speech)
* **Processing**: Python 3.9+, PIL (Pillow), Regex 

---

## 📐 System Architecture



1.  **Ingestion**: Captures image data via a streamlined Streamlit uploader.
2.  **Cognition**: Dispatches image and system instructions to **Gemini 1.5 Flash** for low-latency reasoning.
3.  **Refinement**: Sanitizes raw LLM text using regular expressions to prevent the audio engine from reading formatting characters.
4.  **Synthesis**: Converts the cleaned string into an `.mp3` stream using specialized language codes.
5.  **Rendering**: Displays parallel outputs—Markdown text for visual review and an interactive audio player for narrated summaries.

---

## 🏁 Getting Started

### Prerequisites
* Python 3.9+
* A valid **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/)

### Installation
1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/yourusername/vision-voice-ai.git](https://github.com/yourusername/vision-voice-ai.git)
    cd vision-voice-ai
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the application**:
    ```bash
    streamlit run app.py
    ```

---

## 📈 Engineering Highlights

* **Latency Optimization**: Switched to the `flash` model variant to achieve sub-2-second inference times suitable for production-grade prototypes.
* **UI persistence**: Leveraged `st.session_state` to maintain analysis results across UI interactions, reducing redundant API costs.
* **Security**: Designed with secure API handling to ensure sensitive credentials remain outside of version control.

---

## 📜 License
Distributed under the MIT License.
