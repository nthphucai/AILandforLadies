import os
import sys
from typing import List
from tqdm import tqdm

# Determine the absolute path to the root directory of the project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the project root to the system path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from state import WorkflowState, Paper
from agents.base_agent import BaseAgent


class ConsolidateAnalysis(BaseAgent):
    def __init__(self):
        pass

    def run(self, state: WorkflowState):
        # "Consolidated analysis of the data"
        for topic in tqdm(state["topic_list"], desc="✨ Consolidating analysis:"):   
            topic.summary = self.summarize_topic(topic.papers) # topic["papers"]
            topic.future_trends = self.future_trends(topic.papers)

        return state

    def summarize_topic(self, papers: List[Paper]):
        response = self.create_response(
            system_prompt="A summary of the key insights extracted from the papers",
            content=papers,
        )
        return response

    def future_trends(self, papers: List[Paper]):
        response = self.create_response(
            system_prompt="predict future trends based on the provided papers.",
            content=papers,
        )
        return response


if __name__ == "__main__":
    import pickle

    # Load the state object from a pickle file
    with open("out/Filter.pkl", "rb") as pickle_file:
        state = pickle.load(pickle_file)

    etl = ConsolidateAnalysis()

    etl.run(state)

    # Save the state object as a pickle file
    with open("out/Consolidate.pkl", "wb") as pickle_file:
        pickle.dump(state, pickle_file)
