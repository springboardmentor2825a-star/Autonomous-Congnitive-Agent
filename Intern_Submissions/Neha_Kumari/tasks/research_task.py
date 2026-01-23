import textwrap

from crewai import Task
from agents.research_specialist import research_specialist_agent


research_task = Task(
    agent=research_specialist_agent,
    description=textwrap.dedent("""
                Conduct comprehensive research on the topic: {topic}

                Your tasks:
                1. Search for the most current and relevant information
                2. Gather data from multiple reliable sources
                3. Identify key facts, statistics, and expert opinions
                4. Organize findings in a structured format
                5. Ensure information is accurate and up-to-date

                Provide a detailed research summary with:
                - Key findings
                - Important statistics
                - Expert opinions
                - Recent developments
                - Reliable sources used
                """),
    expected_output="A comprehensive research summary with key findings, statistics, expert opinions, recent developments, and sources",
    output_file="research_findings.md"
    )
