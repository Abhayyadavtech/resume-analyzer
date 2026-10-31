import pymupdf


def extract_text_from_pdf(uploaded_file):
    if not uploaded_file.name.lower().endswith(".pdf"):
        raise ValueError("Unsupported file type. Please upload a PDF file.")
    try:
        doc = pymupdf.open(stream=uploaded_file.read(), filetype="pdf")
    except Exception:
        raise ValueError("The PDF could not be opened. The file may be corrupted.")

    text = "".join(page.get_text() for page in doc)
    doc.close()

    if not text.strip():
        raise ValueError(
            "No readable text found in the PDF. "
            "The file may be a scanned or image-only document (OCR is not supported)."
        )
    return text