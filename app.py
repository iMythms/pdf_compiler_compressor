from pdf2image import convert_from_path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import streamlit as st
import tempfile
from PyPDF2 import PdfMerger
import os


def compress_pdf(input_path, output_path, level="medium"):
    images = convert_from_path(
        input_path, dpi=100 if level == "Low Quality" else 150 if level == "Medium Quality" else 200)
    c = canvas.Canvas(output_path, pagesize=letter)

    for img in images:
        img_io = ImageReader(img)
        c.drawImage(img_io, 0, 0, width=letter[0], height=letter[1])
        c.showPage()

    c.save()


st.set_page_config(page_title="ONE PDF Wizard", layout="centered")
st.title("ONE PDF Wizard")

uploaded_files = st.file_uploader(
    "Upload PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.info("Files ready. Click below to compile and compress.")
    compression_level = st.radio(
        "Select compression level:",
        ["Low Quality", "Medium Quality", "High Quality"],
        index=1,
        horizontal=True
    )

if st.button("Compile"):
    if not uploaded_files:
        st.warning("Please upload at least one PDF.")
    else:
        with st.spinner("Merging PDFs..."):
            merger = PdfMerger()
            temp_dir = tempfile.mkdtemp()

            merged_path = os.path.join(temp_dir, "merged.pdf")
            final_output_path = os.path.join(temp_dir, "final_output.pdf")

            # Merge PDFs
            for file in uploaded_files:
                merger.append(file)
            merger.write(merged_path)
            merger.close()

        with st.spinner("Compressing PDF..."):
            compress_pdf(merged_path, final_output_path,
                         level=compression_level)

        with open(final_output_path, "rb") as f:
            st.success("Done! Download your optimized PDF below.")
            st.download_button("Download Reduced PDF", f,
                               file_name="output_reduced.pdf")
