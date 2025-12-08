"""Database connection handler."""
import sqlite3
from contextlib import contextmanager

class DatabaseManager:
    """Manage database connections and operations."""
    
    def __init__(self, db_path: str = "data/healthcare.db"):
        self.db_path = db_path
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = ()):
        """Execute a query and return results."""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()
    
    def execute_update(self, query: str, params: tuple = ()):
        """Execute an update/insert query."""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.rowcount
