import sqlite3

db_name = "auto_content_generator/fact_drip/databases/facts.db"

def start_facts_db_init(config, log_manager, app_logs, MAX_LOG_ENTRIES):
    log_message = "Starting Fact Drip Database Initializing..."
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY,
            module TEXT NOT NULL,
            category TEXT NOT NULL,
            fact_pt1 TEXT NOT NULL,
            fact_pt2 TEXT NOT NULL,
            status TEXT NOT NULL
        );
    ''')

    conn.commit()
    conn.close()

def get_random_fact(module, config, log_manager, app_logs, MAX_LOG_ENTRIES):
    log_message = f"Getting random {module} fact..."
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM facts 
        WHERE module = ? AND status = "new"
        ORDER BY RANDOM() 
        LIMIT 1;
    ''', (module,))

    fact = cursor.fetchone()
    conn.close()

    if fact:
        log_message = "Retrieved random fact: " + str(fact)
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
        return fact
    else:
        log_message = f"There were no new {module} facts..."
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
        return None



def check_fact_duplicate(category, fact_pt1, fact_pt2):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT COUNT(*) FROM facts 
        WHERE category = ? AND fact_pt1 = ? AND fact_pt2 = ?;
    ''', (category, fact_pt1, fact_pt2))

    count = cursor.fetchone()[0]

    conn.close()

    return count > 0


def insert_fact(module, category, fact_pt1, fact_pt2):
    if len(category) > 28:
        print("Error: 'category' character count exceeds 35.")
        return
    if len(fact_pt1) > 100:
        print("Error: 'fact_pt1' character count exceeds 100.")
        return
    if len(fact_pt2) > 100:
        print("Error: 'fact_pt2' character count exceeds 100.")
        return

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO facts (module, category, fact_pt1, fact_pt2, status)
        VALUES (?, ?, ?, ?, "new");
    ''', (module, category, fact_pt1, fact_pt2))

    conn.commit()
    conn.close()


def update_fact_status(psychology_fact, log_manager, app_logs, MAX_LOG_ENTRIES):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    fact_id = psychology_fact[0]

    query = '''
        UPDATE facts 
        SET status = "uploaded" 
        WHERE id = ?;
    '''

    cursor.execute(query, (fact_id,))

    conn.commit()
    conn.close()

    log_message = "Successfully updated database status for fact: " + str(fact_id)
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)