import logging
import threading

import fitz  # PyMuPDF
from easyocr import easyocr

from agents.base_pdf_parser import BasePDFParser


class PDFParserAgent1(BasePDFParser):
    def __init__(self):
        # Initialize EasyOCR reader once during object creation
        self.reader = easyocr.Reader(['en', 'fr', 'es', 'it'], gpu=True)  # Use GPU if available

    def parse_invoice(self, pdf_content, file_name, chunk_size=5):
        text_extracted = ""

        # Open the PDF file with PyMuPDF
        pdf_document = fitz.open(pdf_content)
        total_pages = len(pdf_document)

        # Process pages in chunks
        for start in range(0, total_pages, chunk_size):
            end = min(start + chunk_size, total_pages)
            print(f"Processing pages {start + 1} to {end}...")

            for i in range(start, end):
                page = pdf_document.load_page(i)  # Load one page at a time
                pix = page.get_pixmap(dpi=150)  # Render page to image
                image_path = f'./data/processed/{file_name}_easyocr_page_{i}.png'
                pix.save(image_path)  # Save the page image

                # Preprocess the image for better OCR results
                preprocessed_image = self.preprocess_image(image_path)

                # Perform OCR on the preprocessed image
                results = self.reader.readtext(preprocessed_image, detail=1, min_size=15, contrast_ths=0.5)

                # Process OCR results
                for result in results:
                    bbox, text, confidence = result
                    if confidence > 0.3:  # Filter low-confidence results
                        cleaned_text = self.postprocess_text(text)
                        text_extracted += cleaned_text + " "
                        # print(f"File {file_name} Page {i}: Detected text: {cleaned_text} with a confidence of {confidence}")
                        # print(f"Bounding box: {bbox}")

                # Clean up memory after processing each page
                del preprocessed_image, results, pix, page

            logging.info(f"Finished processing chunk of pages {start + 1} to {end}.")
            fitz.TOOLS.store_shrink(100)

        pdf_document.close()  # Close the PDF to free resources
        return text_extracted


def run(state):
    try:
        task_thread_id = threading.get_ident()
        logging.info(f"Starting parser 1 task on file {state['file_name']}, Thread ID: {task_thread_id}")
        # Initialize the PDF parser agent
        agent = PDFParserAgent1()
        # Run the agent to parse the invoice
        result = agent.parse_invoice(state['file_path'], state['file_name'])
        logging.info(f"Finished parser 1 task on file {state['file_name']}, Thread ID: {task_thread_id}")
    finally:
        # Cleanup after task completion
        del agent
    return {"ocr1_result": result}
