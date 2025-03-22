# server.py

from fastapi import FastAPI, Request, Header
from typing import Optional
import uvicorn

from app.logger import logger, LogCapture
from app.config import config
from app.agent.run_agent import run_openmanus_with_prompt  # Example agent
from app.llm import LLM, LLMSettings
from app.llm import OpenAIError  # or any other exceptions you might handle

app = FastAPI()

@app.post("/agent")
async def run_agent_endpoint(
    request: Request,
    x_openai_key: Optional[str] = Header(None),
    x_headless: Optional[str] = Header(None),
):
    body = await request.json()
    prompt = body.get("prompt", "")

    # 1) (Optional) override config if needed
    # if x_openai_key:
    #     config.llm["default"].api_key = x_openai_key

    # 2) Start capturing logs
    capture = LogCapture(level="DEBUG")
    capture.start_capture()

    try:
        # 3) Run your agent logic with the prompt
        result = await run_openmanus_with_prompt(prompt)
    finally:
        # 4) Stop capturing logs and store them
        raw_logs = capture.stop_capture()

    # 5) Summarize logs with your LLM
    summarizer = LLM("default")  

    prompt_messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that concisely summarizes logs. "
                "Focus on key steps, errors, or critical information. "
                "Do not return excessive detail."
            ),
        },
        {
            "role": "user",
            "content": f"Please provide a concise summary:\n\n{raw_logs}",
        },
    ]

    try:
        summarized_logs = await summarizer.ask(prompt_messages, stream=False)
    except OpenAIError as e:
        logger.error(f"LLM Summarization Error: {e}")
        summarized_logs = "Failed to summarize logs. Check server logs for details."

    return {
        "result": result,
        "logs_summary": summarized_logs
    }

# ✅ ADD THIS BLOCK TO RUN THE SERVER WHEN CALLED DIRECTLY
if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
