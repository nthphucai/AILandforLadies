from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from typing_extensions import TypedDict

from dataclasses import dataclass


@dataclass
class TopicShema:
    Topic1: str = "environmental science/geology"
    Topic2: str = "Depressive Disorders, and Cancer Therapies"
    Topic3: str = "Artificial Intelligence"


TOPIC_LIST = Literal[
    "Explainable AI for Enhanced Clinical Decision Support in Oncology: A Hybrid Approach Combining Deep Learning and Symbolic Reasoning",
    "Pharmacogenomic-Guided Antidepressant Selection in Major Depressive Disorder: A Real-World Observational Study on Treatment Outcomes and Healthcare Utilization",
    "Assessing the Role of Subsurface Hydrology in Landslide Initiation and Slope Stability in Tropical Montane Regions",
    "Federated Learning for Privacy-Preserving Drug Discovery in Precision Medicine: A Collaborative AI Framework",
]


class TopicResponse(BaseModel):
    titles: List[TOPIC_LIST] = Field(
        ..., description="List of given titles relevant to the given topic."
    )

    # reasoning: str = Field(
    #     default="",
    #     description="Reasoning behind the selection of titles relevant to the given topic.",
    # )


class PaperAnalysis(BaseModel):
    """Comprehensive analysis of an academic paper."""

    title: TOPIC_LIST = Field(
        default="", description="Title of the academic paper being analyzed."
    )
    authors: List[str] = Field(
        default_factory=List[str], description="List of authors of the paper."
    )
    summary: str = Field(
        default="", description="A distilled summary of the paper's abstract."
    )
    keywords: List[str] = Field(
        default_factory=List[str],
        description="List of keywords associated with the paper.",
    )


class Paper(BaseModel):
    """Represents an academic paper with its metadata, topics, and citations."""

    link: str = Field(..., description="Link to the paper, typically a URL or DOI.")
    metadata: PaperAnalysis = Field(
        ...,
        description="Detailed analysis of the paper, including metadata, topics, and citations.",
    )


class Topic(BaseModel):
    """Metadata and content for a section within an academic paper."""

    name: Literal[
        f"{TopicShema.Topic1}",
        f"{TopicShema.Topic2}",
        f"{TopicShema.Topic3}",
    ] = Field(..., description="Name of the topic in the paper.")

    papers: List[Paper] = Field(..., description="List of papers.")

    summary: Optional[str] = Field(
        default="",
        description="A concise summary of the key insights extracted from the papers",
    )
    future_trends: Optional[str] = Field(
        None, description="Future trends related to the topic, if available."
    )


class WorkflowState(TypedDict):
    """State of the workflow, including paper analysis and citations."""

    elt_out: List[Paper] = Field(
        ...,
        description="List of paper analyses, each containing metadata, topics, and citations.",
    )
    topic_list: List[Topic] = Field(
        ...,
        description="List of topics in the paper, each containing metadata and content.",
    )
