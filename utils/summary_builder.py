async def build_summary(results):
    # Create lists for each similarity group
    low_similarity = []
    medium_similarity = []
    high_similarity = []
    # Loop through each result and categorize based on similarity
    for result in results:
        similarity = result['similarity']
        file_name = result['file_name']

        # Group files based on similarity
        if similarity < 0.5:
            low_similarity.append(f"{file_name}")
        elif 0.5 <= similarity <= 0.8:
            medium_similarity.append(f"{file_name}")
        else:
            high_similarity.append(f"{file_name}")
    # Create a markdown table with three columns for each similarity group
    table_content = "| Low Similarity (< 0.5) | Medium Similarity (0.5 - 0.8) | High Similarity (> 0.8) |\n"
    table_content += "|-------------------------|-------------------------------|------------------------|\n"
    # Find the max number of rows among the groups to align the table
    max_rows = max(len(low_similarity), len(medium_similarity), len(high_similarity))
    # Pad the lists with empty strings so they have equal lengths
    low_similarity += [" "] * (max_rows - len(low_similarity))
    medium_similarity += [" "] * (max_rows - len(medium_similarity))
    high_similarity += [" "] * (max_rows - len(high_similarity))
    # Construct the table rows
    for i in range(max_rows):
        table_content += f"| {low_similarity[i]} | {medium_similarity[i]} | {high_similarity[i]} |\n"
    return table_content