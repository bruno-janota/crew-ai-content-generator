import os
import argparse
from pydantic import BaseModel, Field
from typing import List
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool
from helpers import load_env, load_yaml_config, display_social_content, save_content
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", force=True)

# Load environment variables
load_env()

# PyDantic Structured Output Definition
class SocialMediaPost(BaseModel):
    platform: str = Field(..., description="The social media platform (e.g., LinkedIn, Twitter).")
    content: str = Field(..., description="The content of the social media post, including key takeaways, hashtags, and mentions.")

class ContentOutput(BaseModel):
    title: str = Field(..., description="The title of the AI-generated content.")
    summary: str = Field(..., description="A concise summary of the main article.")
    article: str = Field(..., description="The full blog post formatted in markdown.")
    key_takeaways: List[str] = Field(..., description="A list of key takeaways from the content.")
    references: List[str] = Field(..., description="List of sources, research papers, or URLs referenced in the article.")
    social_media_posts: List[SocialMediaPost] = Field(..., description="Platform-specific social media posts for content promotion.")


def create_agents(agents_config, llm_model):
    """Initialize AI Agents with roles and assigned tools."""
    return {
        "ai_trend_research": Agent(
            config=agents_config['ai_trend_research_agent'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            llm=llm_model,
        ),
        "technical_content_strategist": Agent(
            config=agents_config['technical_content_strategist_agent'],
            tools=[],
            llm=llm_model,
        ),
        "ai_writer": Agent(
            config=agents_config['ai_writer_agent'],
            tools=[SerperDevTool(), WebsiteSearchTool()],
            llm=llm_model,
        ),
        "content_optimization": Agent(
            config=agents_config['content_optimization_agent'],
            tools=[],
            llm=llm_model,
        ),
        "quality_assurance": Agent(
            config=agents_config['quality_assurance_agent'],
        ),
    }


def create_tasks(tasks_config, agents):
    """Define content creation tasks and their dependencies."""
    monitor_ai_trends_task = Task(
        config=tasks_config['monitor_ai_trends'],
        agent=agents["ai_trend_research"],
    )

    analyze_ai_research_task = Task(
        config=tasks_config['analyze_ai_research'],
        agent=agents["ai_trend_research"],
    )

    create_ai_content_task = Task(
        config=tasks_config['create_ai_content'],
        agent=agents["ai_writer"],
        context=[monitor_ai_trends_task, analyze_ai_research_task],
    )

    content_optimization_task = Task(
        config=tasks_config['content_optimization'],
        agent=agents["content_optimization"],
        context=[create_ai_content_task],
    )

    quality_assurance_task = Task(
        config=tasks_config['quality_assurance'],
        agent=agents["quality_assurance"],
        output_pydantic=ContentOutput,
        context=[content_optimization_task],
    )

    return [
        monitor_ai_trends_task,
        analyze_ai_research_task,
        create_ai_content_task,
        content_optimization_task,
        quality_assurance_task,
    ]


def run_crew(subject, agents_config, tasks_config, llm_model):
    """Instantiate and run the AI content creation crew."""
    logging.info(f"🚀 Running AI Content Creation Crew for topic: {subject}")

    agents = create_agents(agents_config, llm_model)
    tasks = create_tasks(tasks_config, agents)

    content_creation_crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        verbose=True,
    )

    result = content_creation_crew.kickoff(inputs={'subject': subject})

    # Capture usage metrics
    usage_metrics = content_creation_crew.usage_metrics

    # Model pricing (adjust if needed)
    pricing_per_1k_tokens = {
        'gpt-4o-mini': {'input': 0.005, 'output': 0.015}
    }

    model_pricing = pricing_per_1k_tokens.get(llm_model)
    if not model_pricing:
        raise ValueError(f"Pricing info not found for model: {llm_model}")

    # Calculate total cost
    input_tokens = usage_metrics.prompt_tokens + usage_metrics.cached_prompt_tokens
    output_tokens = usage_metrics.completion_tokens

    input_cost = (input_tokens / 1000) * model_pricing['input']
    output_cost = (output_tokens / 1000) * model_pricing['output']
    total_cost = input_cost + output_cost

    logging.info(f"✅ Content Generation Completed!")
    logging.info(f"💰 Total Cost for running crew: ${total_cost:.4f}")

    return result.pydantic


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run AI-powered content generation with crewAI.")
    parser.add_argument(
        "--subject",
        type=str,
        required=True,
        help="The subject/topic for AI-generated content."
    )

    args = parser.parse_args()
    subject = args.subject

    # Set OpenAI LLM model
    llm_model = 'gpt-4o-mini'

    # Load YAML configurations
    CONFIG_DIR = "config/"
    agents_config = load_yaml_config(os.path.join(CONFIG_DIR, "agents.yaml"))
    tasks_config = load_yaml_config(os.path.join(CONFIG_DIR, "tasks.yaml"))

    # Run AI content generation crew
    result = run_crew(subject, agents_config, tasks_config, llm_model)
    display_social_content(result)
    save_content(result, subject)

    logging.info("🎉 AI Content Generation Pipeline Completed!")
