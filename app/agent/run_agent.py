#i created this shit
# app/agent/run_agent.py
import asyncio
from app.agent.manus import Manus
from app.logger import logger

async def run_openmanus_with_prompt(prompt: str) -> str:
    agent = Manus()
    logger.warning("Processing your request...")
    await agent.run(prompt)
    return f"Finished running prompt: {prompt}"
