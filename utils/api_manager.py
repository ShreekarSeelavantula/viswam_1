import os
import streamlit as st
from datetime import datetime, timedelta
import json

class APIKeyManager:
    def __init__(self):
        self.api_keys = self._load_api_keys()
        self.current_key_index = 0
        self.usage_counts = self._load_usage_counts()
        self.rate_limit_warning_threshold = 45  # Warn when approaching 50 requests
        
    def _load_api_keys(self):
        """Load API keys from environment variables"""
        keys = []
        
        # Primary key
        primary_key = os.environ.get("OPENAI_API_KEY")
        if primary_key:
            keys.append({"key": primary_key, "name": "Primary"})
        
        # Secondary key (OPENAI_API_KEY2)
        secondary_key = os.environ.get("OPENAI_API_KEY2")
        if secondary_key:
            keys.append({"key": secondary_key, "name": "Secondary"})
        
        # Additional backup keys (if available)
        backup_key_1 = os.environ.get("OPENAI_API_KEY_BACKUP1")
        if backup_key_1:
            keys.append({"key": backup_key_1, "name": "Backup 1"})
            
        backup_key_2 = os.environ.get("OPENAI_API_KEY_BACKUP2")
        if backup_key_2:
            keys.append({"key": backup_key_2, "name": "Backup 2"})
        
        return keys
    
    def _load_usage_counts(self):
        """Load usage counts from session state"""
        if 'api_usage_counts' not in st.session_state:
            st.session_state.api_usage_counts = {}
        return st.session_state.api_usage_counts
    
    def _save_usage_counts(self):
        """Save usage counts to session state"""
        st.session_state.api_usage_counts = self.usage_counts
    
    def get_current_key(self):
        """Get the current active API key"""
        if not self.api_keys:
            return None
        
        if self.current_key_index >= len(self.api_keys):
            self.current_key_index = 0
        
        return self.api_keys[self.current_key_index]
    
    def record_usage(self, success=True):
        """Record API usage for the current key"""
        current_key = self.get_current_key()
        if not current_key:
            return
        
        key_name = current_key["name"]
        today = datetime.now().strftime("%Y-%m-%d")
        
        if key_name not in self.usage_counts:
            self.usage_counts[key_name] = {}
        
        if today not in self.usage_counts[key_name]:
            self.usage_counts[key_name][today] = {"requests": 0, "errors": 0}
        
        self.usage_counts[key_name][today]["requests"] += 1
        
        if not success:
            self.usage_counts[key_name][today]["errors"] += 1
        
        self._save_usage_counts()
        
        # Check if we should proactively switch keys
        if success and self.should_warn_about_limit():
            self._proactive_key_switch()
    
    def get_daily_usage(self, key_name=None):
        """Get daily usage for a specific key or current key"""
        if key_name is None:
            current_key = self.get_current_key()
            if not current_key:
                return 0, 0
            key_name = current_key["name"]
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        if key_name in self.usage_counts and today in self.usage_counts[key_name]:
            return (
                self.usage_counts[key_name][today]["requests"],
                self.usage_counts[key_name][today]["errors"]
            )
        
        return 0, 0
    
    def should_warn_about_limit(self):
        """Check if we should warn about approaching rate limit"""
        requests, _ = self.get_daily_usage()
        return requests >= self.rate_limit_warning_threshold
    
    def _proactive_key_switch(self):
        """Proactively switch keys when approaching limit"""
        if len(self.api_keys) <= 1:
            return False
        
        # Check if next key has lower usage
        next_index = (self.current_key_index + 1) % len(self.api_keys)
        next_key = self.api_keys[next_index]
        next_requests, _ = self.get_daily_usage(next_key['name'])
        
        current_requests, _ = self.get_daily_usage()
        
        # Switch if next key has significantly lower usage
        if next_requests < current_requests - 10:
            old_key = self.get_current_key()
            self.current_key_index = next_index
            new_key = self.get_current_key()
            st.info(f"🔄 Proactively switched from {old_key['name']} ({current_requests} requests) to {new_key['name']} ({next_requests} requests) to avoid rate limits.")
            return True
        
        return False
    
    def switch_to_next_key(self):
        """Switch to the next available API key"""
        if len(self.api_keys) <= 1:
            return False
        
        old_key = self.get_current_key()
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        new_key = self.get_current_key()
        
        if old_key and new_key:
            st.warning(f"⚠️ Switched from {old_key['name']} API key to {new_key['name']} API key due to rate limiting.")
            return True
        
        return False
    
    def handle_rate_limit_error(self):
        """Handle rate limit error by switching keys if available"""
        current_key = self.get_current_key()
        if current_key:
            requests, errors = self.get_daily_usage()
            st.error(f"🚫 Rate limit reached for {current_key['name']} API key (Used: {requests} requests today)")
        
        if self.switch_to_next_key():
            new_key = self.get_current_key()
            new_requests, _ = self.get_daily_usage(new_key['name'])
            st.success(f"✅ Automatically switched to {new_key['name']} API key (Used: {new_requests} requests today)")
            return True
        else:
            st.error("❌ All API keys have reached their rate limits. Please wait or add more API keys.")
            return False
    
    def show_usage_status(self):
        """Display current API usage status"""
        if not self.api_keys:
            st.error("❌ No API keys configured")
            return
        
        current_key = self.get_current_key()
        if not current_key:
            return
        
        requests, errors = self.get_daily_usage()
        
        # Show warning if approaching limit
        if self.should_warn_about_limit():
            st.warning(f"⚠️ API Usage Warning: {requests}/50 requests used today with {current_key['name']} key. Will auto-switch if limit reached.")
        
        # Show info about current usage
        with st.expander("📊 API Usage Status", expanded=False):
            st.write(f"**Current Key:** {current_key['name']}")
            st.write(f"**Today's Usage:** {requests} requests, {errors} errors")
            st.write(f"**Available Keys:** {len(self.api_keys)} total")
            
            if len(self.api_keys) > 1:
                st.write("**All Keys Status:**")
                for i, key_info in enumerate(self.api_keys):
                    key_requests, key_errors = self.get_daily_usage(key_info['name'])
                    status = "🟢 Active" if i == self.current_key_index else "⚪ Standby"
                    limit_status = "⚠️ Near Limit" if key_requests >= 45 else "✅ Available"
                    st.write(f"  - {key_info['name']}: {key_requests}/50 requests, {key_errors} errors - {limit_status} {status}")

# Global API manager instance
api_manager = APIKeyManager()