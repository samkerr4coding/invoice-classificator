def classification_prompt(working_directory, file_path, report_path, similarity):
    prompt = (
        f"Here are the instructions for organizing the files based on their similarity scores:\n\n"
        f"1. There is an original PDF file located at: '{file_path}'.\n"
        f"2. A report file has been generated and is available at: '{report_path}'.\n\n"
        f"Now, follow these rules based on the average similarity score ({similarity}):\n"
        f"- If the average similarity is less than 0.5, move the files to the folder: "
        f"'{working_directory}/data/output/low_similarity'.\n"
        f"- If the average similarity is between 0.5 and 0.8, move the files to the folder: "
        f"'{working_directory}/data/output/medium_similarity'.\n"
        f"- If the average similarity is greater than 0.8, move the files to the folder: "
        f"'{working_directory}/data/output/high_similarity'.\n\n"
        f"Make sure to copy  the original PDF and to cut and paste the report file to the correct folder based on this logic."
    )

    return prompt