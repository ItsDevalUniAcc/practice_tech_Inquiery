import sqlite3
from datetime import datetime

class DataManager:
    """
    DataManager handles storage and retrieval of game session data using SQLite.

    Each game session record includes:
    - player_name: str, name of the player
    - score: int, score achieved in the session
    - level: int, level reached in the session
    - timestamp: str, time when the session was saved (YYYY-MM-DD HH:MM:SS)
    - duration: float, session duration in seconds
    - accuracy: float or None, accuracy achieved (0 to 1, or percentage) if applicable
    - mode: str, game mode name
    """

    def __init__(self, db_name="game_data.db"):
        """
        Initialize the DataManager by connecting to the SQLite database
        and creating necessary tables if they do not exist.

        Parameters:
        - db_name: str, path to the SQLite database file.
        """
        try:
            self.conn = sqlite3.connect(db_name)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            self.create_table()
        except sqlite3.Error as e:
            print(f"[DataManager] Error connecting to database: {e}")
            raise

    def create_table(self):
        """
        Create the sessions table if it doesn't already exist.
        """
        create_table_sql = """CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    score INTEGER NOT NULL,
    level INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    duration REAL NOT NULL,
    accuracy REAL,
    mode TEXT NOT NULL
);"""
        try:
            self.cursor.execute(create_table_sql)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"[DataManager] Error creating table: {e}")
            raise

    def save_session(self, player_name, score, level, duration, accuracy, mode):
        """
        Save a new game session record to the database.

        Parameters:
        - player_name: str, name of the player
        - score: int, score achieved
        - level: int, level reached
        - duration: float, session duration in seconds
        - accuracy: float or None, accuracy (e.g., 0.85 for 85%), if applicable
        - mode: str, game mode
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_sql = """INSERT INTO sessions (player_name, score, level, timestamp, duration, accuracy, mode)
VALUES (?, ?, ?, ?, ?, ?, ?);"""
        try:
            self.cursor.execute(insert_sql, (player_name, score, level, timestamp, duration, accuracy, mode))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"[DataManager] Error saving session: {e}")
            raise

    def get_top_scores(self, limit=10, player_name=None, mode=None, start_date=None, end_date=None):
        """
        Retrieve the top N game sessions ordered by score (descending).

        Optional filters:
        - player_name: str, if provided, only include this player's sessions
        - mode: str, if provided, only include sessions of this game mode
        - start_date: str or datetime, include sessions on or after this date (YYYY-MM-DD or full timestamp)
        - end_date: str or datetime, include sessions on or before this date

        Returns:
        - List of dicts, each representing a session.
        """
        base_sql = "SELECT * FROM sessions"
        filters = []
        params = []

        if player_name:
            filters.append("player_name = ?")
            params.append(player_name)
        if mode:
            filters.append("mode = ?")
            params.append(mode)
        if start_date:
            # Convert start_date to string format if needed
            if isinstance(start_date, datetime):
                start_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                try:
                    start_dt = datetime.fromisoformat(start_date)
                    start_str = start_dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    start_str = f"{start_date} 00:00:00"
            filters.append("timestamp >= ?")
            params.append(start_str)
        if end_date:
            if isinstance(end_date, datetime):
                end_str = end_date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                try:
                    end_dt = datetime.fromisoformat(end_date)
                    end_str = end_dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    end_str = f"{end_date} 23:59:59"
            filters.append("timestamp <= ?")
            params.append(end_str)

        where_clause = ""
        if filters:
            where_clause = " WHERE " + " AND ".join(filters)

        sql = f"{base_sql}{where_clause} ORDER BY score DESC LIMIT ?"
        params.append(limit)

        try:
            self.cursor.execute(sql, tuple(params))
            rows = self.cursor.fetchall()
            # Convert sqlite3.Row objects to dicts
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"[DataManager] Error retrieving top scores: {e}")
            return []

    def get_player_history(self, player_name, mode=None, start_date=None, end_date=None):
        """
        Retrieve the full game session history for a given player.

        Optional filters:
        - mode: str, if provided, only include sessions of this game mode
        - start_date: str or datetime, include sessions on or after this date
        - end_date: str or datetime, include sessions on or before this date

        Returns:
        - List of dicts, each representing a session, sorted by timestamp descending (newest first).
        """
        base_sql = "SELECT * FROM sessions"
        filters = []
        params = []

        # Filter by player name (required)
        filters.append("player_name = ?")
        params.append(player_name)

        if mode:
            filters.append("mode = ?")
            params.append(mode)
        if start_date:
            if isinstance(start_date, datetime):
                start_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                try:
                    start_dt = datetime.fromisoformat(start_date)
                    start_str = start_dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    start_str = f"{start_date} 00:00:00"
            filters.append("timestamp >= ?")
            params.append(start_str)
        if end_date:
            if isinstance(end_date, datetime):
                end_str = end_date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                try:
                    end_dt = datetime.fromisoformat(end_date)
                    end_str = end_dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    end_str = f"{end_date} 23:59:59"
            filters.append("timestamp <= ?")
            params.append(end_str)

        where_clause = " WHERE " + " AND ".join(filters)
        sql = f"{base_sql}{where_clause} ORDER BY timestamp DESC"

        try:
            self.cursor.execute(sql, tuple(params))
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"[DataManager] Error retrieving player history: {e}")
            return []

    def get_stats(self, player_name=None, mode=None, start_date=None, end_date=None):
        """
        Calculate and return statistics about game sessions.

        Statistics include:
        - average_score: float
        - best_score: int
        - total_games: int
        - average_accuracy: float

        Optional filters:
        - player_name: str, if provided, only include this player's sessions
        - mode: str, if provided, only include sessions of this game mode
        - start_date: str or datetime, include sessions on or after this date
        - end_date: str or datetime, include sessions on or before this date

        Returns:
        - dict containing the statistics.
        """
        base_sql = """SELECT
    AVG(score) as average_score,
    MAX(score) as best_score,
    COUNT(*) as total_games,
    AVG(accuracy) as average_accuracy
