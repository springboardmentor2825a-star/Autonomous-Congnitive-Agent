import textwrap

from crewai import Task
from agents.data_analyst import data_analyst_agent
from tasks.research_task import research_task


analysis_task = Task(
    agent=data_analyst_agent,
    description=textwrap.dedent("""
                Analyze the research findings for the topic: {topic}

                Your tasks:
                1. Review the research findings from the previous task
                2. Identify patterns, trends, and key insights
                3. Analyze the implications and significance
                4. Provide expert interpretation of the data
                5. Highlight the most important conclusions

                Provide:
                - Key insights and patterns
                - Trend analysis
                - Implications and significance
                - Expert interpretation
                - Actionable conclusions
                """),
    expected_output="A detailed analysis report with insights, patterns, and conclusions",
    context=[research_task],
    output_file="analysis_report.md"
    )
