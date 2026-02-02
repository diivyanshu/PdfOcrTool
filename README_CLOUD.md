# PDF OCR Tool - Cloud Version

This version of the application uses **Tesseract OCR** (Linux-compatible) instead of Apple Vision, making it suitable for deployment on cloud platforms like Render, AWS, Google Cloud, or Azure.

## 🚀 How to Deploy (e.g., on Render.com)

1.  **Push this folder to GitHub**:
    *   Create a new repository.
    *   Upload these files.
2.  **Create a Web Service** on Render:
    *   Connect your GitHub repo.
    *   Select "Docker" as the Runtime (it will automatically find the `Dockerfile`).
    *   Click Deploy.

## 🛠 Running Locally (Mac/Linux/Windows)

To run this version on your computer, you must have **Tesseract** installed.

### Mac (Homebrew)
```bash
brew install tesseract
pip install -r requirements.txt
streamlit run app.py
```

### Windows
1.  Download and install Tesseract for Windows.
2.  Add it to your PATH.
3.  `pip install -r requirements.txt`
4.  `streamlit run app.py`

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install tesseract-ocr
pip install -r requirements.txt
streamlit run app.py
```
