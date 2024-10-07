import gc
import logging
import os
import threading

from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from sklearn.metrics.pairwise import cosine_similarity

from prompts.comparison_prompt import comparison_prompt


class ComparisonAgent:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        # Initialize Sentence Transformer model for embeddings
        self.embedding_model = SentenceTransformerEmbeddings(model_name=model_name)
        # Initialize LLM (local or Azure-based)
        self.llm = AzureChatOpenAI(
            azure_deployment=os.environ.get('AZURE_OPENAI_DEPLOYEMENT_NAME'),
            api_version=os.environ.get('AZURE_OPENAI_API_VERSION'),
            name="llm"
        )

    def compute_embedding(self, text):
        """
        Compute the embedding of a given text using the Sentence Transformer model.
        """
        return self.embedding_model.embed_documents([text])

    def calculate_similarity(slf, embedding1, embedding2):
        """
                Combined similarity calculation
                - cosine similarity with embeddings for semantic comparison.
        """
        # Cosine similarity on embeddings (semantic)
        cos_sim = cosine_similarity(embedding1, embedding2)[0][0]

        return cos_sim

    def compare_results(self, file_name, ocr1_result, ocr2_result):
        """
        Compare OCR results textually and via cosine similarity.
        """
        # Compute embeddings for each agent's OCR result
        embedding1 = self.compute_embedding(ocr1_result)
        embedding2 = self.compute_embedding(ocr2_result)

        # Calculate cosine similarities between embeddings
        similarity_12 = self.calculate_similarity(embedding1, embedding2)

        # Prepare a prompt with cosine similarities for LLM
        prompt = comparison_prompt(file_name, ocr1_result, ocr2_result, similarity_12)

        # Send the prompt to the LLM for detailed comparison
        response = self.llm([HumanMessage(content=prompt)])

        return {
            "content": response.content,
            "similarity": similarity_12,
            "file_name": file_name
        }


def run(state):
    try:
        # Create the agent instance
        task_thread_id = threading.get_ident()
        logging.info(f"Starting comparison task on file {state['file_name']}, Thread ID: {task_thread_id}")
        agent = ComparisonAgent()

        # Perform the comparison
        comparison = agent.compare_results(
            state['file_name'],
            state['ocr1_result'],
            state['ocr2_result']
        )
        logging.info(f"Finished comparison task on file {state['file_name']}, Thread ID: {task_thread_id}")
    finally:
        # Ensure agent is deleted and garbage collection is triggered
        del agent
        gc.collect()

    # Return the comparison result
    return {"result": comparison['content'], "similarity": comparison['similarity']}
