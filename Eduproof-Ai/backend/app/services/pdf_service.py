from pypdf import PdfReader


def extract_pdf_text(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text


def extract_pdf_image_count(file_path):
    reader = PdfReader(file_path)
    image_count = 0

    for page in reader.pages:
        page_images = getattr(page, "images", None)
        if page_images:
            image_count += len(page_images)

    return image_count