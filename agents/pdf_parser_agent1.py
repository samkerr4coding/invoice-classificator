import gc
import logging
import threading
import fitz  # PyMuPDF
import pytesseract
import torch
from PIL import Image
from easyocr import easyocr
from transformers import LayoutLMv3Processor, LayoutLMv3ForTokenClassification

from agents.base_pdf_parser import BasePDFParser


class PDFParserAgent1(BasePDFParser):
    def __init__(self, model_name="microsoft/layoutlmv3-base"):
        # Load LayoutLMv3 Processor and Model
        self.processor = LayoutLMv3Processor.from_pretrained(model_name)
        self.model = LayoutLMv3ForTokenClassification.from_pretrained(model_name)

    def convert_pdf_to_images(self, pdf_path):
        """Convert PDF pages to images."""
        pdf_document = fitz.open(pdf_path)
        images = []
        pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            # Save image to disk to visually inspect it
            img.save(f"page_{page_num}.png")
            images.append(img)

        return images

    def extract_text_and_boxes(self, images):
        """Extract text and bounding boxes using OCR."""
        words_data = []

        for image in images:

            ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            words_data.append(ocr_data)

        return words_data

    def prepare_inputs(self, image, words_data):
        """Prepare images, words, and boxes for LayoutLMv3."""
        words = words_data['text']
        boxes = []

        for i in range(len(words_data['text'])):
            x, y, w, h = (words_data['left'][i], words_data['top'][i],
                          words_data['width'][i], words_data['height'][i])
            # Normalize bounding box to 0-1000 scale as LayoutLMv3 uses it
            boxes.append([x, y, x + w, y + h])

        encoded_inputs = self.processor(images=image,
                                        words=words,
                                        boxes=boxes,
                                        return_tensors="pt",
                                        padding="max_length",
                                        truncation=True)

    def parse_invoice(self, pdf_content, file_name, chunk_size=5):
        """Complete process to extract text from a PDF."""
        # Step 1: Convert PDF to images
        images = self.convert_pdf_to_images(pdf_content)

        # Step 2: Extract text and bounding boxes using OCR
        ocr_data = self.extract_text_and_boxes(images)

        extracted_text = []

        # Step 3: Process each page/image with LayoutLMv3
        for i, image in enumerate(images):
            encoded_inputs = self.prepare_inputs(image, ocr_data[i])

            # Forward pass through LayoutLMv3 model
            with torch.no_grad():
                outputs = self.model(**encoded_inputs)

            # Get token predictions
            logits = outputs.logits
            predictions = torch.argmax(logits, dim=2)

            # Convert tokens back to text
            tokens = self.processor.tokenizer.convert_ids_to_tokens(encoded_inputs['input_ids'][0])
            pred_labels = [self.model.config.id2label[label_id.item()] for label_id in predictions[0]]

            # Collect text tokens (if classification-based, change this to extract the label)
            page_text = " ".join([token for token, label in zip(tokens, pred_labels) if label != "O"])
            extracted_text.append(page_text)

        return "\n".join(extracted_text)

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
