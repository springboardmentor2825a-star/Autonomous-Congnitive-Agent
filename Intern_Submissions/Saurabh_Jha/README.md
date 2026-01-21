project:
  name: Autonomous Cognitive Engine
  domain: GenAI / Autonomous Agents
  purpose: >
    An autonomous cognitive engine for executing deep research and
    long-horizon tasks, simulating how modern AI agents operate in
    enterprise and research environments.

problem_statement:
  description: >
    Build an autonomous cognitive engine that can understand high-level
    goals, decompose them into sub-tasks, execute steps autonomously using
    tools, maintain memory, evaluate outputs, and escalate to humans when
    confidence is low.

system_architecture:
  execution_flow:
    - user_goal
    - planner_agent
    - executor_agent
    - memory_rag
    - reflection_agent
    - evaluation_gate
    - output_or_escalation

core_capabilities:
  - autonomous_task_decomposition
  - multi_step_execution
  - tool_augmented_research
  - vector_memory_rag
  - self_evaluation
  - human_in_the_loop_escalation
  - streamlit_ui

agents:
  planner_agent:
    responsibility: task_decomposition
  executor_agent:
    responsibility: tool_execution
  reflection_agent:
    responsibility: confidence_assessment
  evaluator_agent:
    responsibility: escalation_decision
  synthesis_agent:
    responsibility: final_summary_generation

memory_system:
  type: vector_memory
  usage: evidence_storage_and_retrieval
  visibility: shown_in_ui

safety_and_controls:
  - bounded_execution_steps
  - reflection_based_checks
  - tool_failure_handling
  - explicit_human_escalation

execution_interfaces:
  cli:
    command: python src/main.py
  ui:
    framework: streamlit
    local_command: streamlit run app_streamlit.py
    deployed_url: https://congnitive-agent.streamlit.app/

deployment:
  local: supported
  cloud: streamlit_cloud
  public_access: enabled

post_deployment:
  - test_with_multiple_goals
  - verify_memory_grounding
  - observe_escalation_cases

submission:
  method: github_pull_request
  submission_path: Intern_Submissions/Saurabh_Jha