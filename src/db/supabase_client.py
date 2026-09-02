"""
Nivra Supabase Database Client & Persistent Storage Manager
Manages PostgreSQL / Supabase storage for user bookmarked schemes, chat history,
and scheme metadata with seamless fallback local persistence.
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

logger = logging.getLogger("nivra.supabase")
logging.basicConfig(level=logging.INFO)

class SupabaseManager:
    """Manages Supabase database operations with fallback local persistence."""
    
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL", "")
        self.supabase_key = os.getenv("SUPABASE_KEY", "")
        self.client = None
        self.is_connected = False

        # In-memory / file fallback storage
        self._fallback_saved_schemes = set(["Stand-Up India Scheme", "WE Hub Telangana Prototype Grant"])
        self._fallback_chat_logs = []

        self._init_supabase()

    def _init_supabase(self):
        """Initializes official Supabase client if valid credentials exist."""
        if self.supabase_url and self.supabase_key and "your-project" not in self.supabase_url:
            try:
                from supabase import create_client, Client
                self.client: Client = create_client(self.supabase_url, self.supabase_key)
                self.is_connected = True
                logger.info(f"Successfully connected to Supabase database at {self.supabase_url}")
            except Exception as e:
                logger.warning(f"Failed to connect to Supabase: {e}. Activating local persistence fallback.")
                self.is_connected = False
        else:
            logger.info("Supabase credentials not provided. Running in local fallback persistence mode.")
            self.is_connected = False

    # --- Saved Schemes Operations ---
    def save_scheme(self, scheme_name: str, user_id: str = "demo_user") -> bool:
        """Saves a bookmarked scheme for a user."""
        if self.is_connected and self.client:
            try:
                data = {
                    "user_id": user_id,
                    "scheme_name": scheme_name
                }
                self.client.table("saved_schemes").upsert(data).execute()
                logger.info(f"Saved scheme '{scheme_name}' to Supabase database.")
                return True
            except Exception as e:
                logger.error(f"Error saving scheme to Supabase: {e}")
        
        # Fallback
        self._fallback_saved_schemes.add(scheme_name)
        return True

    def remove_saved_scheme(self, scheme_name: str, user_id: str = "demo_user") -> bool:
        """Removes a bookmarked scheme for a user."""
        if self.is_connected and self.client:
            try:
                self.client.table("saved_schemes").delete().eq("user_id", user_id).eq("scheme_name", scheme_name).execute()
                logger.info(f"Removed scheme '{scheme_name}' from Supabase database.")
                return True
            except Exception as e:
                logger.error(f"Error removing scheme from Supabase: {e}")

        # Fallback
        self._fallback_saved_schemes.discard(scheme_name)
        return True

    def get_saved_schemes(self, user_id: str = "demo_user") -> List[str]:
        """Fetches all bookmarked schemes for a user."""
        if self.is_connected and self.client:
            try:
                response = self.client.table("saved_schemes").select("scheme_name").eq("user_id", user_id).execute()
                if response.data:
                    return [item["scheme_name"] for item in response.data]
            except Exception as e:
                logger.error(f"Error fetching saved schemes from Supabase: {e}")

        # Fallback
        return list(self._fallback_saved_schemes)

    # --- Chat History Operations ---
    def log_chat(self, query: str, official_answer: str, plain_answer: str, language: str) -> bool:
        """Logs a Q&A interaction to Supabase chat_history table."""
        chat_entry = {
            "query": query,
            "official_answer": official_answer,
            "plain_answer": plain_answer,
            "language": language
        }
        if self.is_connected and self.client:
            try:
                self.client.table("chat_history").insert(chat_entry).execute()
                logger.info("Logged chat interaction to Supabase.")
                return True
            except Exception as e:
                logger.error(f"Error logging chat to Supabase: {e}")

        # Fallback
        self._fallback_chat_logs.append(chat_entry)
        return True

    def get_chat_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Fetches past Q&A interactions."""
        if self.is_connected and self.client:
            try:
                response = self.client.table("chat_history").select("*").order("id", desc=True).limit(limit).execute()
                if response.data:
                    return response.data
            except Exception as e:
                logger.error(f"Error fetching chat history from Supabase: {e}")

        # Fallback
        return list(reversed(self._fallback_chat_logs[-limit:]))

# Singleton Instance
supabase_manager = SupabaseManager()