FROM sessions"""
        filters = []
        params = []
        if player_name:
            filters.append("player_name = ?")
            params.append(player_name)
        if mode:
            filters.append("mode = ?")
            params.append(mode)
        if start_date:
            if isinstance(start_date, datetime):
                start_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                try:
                    start_dt = datetime.fromisoformat(start_date)
                    start_str = start_dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    start_str = f"{start_date} 00:00:00"
            filters.append("timestamp >= ?")
            params.append(start_str)
        if end_date:
            if isinstance(end_date, datetime):
                end_str = end_date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                try:
                    end_dt = datetime.fromisoformat(end_date)
                    end_str = end_dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    end_str = f"{end_date} 23:59:59"
            filters.append("timestamp <= ?")
            params.append(end_str)

        where_clause = ""
        if filters:
            where_clause = " WHERE " + " AND ".join(filters)

        sql = base_sql + where_clause
        try:
            self.cursor.execute(sql, tuple(params))
            row = self.cursor.fetchone()
            if row:
                stats = {
                    "average_score": row["average_score"] if row["average_score"] is not None else 0.0,
                    "best_score": row["best_score"] if row["best_score"] is not None else 0,
                    "total_games": row["total_games"],
                    "average_accuracy": row["average_accuracy"] if row["average_accuracy"] is not None else 0.0
                }
                return stats
            else:
                return {}
        except sqlite3.Error as e:
            print(f"[DataManager] Error calculating statistics: {e}")
            return {}

    def close(self):
        """
        Close the database connection.
        """
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

    def __del__(self):
        """
        Destructor to ensure the database connection is closed.
        """
        try:
            self.close()
        except Exception:
            pass

# Example usage:
# dm = DataManager("game_data.db")
# dm.save_session("Alice", 200, 3, 60.0, 0.75, "Classic")
# top_scores = dm.get_top_scores(5)
# history = dm.get_player_history("Alice")
# stats_alice = dm.get_stats(player_name="Alice")
# stats_global = dm.get_stats()
# print(top_scores, history, stats_alice, stats_global)
# dm.close()
