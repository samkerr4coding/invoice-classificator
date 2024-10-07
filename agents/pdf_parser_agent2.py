import gc
import logging
import threading
from abc import ABC

import pytesseract
from PIL import Image
from pdf2image import convert_from_path

from agents.base_pdf_parser import BasePDFParser


class PDFParserAgent2(BasePDFParser):
    def parse_invoice(self, pdf_content, file_name, chunk_size=5):
        text_extracted = ""

        # Convert PDF to images in chunks to save memory
        total_pages = convert_from_path(pdf_content, dpi=150)
        num_pages = len(total_pages)

        # Process the PDF in chunks
        for start in range(0, num_pages, chunk_size):
            end = min(start + chunk_size, num_pages)
            # print(f"Processing pages {start + 1} to {end}...")

            for i, page in enumerate(total_pages[start:end], start=start):
                page_file_name = f'{file_name}_tesseract_page_{i}.png'
                image_path = f'./data/processed/{page_file_name}'
                page.save(image_path, 'PNG')  # Save the page image

                # Preprocess the image for better OCR results
                preprocessed_image_path = self.preprocess_image(image_path)

                # Load the preprocessed image for OCR
                preprocessed_image = Image.open(preprocessed_image_path)

                # Perform OCR using pytesseract with custom configuration
                custom_config = r'--oem 3 --psm 6 -l eng+fra+ita+esp'
                text = pytesseract.image_to_string(preprocessed_image, config=custom_config)

                # Postprocess the extracted text
                clean_text = self.postprocess_text(text)

                # Append extracted and post-processed text
                text_extracted += clean_text
                # logging.info(f"File {file_name} Page {i}: Detected text:\n{clean_text}")

                # Clean up image objects to free memory
                preprocessed_image.close()
                del preprocessed_image, page
                gc.collect()  # Force garbage collection

            logging.info(f"Finished processing chunk of pages {start + 1} to {end}.")

        return text_extracted


def run(state):
    try:
        task_thread_id = threading.get_ident()
        logging.info(f"Starting parser 2 task on file {state['file_name']}, Thread ID: {task_thread_id}")
        agent = PDFParserAgent2()
        # Run the agent to parse the invoice
        result = agent.parse_invoice(state['file_path'], state['file_name'])
        logging.info(f"Finished parser 2 task on file {state['file_name']}, Thread ID: {task_thread_id}")
    finally:
        # Cleanup after task completion
        del agent
        gc.collect()
        # Trigger garbage collection to free memory
    return {"ocr2_result": result}
