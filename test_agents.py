# test_agents.py
import os
from app.ai_agents.agents import AGENTS
import asyncio
from app.ai_agents.strategy.ai_strategy_agent import AIStrategyAgent



# Проверка API-ключа
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY не найден в окружении!")

print("🔍 Проверяю API-ключ...\n")
print("✅ OPENROUTER_API_KEY найден\n")

agent_names = list(AGENTS.keys())
print(f"📌 Найдено агентов: {len(agent_names)}")
print(agent_names, "\n")

print("=== ТЕСТ ЗАПУЩЕН ===\n")

# Минимальные тестовые данные для разных типов аргументов
test_payload = {"test": "data"}
test_input_data = {"test": "data"}
test_goal = {"goal": "test goal"}
test_project = {"project_name": "Test Project", "niche": "Test Niche"}
test_situation = {"situation": "Test Situation"}

# Словарь соответствия имени аргумента для run()
agent_args = {
    "ai_data_agent": ("payload", test_payload),
    "ai_designer": ("payload", test_payload),
    "ai_ux": ("payload", test_payload),
    "ai_video_creator": ("payload", test_payload),
    "ai_webbuilder": ("project_name", test_project),  # webbuilder требует два поля
    "ai_ceo_assistant": None,  # нет метода run
    "ai_client_psychologist": ("situation", test_situation),
    "ai_experiments_agent": ("input_data", test_input_data),
    "ai_growth_agent": ("input_data", test_input_data),
    "ai_training_curator": ("goal", test_goal),
    "ai_crm_agent": ("input_data", test_input_data),
    "ai_project_manager": ("payload", test_payload),
    "ai_workflow_builder": ("payload", test_payload),
    "ai_brand_manager": ("input_data", test_input_data),
    "ai_competitor_agent": ("input_data", test_input_data),
    "ai_content_agent": ("input_data", test_input_data),
    "ai_copywriter": ("payload", test_payload),
    "ai_marketing_agent": ("input_data", test_input_data),
    "ai_market_research_agent": ("input_data", test_input_data),
    "ai_seo_specialist": ("input_data", test_input_data),
    "ai_smm_manager": ("input_data", test_input_data),
    "ai_traffic_manager": ("payload", test_payload),
    "ai_accountant": ("payload", test_payload),
    "ai_admin_assistant": ("payload", test_payload),
    "ai_compliance_agent": ("payload", test_payload),
    "ai_hr": ("input_data", test_input_data),
    "ai_legal_agent": ("input_data", test_input_data),
    "ai_onboarding_agent": ("input_data", test_input_data),
    "ai_call_bot": ("payload", test_payload),
    "ai_client_service_manager": ("payload", test_payload),
    "ai_lead_scoring_agent": ("input_data", test_input_data),
    "ai_sales_manager": ("input_data", test_input_data),
    "ai_business_analyst": ("input_data", test_input_data),
    "ai_finance_docs_agent": ("input_data", test_input_data),
    "ai_financial_analyst": ("input_data", test_input_data),
    "ai_operations_agent": ("input_data", test_input_data),
    "ai_product_manager": ("input_data", test_input_data),
    "ai_strategy_agent": ("input_data", test_input_data),
}

for name in agent_names:
    agent = AGENTS[name]
    print(f"=== Тест агента: {name} ===")
    
    arg_info = agent_args.get(name)
    
    try:
        if arg_info is None:
            print("❌ У агента нет метода run или call_api\n")
            continue

        arg_name, arg_value = arg_info
        
        # webbuilder требует оба поля передавать как **project_name
        if name == "ai_webbuilder":
            response = agent.run(**arg_value)
        else:
            response = getattr(agent, "run")( **{arg_name: arg_value} )
        
        print("✅ Успешно выполнено\n")
    except Exception as e:
        print(f"❌ Ошибка: {e}\n")
