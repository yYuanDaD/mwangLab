"""Standalone test for the SEA CDM extraction pipeline.

Spins up a mini-agent with only two tools (fetch_geo_description,
extract_sea_cdm_conditions), asks it to scrape a GEO accession's web
description and structure it into SEA CDM JSON. Useful for verifying
that the LLM correctly interprets arbitrary GEO study pages.

Usage:
    python test_seacdm.py                        # defaults to GSE266241
    python test_seacdm.py GSE150316              # one accession
    python test_seacdm.py GSE266241 GSE150316    # multiple, run sequentially
"""

import json
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(_PROJECT_ROOT)
sys.path.insert(0, _PROJECT_ROOT)

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent

from tools.seacdm_tools import extract_sea_cdm_conditions
from tools.geo_tools import fetch_geo_description
from tools.guards import guard_tools


SYSTEM_PROMPT = """
You are a bioinformatics assistant. For a given GEO accession:
1. Call fetch_geo_description to retrieve the study summary and overall design.
2. Call extract_sea_cdm_conditions to structure the information into SEA CDM JSON.
   Populate fields based ONLY on the description text you fetched:
   - study_id: the GEO accession
   - study_objective: a concise summary of the scientific aim
   - experiments: one entry per distinct treatment-vs-control comparison
   - assays: sequencing technology and platform mentioned in the description
3. Report the JSON path. Do NOT call any tool more than necessary.
"""


def run_one(accession: str, agent) -> None:
    print(f"\n{'=' * 60}")
    print(f"  Testing SEA CDM extraction for {accession}")
    print(f"{'=' * 60}")

    query = f"Extract the experimental conditions for GEO study {accession} in SEA CDM format."

    config = {"recursion_limit": 12}
    for chunk in agent.stream({"messages": [("user", query)]}, config=config):
        for node_name, node_state in chunk.items():
            print(f"\n[{node_name.upper()}] -------------------------")
            latest_msg = node_state["messages"][-1]

            if hasattr(latest_msg, "tool_calls") and latest_msg.tool_calls:
                for tc in latest_msg.tool_calls:
                    print(f" Calling: {tc['name']}")
                    args_str = str(tc["args"])
                    print(f" Args: {args_str[:400]}{'...' if len(args_str) > 400 else ''}")

            elif latest_msg.type == "ai" and latest_msg.content:
                print(f" Agent: {latest_msg.content}")

            elif latest_msg.type == "tool":
                print(f" Tool [{latest_msg.name}] finished.")
                preview = str(latest_msg.content)[:400]
                print(f" Result preview: {preview}...\n")

    json_path = f"./output/{accession}_seacdm.json"
    if os.path.exists(json_path):
        print(f"\n{'=' * 60}")
        print(f"  Saved JSON ({json_path}):")
        print(f"{'=' * 60}")
        with open(json_path, encoding="utf-8") as f:
            print(json.dumps(json.load(f), indent=2, ensure_ascii=False))
    else:
        print(f"\nWARN: expected JSON not found at {json_path}")


def main():
    load_dotenv()
    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        raise ValueError("CLAUDE_API_KEY not set in .env")

    accessions = sys.argv[1:] or ["GSE266241"]

    llm = ChatAnthropic(model="claude-sonnet-4-6", api_key=api_key, temperature=0)
    tools = guard_tools(
        [fetch_geo_description, extract_sea_cdm_conditions],
        max_calls_per_tool=2,
    )
    agent = create_agent(model=llm, tools=tools, system_prompt=SYSTEM_PROMPT)

    for acc in accessions:
        run_one(acc, agent)


if __name__ == "__main__":
    main()
