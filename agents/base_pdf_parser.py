import re
from abc import ABC, abstractmethod
import cv2
import gc

# Abstract base class for common functionality
class BasePDFParser(ABC):
    def preprocess_image(self, image_path):
        """
        Preprocess the image to improve OCR performance:
        - Convert to grayscale
        - Denoise the image
        - Apply thresholding
        - Optionally resize the image
        """
        image = cv2.imread(image_path)

        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Denoise the image
        denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)

        # Enhance contrast before thresholding
        contrast_enhanced = cv2.convertScaleAbs(denoised, alpha=1.1, beta=0)  # Increase contrast

        # Softer thresholding using adaptive thresholding with careful tuning
        # Use adaptive thresholding instead of Otsu
        # TODO see if required
        #thresholded = cv2.adaptiveThreshold(contrast_enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

        # Dilate to strengthen text regions with less aggressive kernel
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        dilated = cv2.dilate(contrast_enhanced, kernel, iterations=1)

        # Optionally resize the image (if it's too small, resize it to improve text recognition)
        resized = cv2.resize(dilated, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        # Save the processed image
        preprocessed_image_path = image_path.replace('.png', f'_processed.png')
        cv2.imwrite(preprocessed_image_path, resized)

        # Clean up to avoid memory retention
        del image, gray, denoised,  dilated, resized
        gc.collect()  # Invoke garbage collector

        return preprocessed_image_path  # Return the path of the processed image

    def postprocess_text(self, text):
        """
        Postprocess the extracted text to clean it up:
        - Remove unwanted characters
        - Apply regex for cleaning
        """
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s.,]', '', text)
        return cleaned_text

    @abstractmethod
    def parse_invoice(self, pdf_content, file_name):
        """
        Abstract method for parsing invoices.
        Each specific parser should implement this method according to its OCR process.
        """
        pass