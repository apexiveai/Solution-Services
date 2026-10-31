MODULE_CATALOG = [
    {"code": "manufacturing-core", "name": "Manufacturing Core Platform", "required": True},
    {"code": "smart-factory", "name": "Smart Factory Operations", "required": False},
    {"code": "industrial-iot-data", "name": "Industrial IoT & Data Platform", "required": False},
    {"code": "predictive-maintenance", "name": "AI Predictive Maintenance", "required": False},
    {"code": "quality-production-intelligence", "name": "Quality & Production Intelligence", "required": False},
    {"code": "supply-chain-warehouse", "name": "Supply Chain & Warehouse", "required": False},
    {"code": "manufacturing-command-center", "name": "Manufacturing Command Center", "required": False},
]

CAPABILITY_CATALOG = [
    "manufacturing_data_management",
    "factory_operations",
    "production_planning_and_scheduling",
    "industrial_iot",
    "predictive_maintenance",
    "quality_management",
    "supply_chain_management",
    "warehouse_management",
    "energy_management",
    "manufacturing_erp_integration",
    "industrial_big_data",
    "ai_manufacturing_command_center",
]

ARCHITECTURE_LAYERS = [
    {
        "name": "Production & Factory Equipment",
        "components": ["PLC", "SCADA", "Sensors", "Machines", "IoT Gateways"],
    },
    {
        "name": "Industrial Data Platform",
        "components": ["Data Integration", "Streaming", "Historian", "Data Governance"],
    },
    {
        "name": "AI & Big Data Intelligence",
        "components": ["Predictive Analytics", "Computer Vision", "AI Agents", "Digital Twin"],
    },
    {
        "name": "Enterprise Operations",
        "components": ["MES", "ERP", "SCM", "WMS", "QMS", "CRM"],
    },
    {
        "name": "Manufacturing Command Center",
        "components": ["Production", "Quality", "Cost", "Inventory", "Performance"],
    },
]
