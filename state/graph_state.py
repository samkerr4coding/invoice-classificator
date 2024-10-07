from typing import TypedDict


class GraphState(TypedDict):
    file_path: str
    file_name: str
    ocr1_result: str
    ocr2_result: str
    similarity: float
    result: str
    report: str