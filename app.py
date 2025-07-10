import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

def tempel_foto(pdf_file, foto_file, x, y, scale):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    img = Image.open(foto_file)

    # Konversi ke PNG dalam memori
    img_io = io.BytesIO()
    img.save(img_io, format="PNG")
    img_io.seek(0)

    img_width, img_height = img.size
    img_width *= scale
    img_height *= scale

    for page in doc:  # Ubah ke `doc[0:1]` jika hanya halaman pertama
        rect = fitz.Rect(x, y, x + img_width, y + img_height)
        page.insert_image(rect, stream=img_io.getvalue())

    # Simpan ke memori
    output_io = io.BytesIO()
    doc.save(output_io)
    doc.close()
    output_io.seek(0)
    return output_io

st.title("📎 Tempel Pasfoto ke PDF")

pdf_file = st.file_uploader("Unggah file PDF", type=["pdf"])
foto_file = st.file_uploader("Unggah pasfoto (JPG/PNG)", type=["jpg", "jpeg", "png"])

x = st.number_input("Posisi X (px)", value=50)
y = st.number_input("Posisi Y (px)", value=50)
scale = st.slider("Skala ukuran pasfoto", 0.1, 2.0, 1.0, 0.1)

if st.button("Tempel Pasfoto") and pdf_file and foto_file:
    output = tempel_foto(pdf_file, foto_file, x, y, scale)
    st.success("✅ Pasfoto berhasil ditempel!")
    st.download_button("📥 Unduh PDF Hasil", data=output, file_name="hasil.pdf", mime="application/pdf")
