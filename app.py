import os

import streamlit as st
from dotenv import load_dotenv
from google import genai


MODEL_NAME = "gemini-2.5-flash"
MAX_INPUT_CHARACTERS = 12000


def load_api_key() -> str | None:
    """Membaca API key Gemini dari file .env atau environment variable."""
    load_dotenv()
    return os.getenv("GEMINI_API_KEY")


def build_prompt(text: str, summary_length: str, output_format: str) -> str:
    """Menyusun prompt ringkasan agar hasilnya rapi dan mudah dibaca."""
    return f"""
Anda adalah asisten belajar yang ahli merangkum teks.

Ringkas teks berikut dengan detail:
- Panjang ringkasan: {summary_length}
- Format output: {output_format}
- Bahasa: Indonesia

Aturan output:
- Pertahankan ide utama dan fakta penting.
- Gunakan bahasa sederhana untuk pemula.
- Jangan menambahkan informasi yang tidak ada di teks.
- Jika ada istilah penting, jelaskan secara singkat.

Teks yang diringkas:
{text}
"""


def summarize_text(api_key: str, prompt: str) -> str:
    """Mengirim prompt ke Gemini dan mengembalikan ringkasan."""
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    return response.text or ""


def main() -> None:
    st.set_page_config(
        page_title="AI Text Summarizer",
        page_icon="AI",
        layout="centered",
    )

    st.title("AI Text Summarizer")
    st.caption("Ringkas artikel, catatan, atau materi panjang dengan Google Gemini.")

    api_key = load_api_key()
    if not api_key:
        st.error("GEMINI_API_KEY belum ditemukan. Buat file .env dari .env.example.")
        st.stop()

    with st.sidebar:
        st.header("Pengaturan")
        summary_length = st.selectbox("Panjang ringkasan", ["Pendek", "Sedang", "Detail"])
        output_format = st.selectbox("Format output", ["Paragraf", "Bullet points", "Poin belajar"])
        st.info("Model: gemini-2.5-flash")

    with st.form("summary_form"):
        text = st.text_area(
            "Teks yang ingin diringkas",
            height=280,
            placeholder="Tempel artikel, materi belajar, atau catatan panjang di sini...",
        )
        submitted = st.form_submit_button("Ringkas Teks")

    if submitted:
        clean_text = text.strip()

        if not clean_text:
            st.warning("Masukkan teks terlebih dahulu.")
            st.stop()

        if len(clean_text) < 80:
            st.warning("Teks terlalu pendek untuk diringkas. Masukkan minimal 80 karakter.")
            st.stop()

        if len(clean_text) > MAX_INPUT_CHARACTERS:
            st.warning(f"Teks terlalu panjang. Maksimal {MAX_INPUT_CHARACTERS} karakter.")
            st.stop()

        prompt = build_prompt(clean_text, summary_length, output_format)

        with st.spinner("Gemini sedang membuat ringkasan..."):
            try:
                result = summarize_text(api_key, prompt)
            except Exception as error:
                st.error(f"Terjadi error saat menghubungi Gemini: {error}")
                st.stop()

        if not result.strip():
            st.warning("Gemini tidak mengembalikan ringkasan. Coba lagi.")
            st.stop()

        st.subheader("Hasil Ringkasan")
        st.markdown(result)


if __name__ == "__main__":
    main()
