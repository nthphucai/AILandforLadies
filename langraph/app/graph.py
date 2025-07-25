import os
import sys

from langgraph.graph import StateGraph

# Determine the absolute path to the root directory of the project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print(f"Project root directory: {project_root}")

# Add the project root to the system path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from state import WorkflowState
from agents.etl import ETL
from agents.filter import Filter
from agents.consolidate import ConsolidateAnalysis

# Phan loai cac paper analysis tasks
# 1. ETL: Extract, Transform, Load - to parse the paper and extract metadata
# 2. Filter: Filter topics based on relevance summary and section conten
# 3. Consolidate: Combine all analyses and summaries into a comprehensive report and forecast potential trends

elt = ETL()
filter_topic = Filter()
consolidate = ConsolidateAnalysis()


def create_paper_analysis_graph(debug: bool = False) -> StateGraph:
    workflow = StateGraph(WorkflowState)

    # Add nodes to the graph
    workflow.add_node("etl", elt.run)
    workflow.add_node("filter", filter_topic.run)
    workflow.add_node("consolidate", consolidate.run)

    # Define the entry point
    workflow.set_entry_point("etl")  # Start by parsing the paper

    # Define edges (how nodes connect)
    # After parsing, we can extract metadata and citations in parallel
    workflow.add_edge("etl", "filter")
    workflow.add_edge("filter", "consolidate")

    # Define the exit point
    workflow.set_finish_point("consolidate")

    return workflow.compile()


def display_graph(graph, file_name: str = "Langraph_workflow.png"):

    try:
        file_path = os.path.join(project_root, file_name)
        png_graph = graph.get_graph().draw_mermaid_png()
        with open(file_path, "wb") as f:
            f.write(png_graph)

        print(f"Graph saved as '{file_name}' in {project_root}")

    except Exception as e:
        print(f"Error display graph: {e}")
        pass


def write_json_file(data, file_path):
    import json

    """
    Write data to a JSON file.

    Args:
        data (dict or list): The data to write to the JSON file.
        file_path (str): The path to the JSON file.
    """
    try:
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully written to {file_path}")
    except Exception as e:
        print(f"An error occurred while writing to the JSON file: {e}")


if __name__ == "__main__":
    from fastapi.encoders import jsonable_encoder

    # Create the graph
    graph = create_paper_analysis_graph(debug=True)
    print("Workflow created successfully.")

    # Display graph
    # img_graph = graph.get_graph_to_display()
    display_graph(graph=graph, file_name="Langraph_workflow.png")

    # Initial state invoked with user question
    initial_state = WorkflowState(
        elt_out=[],
        topic_list=[],
    )

    # Invoke the graph with the initial state
    result = graph.invoke(initial_state)
    
    write_json_file(jsonable_encoder(result),  file_path="out/WorkflowState.json")
