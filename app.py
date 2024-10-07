import asyncio
import logging
import os
import threading
import time
import uuid

import chainlit as cl
import fitz
from dotenv import load_dotenv

from graph.graph import create_graph
from utils.folder_cleaner import FolderCleaner
from utils.summary_builder import build_summary

load_dotenv()

# Define the input folder where files will be uploaded
input_folder = "./data/input"
folder_to_clean = "./data/processed"

# Semaphore to limit concurrency to 2
concurrency_limit = 1
semaphore = asyncio.Semaphore(concurrency_limit)

graph = create_graph()


@cl.on_chat_start
async def start():
    actions = [cl.Action(name="process_files", value="process_files", description="Ocr me i'm famous!!!")]
    await cl.Message(
        content="Please deposit your invoice PDFs in the './data/input/' folder and click the button below to process them. "
                "Then Click 'Process Files' to start processing files from the input folder.",
        actions=actions
    ).send()


@cl.action_callback("process_files")
async def handle_action(action: cl.Action):
    try:
        if action.name == "process_files":

            if not os.path.exists(input_folder):
                await cl.Message(
                    content="Input folder does not exist. Please create './data/input/' and add some files.").send()
                return

            files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

            if files:
                cleaner = FolderCleaner(folder_to_clean)
                await cleaner.clean()

                start_time = time.time()  # Start the timer
                results = []

                for file in files:
                    # Sequentially process each file one by one and await its result
                    results.append(await limited_process_file(os.path.join(input_folder, file), file))

                total_duration = time.time() - start_time  # Calculate total duration
                await cl.Message(content=f"Processed {len(files)} file(s) in {total_duration:.2f} seconds.").send()

                table_content = await build_summary(results)

                del results
                # Send the markdown table as a message
                await cl.Message(content=table_content).send()

                await start()  # Restart the chat interaction
            else:
                await cl.Message(
                    content="No files found in the input folder. Please add some files and try again.").send()
    except Exception as e:
        logging.error(f"Error in handle_action: {e}")
        await cl.Message(content=f"An error occurred: {e}").send()


# Semaphore-wrapped process_file to limit concurrency
async def limited_process_file(file_path: str, file_name: str):
    async with semaphore:
        return await process_file(file_path, file_name)


async def process_file(file_path: str, file_name: str):
    task_thread_id = threading.get_ident()
    logging.info(f"Processing file: {file_name}, Thread ID: {task_thread_id}")

    try:
        config = {"configurable": {"thread_id": uuid.uuid4()}}

        # Run the workflow for each file
        comparison = await cl.make_async(graph.invoke)(
            {"file_path": file_path, "file_name": file_name},
            config=config
        )

        await cl.Message(
            content=f"Comparison completed for {file_name}. Similarity: {comparison['similarity']:.2f}.").send()

        return comparison
    except Exception as e:
        logging.error(f"Error processing file {file_name}: {e}")
        await cl.Message(content=f"Error processing {file_name}: {e}").send()
        return None


if __name__ == "__main__":
    from chainlit.cli import run_chainlit  # Import the Chainlit CLI runner

    run_chainlit(__file__)
