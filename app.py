import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY tidak ditemukan pada file .env")
    st.stop()

client = genai.Client(api_key=api_key)

st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📝",
    layout="centered"
)

st.title("📝 AI Text Summarizer")
st.write("Ringkas artikel, materi, atau teks panjang menggunakan Google Gemini AI.")

summary_type = st.selectbox(
    "Pilih panjang ringkasan",
    [
        "Pendek",
        "Sedang",
        "Panjang"
    ]
)

text = st.text_area(
    "Masukkan teks",
    height=250,
    placeholder="Tempel artikel atau materi di sini..."
)

if st.button("✨ Ringkas Teks"):

    if text.strip() == "":
        st.warning("Masukkan teks terlebih dahulu.")
    else:

        prompt = f"""
Ringkas teks berikut.

Panjang ringkasan:
{summary_type}

Gunakan bahasa Indonesia yang mudah dipahami.

Teks:

{text}
"""

        with st.spinner("Sedang membuat ringkasan..."):

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                st.subheader("Hasil Ringkasan")

                st.success(response.text)

            except Exception as e:

                st.error(f"Terjadi kesalahan:\n{e}")