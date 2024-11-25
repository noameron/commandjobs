from abc import ABC, abstractmethod
import sqlite3


class AbstractJobScraper(ABC):
    def __init__(self, db_path='job_listings.db'):
        self.db_path = db_path
        self.new_entries_count = 0  # Initialize counter for new entries

    @abstractmethod
    def scrape_jobs(self, *args, **kwargs):
        pass

    def save_to_database(self, original_text, original_html, source, external_id):
        """
        Save a job listing to the SQLite database. Uses INSERT OR IGNORE to skip existing records.
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "INSERT OR IGNORE INTO job_listings (original_text, original_html, source, external_id) VALUES (?, ?, ?, ?)",
            (original_text, original_html, source, external_id),
        )
        conn.commit()
        conn.close()
        return c.rowcount > 0  # True if the listing was inserted

