# agent_stocks_tool.py

import requests
import json
from typing import Any, Dict
from app.tool.base import BaseTool, ToolResult
from app.exceptions import ToolError

class StocksTool(BaseTool):
    name: str = "stocks_tool"
    description: str = "Fetch stock details from the new MCP HTTP endpoint."

    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The stocks query or symbol (e.g. 'AAPL')"
            }
        },
        "required": ["query"]
    }

    async def execute(self, query: str, **kwargs) -> ToolResult:
        try:
            resp = requests.post(
                "http://localhost:5600/stocks",
                json={"query": query},
                timeout=300
            )
            resp.raise_for_status()
            data = resp.json()
            raw_result_str = data.get("result", "")
            if not raw_result_str:
                raise ToolError("No 'result' field in response")

            parsed = {}
            try:
                parsed = json.loads(raw_result_str)
            except json.JSONDecodeError:
                pass

            if isinstance(parsed, dict):
                answer = parsed.get("data", {}).get("answer", "")
                if answer:
                    return ToolResult(output=answer)

            return ToolResult(output=raw_result_str)

        except requests.RequestException as e:
            raise ToolError(f"HTTP error calling stocks endpoint: {e}")
        except Exception as e:
            raise ToolError(f"Error parsing stocks data: {e}")
