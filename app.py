import streamlit as st
import tempfile
from PyPDF2 import PdfMerger
import fitz  # PyMuPDF
import os


def compress_pdf(input_path, output_path):
    doc = fitz.open(input_path)
    doc.save(output_path, garbage=4, deflate=True, clean=True)
    doc.close()


st.set_page_config(page_title="ONE PDF Wizard", layout="centered")
st.title("ONE PDF Wizard")

uploaded_files = st.file_uploader(
    "Upload PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.info("Files ready. Click below to compile and compress.")

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
            compress_pdf(merged_path, final_output_path)

        with open(final_output_path, "rb") as f:
            st.success("Done! Download your optimized PDF below.")
            st.download_button("Download Reduced PDF", f,
                               file_name="output_reduced.pdf")
