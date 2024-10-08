def comparison_prompt(file_name, ocr1_result, ocr2_result, similarity_12):
    prompt = (
        f"You have to compare two pdf extractions done on the same pdf invoice file by python OCR libs easyOcr,PaddleOcr"
        f"here is the first extraction:\n\n{ocr1_result}\n\n, "
        f"here is the second extraction:\n\n{ocr2_result}\n\n"
        # f"and the third and last one:\n\n{ocr3_result}\n\n"
        f"IMPORTANT : "
        f"If the document extracted is not an invoice you don't have to perform the comparison and you can inform the user that the document provided is not an invoice"
        f"The comparison should be done globally on the two text extractions and always presented under the form of a table."
        f"For each file you will start with a title 'Comparative analysis of the extraction of {file_name}' then "
        f"you will compare and summarize for the user the various informations we can expect in a classical invoice like:"
        f"- Emitter of the invoice with name, address and contact"
        f"- Receiver of the invoice with name, address and contact"
        f"- Invoice Number"
        f"- Order Number"
        f"- Due Date"
        f"- Total amount"
        f"- Taxes amount"
        f"- Payment delay information"
        f"Do not add additional text or comment with this part of the answer."
        f"After a carriage return and with the title 'Similarity' you will display the"
        # f"table or matrix the computed similarities: \n"
        f"similarity between easyOcr extraction and PaddleOcr extraction: {similarity_12: .2f}\n"
        # f"Similarity between easyOcr extraction and TesserAct extraction: {similarity_13: .2f}\n"
        # f"Similarity between PaddleOcr extraction and TesserAct extraction: {similarity_23: .2f}\n\n"
    )
    return prompt
