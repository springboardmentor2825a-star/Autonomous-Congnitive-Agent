import textwrap

from crewai import Task
from agents.content_writer import content_writer_agent
from tasks.analysis_task import analysis_task
from tasks.research_task import research_task


writing_task = Task(
    agent=content_writer_agent,
    description=textwrap.dedent("""
                Create a comprehensive report on the topic: {topic}

                Your tasks:
                1. Review both research findings and analysis results
                2. Write a well-structured, comprehensive report
                3. Ensure clarity and readability for the target audience
                4. Include executive summary, main content, and conclusions
                5. Cite all sources appropriately

                The report should include:
                - Executive Summary
                - Introduction
                - Main Findings
                - Analysis and Insights
                - Conclusions and Recommendations
                - Sources and References
                """),
    expected_output="A comprehensive, well-structured report with executive summary and conclusions",
    context=[research_task, analysis_task],
    output_file="final_report.md"
    )
