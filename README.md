# invoice-classificator
Automating pdf Invoice (or any kind of document) Classification with Chainlit, Langraph, Gemini Flash, Tesseract, and EasyOCR

## Summary

This project is a Proof of Concept (PoC) demonstrating the integration of Optical Character Recognition (OCR) and AI for invoice classification. It utilizes `langgraph` workflows to enable users to upload a PDF file, which is processed through a custom workflow, resulting in a comparative analysis from various OCR engines and a final assessment from a Language Model (LLM).

### Workflow Design based on langgraph

The workflow is designed as follows:

![Workflow Design](images/design.png)

1. **Entry Node**: A simple "dumb" node serves as the single point of entry for the workflow.
2. **OCR Nodes**: Multiple OCR nodes are connected to the entry node, each utilizing a different Python OCR library (`EasyOCR`, `PaddleOCR`, or `Tesseract`). These nodes independently process the uploaded PDF file to extract text.
3. **Comparison Node**: A final comparison node waits for the results from all OCR nodes. It then aggregates these results and sends them to an AI-powered LLM instance, which produces a summary and a similarity percentage for each OCR result.

The workflow allows flexibility in LLM configurations, with options for either a remote Azure OpenAI service or a local LLM instance powered by Ollama. In local mode, you can select your desired model for the comparison task.

![Workflow Design](images/design3.png)

### Key Libraries and Tools

This project leverages several open-source libraries and tools:

- **langgraph**: Workflow management and orchestration.
- **langchain**: Integration of language models with a variety of tools and applications.
- **langchain_google_genai**: Access to OpenAI and Azure-based language models.
- **langchain-ollama**: Interface for running local LLMs using Ollama.
- **EasyOCR**: Lightweight OCR library for extracting text from images.
- **Tesseract**: Google's OCR engine.
- **Chainlit**: UI framework for interacting with LLM workflows.
- **pdf2image**: Conversion of PDF pages to images for OCR processing.
- **PyMuPDF**: Conversion of PDF pages to images for OCR processing.

![Libraries](images/libs.png)

## Installation

### .env file

### Google api Key



### Python Requirements

To get started, set up a Python 3.12 virtual environment and install the dependencies using Poetry:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

To run the application:

```angular2html
python app.py
```

Usage

Once the dependencies are installed and the app is running, follow these steps to classify your PDF invoices or documents:

    Upload a PDF Document:
        After launching the app, upload your desired PDF file. The system will automatically process the file using multiple OCR engines.

    View OCR Results:
        The tool extracts text from the document using Tesseract, EasyOCR, and other engines, presenting a comparative analysis.

    Review AI-Powered Assessment:
        The extracted text is passed through an LLM for assessment, where a summary is generated, and the similarity between the OCR results is calculated.

    Download or View Results:
        The final output can be downloaded or reviewed directly within the Chainlit UI.

Configuration

You can configure the tool to use either a remote Azure OpenAI service or run an LLM locally using Ollama:

    Remote LLM:
        Add your Azure OpenAI API key in the environment configuration file:

        bash

    OPENAI_API_KEY=your-openai-api-key

Local LLM (using Ollama):

    To run the LLM locally, ensure that you have installed Ollama, and specify the model you'd like to use:

    bash

        OLLAMA_MODEL="your-local-model"

Contributing

Contributions are welcome! To contribute:

    Fork the repository.
    Create a feature branch (git checkout -b feature/your-feature).
    Commit your changes (git commit -m 'Add your feature').
    Push to the branch (git push origin feature/your-feature).
    Open a Pull Request.

Please make sure to include tests and documentation updates for any new features or fixes.
License

This project is licensed under the MIT License - see the LICENSE file for details
