import asyncio
import os
import webbrowser

import cognee
from cognee_integration_strands import get_sessionized_cognee_tools
from cognee_integration_strands.tools import run_cognee_task
from dotenv import load_dotenv
from strands import Agent
from strands.models.openai import OpenAIModel

load_dotenv()


async def visualize_graph(file_name, open_browser=True):
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    destination_file_path = os.path.join(current_file_dir, file_name)

    # Run visualization in the background task runner for consistency
    run_cognee_task(cognee.visualize_graph(destination_file_path))

    if open_browser:
        url = "file://" + os.path.abspath(destination_file_path)
        webbrowser.open(url)


async def main():
    from cognee.api.v1.config import config

    config.data_root_directory(os.path.join(os.path.dirname(__file__), "../.cognee/data_storage"))

    config.system_root_directory(os.path.join(os.path.dirname(__file__), "../.cognee/system"))

    async def setup_cognee():
        await cognee.prune.prune_data()
        await cognee.prune.prune_system(metadata=True)

    # Run setup in the background task runner
    run_cognee_task(setup_cognee())

    """
        Do a research on the following topic: "What contracts are in the healthcare industy?"
    """

    add_tool, search_tool = get_sessionized_cognee_tools("a-sample-session-id")

    # Configure the model
    model = OpenAIModel(
        client_args={"api_key": os.getenv("LLM_API_KEY")},
        model_id="gpt-4o",
    )

    # A fresh agent instance, unaware of what is in the memory
    agent = Agent(
        model=model,
        tools=[add_tool, search_tool],
    )

    fresh_agent = Agent(
        model=model,
        tools=[add_tool, search_tool],
    )

    # Feed data to the agent
    messages = [
        'We have signed a contract with the following company: "Guardian Insurance Ltd". '
        "Company is in the insurance industry. Start date is Feb 2023 and "
        "end date is Feb 2026. Contract value is £1.8M.",
        'We have signed a contract with the following company: "Pioneer Assurance Group". '
        "Company is in the insurance industry. Start date is Oct 2024 and "
        "end date is Oct 2029. Contract value is £4.2M.",
        'We have signed a contract with the following company: "Finovate Systems". '
        "Company is in the fintech industry. Start date is May 2024 and "
        "end date is May 2027. Contract value is £2.3M.",
    ]

    for msg in messages:
        response = agent(msg)
        print("\n\n")
        print(f"Processed: {msg[:50]}...")

    print("\n=== AGENT RESPONSE (Ingestion) ===")
    print("Data ingestion completed via individual calls.")

    print("\n=== SEARCHING ===")
    response = fresh_agent(
        "I need to research our contract portfolio. Can you search for any contracts we have "
        "with companies in the insurance industry? Please use the search functionality to "
        "find this information."
    )

    print("\n=== AGENT RESPONSE ===")
    print(response)

    await visualize_graph(file_name="session_example.html")


if __name__ == "__main__":
    asyncio.run(main())
