import sqlite3
import os

DB_FILE = 'history_cache.db'

def initialize_db():
    """
    Initialise la base de données SQLite. Crée la table si elle n'existe pas déjà.
    """
    # Vérifie si le fichier de base de données existe déjà
    db_exists = os.path.exists(DB_FILE)

    # Connexion à la base de données (crée le fichier si nécessaire)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Si la base de données n'existait pas, créer la table
    if not db_exists:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history_cache (
                id INTEGER PRIMARY KEY,
                history_id INTEGER
            )
        ''')
        conn.commit()

    conn.close()

def load_history_id():
    """
    Charge le history_id à partir de la base de données SQLite.
    Retourne None si aucun history_id n'est trouvé.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT history_id FROM history_cache WHERE id=1')
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def save_history_id(history_id):
    """
    Sauvegarde le history_id dans la base de données SQLite.
    Si un history_id existe déjà, il est mis à jour.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO history_cache (id, history_id)
        VALUES (1, ?)
    ''', (history_id,))
    conn.commit()
    conn.close()

def clear_history_id():
    """
    Supprime le history_id du cache SQLite.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM history_cache WHERE id=1')
    conn.commit()
    conn.close()
    print("Cache supprimé : history_id réinitialisé.")
