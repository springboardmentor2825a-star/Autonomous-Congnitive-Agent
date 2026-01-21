project:
  name: Autonomous Cognitive Engine
  domain: GenAI / Autonomous Agents
  purpose: >
    An autonomous cognitive engine for deep research and long-horizon
    task execution, designed to simulate how modern AI agents operate
    in enterprise and research environments.

problem_statement:
  description: >
    Build an autonomous cognitive engine that can understand high-level
    goals, decompose them into sub-tasks, execute steps autonomously using
    tools, maintain memory, evaluate its own outputs, and escalate to
    humans when confidence is low.

system_architecture:
  execution_flow:
    - user_goal
    - planner_agent
    - executor_agent:
        uses:
          - external_tools
          - fallback_knowledge
    - vector_memory_rag
    - reflection_agent
    - evaluation_gate:
        outcomes:
          - human_escalation
          - synthesis_agent
    - final_output

core_capabilities:
  planning: autonomous_task_decomposition
  execution: multi_step_autonomous_execution
  tools: web_search_with_fallback
  memory: vector_based_memory_rag
  reasoning: reflection_and_self_evaluation
  safety: human_in_the_loop_escalation
  interface: streamlit_ui

agents:
  planner_agent:
    role: >
      Breaks high-level goals into structured research-oriented sub-tasks.

  executor_agent:
    role: >
      Executes planned tasks using external tools and deterministic fallback
      strategies when tools fail or return insufficient data.

  reflection_agent:
    role: >
      Evaluates evidence sufficiency and diversity to assess confidence.

  evaluator_agent:
    role: >
      Decides whether the system should proceed to synthesis or escalate
      to a human.

  synthesis_agent:
    role: >
      Produces a grounded executive-style summary based on stored memory.

memory_system:
  type: vector_memory
  purpose: >
    Store and retrieve evidence using embeddings to enable grounded
    reasoning and reduce hallucinations.
  visibility: exposed_to_user_via_ui

safety_and_guardrails:
  controls:
    - bounded_execution_steps
    - reflection_based_quality_checks
    - tool_failure_handling
    - explicit_human_escalation

cost_awareness:
  strategies:
    - limited_execution_steps
    - controlled_tool_invocation
    - no_unbounded_llm_loops

execution_interfaces:
  cli:
    command: python src/main.py
  ui:
    framework: streamlit
    command: streamlit run app_streamlit.py
    capabilities:
      - dynamic_goal_input
      - execution_status_display
      - executive_summary_view
      - memory_inspection
      - escalation_visibility

deployment_notes:
  local_execution: supported
  streamlit_cloud: compatible
  service_ready: true

post_deployment_steps:
  - run_multiple_goals_across_domains
  - inspect_memory_for_grounding
  - observe_escalation_behavior
  - document_confidence_failures
  - identify_human_intervention_points
