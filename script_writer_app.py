import streamlit as st
from openai import OpenAI
from fpdf import FPDF
import base64

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Creative Script Generator", layout="centered")

# Custom Styling
st.markdown("""
    <style>
        .main {
            background-color: #0e1117;
            color: #ffffff;
        }
        .stTextInput>div>div>input {
            background-color: #262730;
            color: white;
        }
        .stButton button {
            background-color: #ff4b4b;
            color: white;
            font-weight: bold;
        }
        .stMarkdown {
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 Creative Script Writer")
st.markdown("Enter a topic and customize your script below.")

# User Inputs
topic = st.text_input("🎯 Topic or Idea")
genre = st.selectbox("🎭 Genre", ["Drama", "Comedy", "Sci-Fi", "Romance", "Horror", "Fantasy", "Thriller"])
tone = st.selectbox("🗣️ Tone", ["Inspiring", "Funny", "Serious", "Dark", "Light-hearted"])
length = st.slider("📏 Script Length (Approx. Tokens)", min_value=300, max_value=1000, value=700, step=100)

# Generate
if st.button("📝 Generate Script"):
    with st.spinner("Crafting your screenplay..."):
        prompt = (
            f"Write a short film script with the topic: '{topic}', in the genre of {genre}, "
            f"with a {tone.lower()} tone. Make it around {length} tokens long. "
            f"Include character names, scene formatting, and a creative arc."
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a talented scriptwriter who formats professional short instgaram/tiktok reel scripts, you have all the bases covered, hook, buildup, climax, CTA."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=length
        )

        script = response.choices[0].message.content
        st.markdown("### ✍️ Generated Script")
        st.write(script)

        # PDF Export
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for line in script.split("\n"):
            pdf.multi_cell(0, 10, txt=line)

        pdf_file = "generated_script.pdf"
        pdf.output(pdf_file)

        # Download Link
        with open(pdf_file, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            href = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="{pdf_file}">📥 Download Script as PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
