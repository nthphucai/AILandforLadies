import os
import sys
from pydantic import BaseModel, Field
from typing import List, Literal
from tqdm import tqdm

# Determine the absolute path to the root directory of the project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the project root to the system path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from state import WorkflowState, Paper, TopicResponse
from agents.base_agent import BaseAgent


class Filter(BaseAgent):
    def __init__(self):
        super().__init__(name="FilterAgent")

    def run(self, state: WorkflowState):
        """Run the filtering process on the workflow state."""
        papers = state["elt_out"]
        with tqdm(state["topic_list"]) as pbar:
            for topic in state["topic_list"]:
                pbar.set_description(f"✨ 🔍 Filtering topics >> {topic.name}")
                topic.papers = self.filter_topic(topic.name, papers)

        # #### Normal Behavior  - NOT OOP ####
        # temporary_papers = []
        # for topic in tqdm(state["topic_list"], desc="✨ 🔍 Filtering topics"):
        #     relevant_papers = self.filter_topic(topic.name, papers)
        #     temporary_papers.append({"name": topic.name, "papers": relevant_papers, "summary": topic.summary, "future_trends": topic.future_trends})
        
        # state["topic_list"] = temporary_papers
        # #### Normal Behavior ####

        return state

    def filter_topic(self, topic: str, papers: List[Paper]) -> list:
        """Filter sections based on some criteria."""
        titles = [{"title": paper.metadata.title} for paper in papers]
        content = (
            "This is the topic: {} \nHere are the titles: {}".format(
                topic, str(titles)
            ),
        )
        response = self.parse_response(
            system_prompt=f"List of titles where {topic} is prominently mentioned",
            content=content,
            response_format=TopicResponse,
        )
        print(
            f"\n{'*' * 20}\n"
            f"{len(response.titles)} titles found for topic: {topic}\n"
            f"Titles: {response.titles}\n"
            f"{'*' * 20}"
        )

        relevant_papers = [
            page for page in papers if page.metadata.title in response.titles
        ]
        return relevant_papers


if __name__ == "__main__":
    import pickle

    # Load the state object from a pickle file
    with open("out/ETL.pkl", "rb") as pickle_file:
        state = pickle.load(pickle_file)

    etl = Filter()

    etl.run(state)
    # print("ETL process completed. Extracted data:", state["elt_out"])

    # Save the state object as a pickle file
    with open("out/Filter.pkl", "wb") as pickle_file:
        pickle.dump(state, pickle_file)
