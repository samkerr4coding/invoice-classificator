from langgraph.constants import START, END
from langgraph.graph import StateGraph

from agents import pdf_parser_agent1, pdf_parser_agent2, comparison_agent, classification_agent
from state.graph_state import GraphState


def create_graph():
    global graph
    workflow = StateGraph(state_schema=GraphState)
    workflow.add_node("entry_point", lambda x: x)
    workflow.add_edge(START, "entry_point")
    workflow.add_node("parse_pdf1", pdf_parser_agent1.run)
    #workflow.add_node("parse_pdf2", pdf_parser_agent2.run)
    #workflow.add_node("compare_results", comparison_agent.run)
    #workflow.add_node("classify_results", classification_agent.run)
    workflow.add_edge("entry_point", "parse_pdf1")
    #workflow.add_edge("entry_point", "parse_pdf2")
    #workflow.add_edge(["parse_pdf1", "parse_pdf2"], "compare_results")
    #workflow.add_edge("parse_pdf1", "compare_results")
    #workflow.add_edge("compare_results", "classify_results")
    workflow.add_edge("parse_pdf1", END)
    graph = workflow.compile()
    return graph
