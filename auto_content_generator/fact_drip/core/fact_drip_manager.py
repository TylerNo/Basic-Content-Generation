from auto_content_generator.fact_drip.fact_modules.psychology_facts.psychology_facts_manager import start_psychology_facts_manager
from auto_content_generator.fact_drip.fact_modules.motivation_facts.motivation_facts_manager import start_motivation_facts_manager
from auto_content_generator.fact_drip.databases.facts_db_manager import start_facts_db_init
from auto_content_generator.fact_drip.fact_modules.legal_facts.legal_facts_manager import start_legal_facts_manager

def start_fact_drip_manager(config, log_manager, app_logs, MAX_LOG_ENTRIES):
    log_message = "Starting Fact Drip Manager..."
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    start_facts_db_init(config, log_manager, app_logs, MAX_LOG_ENTRIES)

    enable_psychology_facts = config['fact_drip']['psychology_facts']
    enable_legal_facts = config['fact_drip']['legal_facts']
    enable_motivation_facts = config['fact_drip']['motivation_facts']

    if enable_psychology_facts == True:
        start_psychology_facts_manager(config, log_manager, app_logs, MAX_LOG_ENTRIES)

    if enable_legal_facts == True:
        start_legal_facts_manager(config, log_manager, app_logs, MAX_LOG_ENTRIES)

    if enable_motivation_facts == True:
        start_motivation_facts_manager(config, log_manager, app_logs, MAX_LOG_ENTRIES)
