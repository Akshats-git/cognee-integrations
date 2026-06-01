import asyncio
import os

import cognee
from cognee_integration_strands import get_sessionized_cognee_tools
from dotenv import load_dotenv
from strands import Agent
from strands.models.openai import OpenAIModel

load_dotenv()


async def main():
    from cognee.api.v1.config import config

    config.data_root_directory(os.path.join(os.path.dirname(__file__), "../.cognee/data_storage"))

    config.system_root_directory(os.path.join(os.path.dirname(__file__), "../.cognee/system"))

    from cognee_integration_strands.tools import run_cognee_task

    async def setup_cognee():
        await cognee.prune.prune_data()
        await cognee.prune.prune_system(metadata=True)

        # """
        #     # Step 1. open file and read the content + add to cognee
        # """
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        for filename in os.listdir(data_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(data_dir, filename)
                with open(file_path, "r") as f:
                    content = f.read()
                    await cognee.add(content)
        await cognee.cognify()

    run_cognee_task(setup_cognee(), timeout=600)

    add_tool, search_tool = get_sessionized_cognee_tools("daulet-test-user")

    # Create an agent with memory capabilities using OpenAI
    model = OpenAIModel(
        client_args={"api_key": os.getenv("LLM_API_KEY")},
        model_id="gpt-4o",
    )
    agent = Agent(model=model, tools=[add_tool, search_tool])

    agent(
        'We have signed a contract with the following company: "Meditech Solutions". '
        "Company is in the healthcare industry. Start date is Jan 2023 and "
        "end date is Dec 2025. Contract value is £1.2M."
    )

    agent(
        'We have signed a contract with the following company: "QuantumSoft". '
        "Company is in the technology industry. Start date is Aug 2024 and "
        "end date is Aug 2028. Contract value is £5.5M."
    )

    agent(
        'We have signed a contract with the following company: "Orion Retail Group". '
        "Company is in the retail industry. Start date is Mar 2024 and "
        "end date is Mar 2026. Contract value is £850K."
    )
    """
        Do a research on the following topic: "What contracts are in the healthcare industy?"
    """
    # Create a fresh agent instance to avoid memory interference
    fresh_model = OpenAIModel(
        client_args={"api_key": os.getenv("LLM_API_KEY")},
        model_id="gpt-4o",
    )
    fresh_agent = Agent(
        model=fresh_model,
        tools=[
            add_tool,
            search_tool,
        ],
    )

    fresh_agent(
        "I need to research our contract portfolio. Can you search for any contracts we have "
        "with companies in the healthcare industry? Please use the search functionality to "
        "find this information."
    )


if __name__ == "__main__":
    asyncio.run(main())
