ANTRASCIU_STRUKTURA_CREATE_QUERY = """
    CREATE TABLE IF NOT EXISTS antrasciu_struktura (
        heading TEXT NOT NULL,
        your_suggestion TEXT NOT NULL
    )
"""
TEKSTO_KOREKCIJOS_REKOMENDACIJOS_CREATE_QUERY = """
    CREATE TABLE IF NOT EXISTS teksto_korekcijos_rekomendacijos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_word TEXT NOT NULL,
        suggested_correction TEXT NOT NULL,
        reasoning TEXT
    )
"""
INSERT_INTO_ANTRASCIU_STRUKTURA_QUERY = """
    INSERT INTO antrasciu_struktura (heading, your_suggestion)
    VALUES ('{heading}', '{suggestion}')
"""
INSERT_INTO_TEKSTO_KOREKCIJOS = """
    INSERT INTO teksto_korekcijos_rekomendacijos (original_word, suggested_correction, reasoning)
    VALUES ('{original_word}', '{suggested_correction}', '{reasoning}')
"""