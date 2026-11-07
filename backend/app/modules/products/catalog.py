PRODUCT_CATALOG = [
    {
        "code": "vertical-llms",
        "name": "Vertical LLMs",
        "family": "AI & Automation",
        "capabilities": ["domain_knowledge", "grounded_responses", "model_governance", "evaluation"],
    },
    {
        "code": "tac-maas",
        "name": "TAC MaaS",
        "family": "AI & Automation",
        "capabilities": ["model_catalog", "model_routing", "lifecycle_visibility", "hybrid_serving"],
    },
    {
        "code": "ai-agent-platform",
        "name": "AI Agent Platform",
        "family": "AI & Automation",
        "capabilities": ["agent_design", "workflow_orchestration", "tool_connections", "observability"],
    },
    {
        "code": "chatbot",
        "name": "Chatbot",
        "family": "AI & Automation",
        "capabilities": ["knowledge_conversations", "guided_journeys", "human_handoff", "multichannel"],
    },
    {
        "code": "chatbi",
        "name": "ChatBI",
        "family": "Data Intelligence",
        "capabilities": ["natural_language_analytics", "governed_metrics", "visual_explanations", "insight_sharing"],
    },
    {
        "code": "aiops-agents",
        "name": "AIOps Agents",
        "family": "AI & Automation",
        "capabilities": ["signal_correlation", "incident_assistance", "response_workflows", "operator_approval"],
    },
    {
        "code": "autoagent",
        "name": "AutoAgent",
        "family": "AI & Automation",
        "capabilities": ["process_orchestration", "application_automation", "exception_handling", "automation_governance"],
    },
    {
        "code": "apexive-corerpa",
        "name": "Apexive CoreRPA",
        "family": "Intelligent Automation",
        "capabilities": ["workflow_design", "bot_orchestration", "license_governance", "execution_monitoring"],
    },
    {
        "code": "turing-dev-suite",
        "name": "TuringDevSuite",
        "family": "AI & Automation",
        "capabilities": ["ai_development_assistance", "delivery_collaboration", "quality_practices", "enterprise_controls"],
    },
    {
        "code": "edge-intelligence",
        "name": "AI² Edge Intelligence",
        "family": "Edge & Operations",
        "capabilities": ["edge_workloads", "local_inference", "device_connectivity", "central_visibility"],
    },
    {
        "code": "ontology-platform",
        "name": "Ontology Platform",
        "family": "Data Intelligence",
        "capabilities": ["business_concept_modeling", "source_mapping", "knowledge_discovery", "semantic_reuse"],
    },
    {
        "code": "dataatlas",
        "name": "DataAtlas",
        "family": "Data Intelligence",
        "capabilities": ["data_catalog", "lineage", "stewardship", "quality_context"],
    },
    {
        "code": "dataflux",
        "name": "DataFlux",
        "family": "Data Intelligence",
        "capabilities": ["source_integration", "pipeline_design", "run_monitoring", "hybrid_connectivity"],
    },
    {
        "code": "intelligent-operation",
        "name": "IO — Intelligent Operation",
        "family": "Edge & Operations",
        "capabilities": ["operations_workspace", "performance_intelligence", "decision_workflows", "enterprise_integration"],
    },
]

PRODUCT_BY_CODE = {product["code"]: product for product in PRODUCT_CATALOG}
