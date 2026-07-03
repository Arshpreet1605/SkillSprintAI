import pdfplumber

def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_resume_text(uploaded_file):
    file_type = uploaded_file.name.split(".")[-1].lower()
    if file_type == "pdf":
        return extract_text_from_pdf(uploaded_file)
    return ""