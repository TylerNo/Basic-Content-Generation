from auto_content_generator.midnight_smokey.core.midnight_smokey_manager import start_midnight_smokey_manager
from auto_content_generator.mock_times.core.mock_times_manager import start_mock_times_manager
from auto_content_generator.core.main.scraper_manager import start_scraper_manager
from auto_content_generator.core.main.database_init import start_database_init
from auto_content_generator.fact_drip.core.fact_drip_manager import start_fact_drip_manager
import time

def acg_main(app_logs, MAX_LOG_ENTRIES, config, log_manager):
    enable_midnight_smokey = config['functions']['midnight_smokey']
    enable_mock_times = config['functions']['mock_times']
    enable_fact_drip = config['functions']['fact_drip']

    start_database_init(app_logs, MAX_LOG_ENTRIES, log_manager)

    while log_manager.stop_signal == False:
        start_scraper_manager(app_logs, MAX_LOG_ENTRIES, config, log_manager)
        if enable_midnight_smokey == True:
            start_midnight_smokey_manager(log_manager, app_logs, MAX_LOG_ENTRIES)
        if enable_mock_times == True:
            start_mock_times_manager(config, log_manager, app_logs, MAX_LOG_ENTRIES)
        if enable_fact_drip == True:
            start_fact_drip_manager(config, log_manager, app_logs, MAX_LOG_ENTRIES)



