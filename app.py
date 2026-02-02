import streamlit as st
import backend
import os
import tempfile
from io import BytesIO

st.set_page_config(page_title="PDF OCR Tool", page_icon="📄", layout="centered")

st.title("📄 PDF OCR & Merge Tool")
st.write("Upload multiple PDFs, reorder them, and convert them to an editable Word Document (OCR included).")

# Initialize session state for files if not exists
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# File Uploader
uploaded_files = st.file_uploader("Select PDFs", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    # We use a list to keep track of ordering. 
    # Streamlit reloads on every interaction, so we just trust the uploader's current state
    # but give the user a way to visualize them.
    
    st.success(f"{len(uploaded_files)} files selected.")
    
    # Simple drag-and-drop reordering is hard in basic Streamlit, 
    # but we can list them. The uploader usually keeps selection order.
    # For a simple version, we stick to the uploaded order.
    st.write("### Files to Process:")
    for i, file in enumerate(uploaded_files):
        st.text(f"{i+1}. {file.name}")

    if st.button("🚀 Merge & Process", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # 1. Merge
            status_text.text("Merging files...")
            merged_pdf = backend.merge_pdfs(uploaded_files)
            progress_bar.progress(20)
            
            # 2. Convert to Images
            status_text.text("Converting PDF pages to images for OCR...")
            images = backend.convert_to_images(merged_pdf)
            progress_bar.progress(40)
            
            # 3. OCR
            status_text.text(f"Running OCR on {len(images)} pages...")
            
            def progress_callback(current, total):
                # Map 40-90%
                val = 40 + int((current / total) * 50)
                progress_bar.progress(val)
                status_text.text(f"OCR Processing Page {current}/{total}...")

            extracted_text = backend.perform_ocr(images, progress_callback=progress_callback)
            progress_bar.progress(90)
            
            # 4. Save
            status_text.text("Generating Word Document...")
            
            # We need to save to a bytes buffer to verify download, 
            # BUT backend.save_to_docx expects a filename.
            # Let's Modify backend slightly or just use a temp file.
            
            with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
                temp_path = tmp.name
                
            backend.save_to_docx(extracted_text, temp_path)
            progress_bar.progress(100)
            status_text.text("✅ Done! Ready to download.")
            
            # Read back for download button
            with open(temp_path, "rb") as f:
                docx_data = f.read()
            
            st.download_button(
                label="📥 Download Word Document",
                data=docx_data,
                file_name="converted_output.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            
            os.remove(temp_path)

        except Exception as e:
            st.error(f"An error occurred: {e}")

else:
    st.info("Please upload PDF files to begin.")
