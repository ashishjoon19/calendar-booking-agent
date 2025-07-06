from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

class CalendarService:
    def __init__(self):
        self.service = self._authenticate()
        self.calendar_id = 'primary'  # Use primary calendar
    
    def _authenticate(self):
        """Authenticate with Google Calendar API using service account"""
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        
        # Path to service account key file
        service_account_file = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'credentials/service-account-key.json')
        
        credentials = Credentials.from_service_account_file(
            service_account_file,
            scopes=SCOPES
        )
        
        return build('calendar', 'v3', credentials=credentials)
    
    def get_events(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get events from calendar between start and end dates"""
        try:
            # Convert dates to RFC3339 format
            start_time = f"{start_date}T00:00:00Z"
            end_time = f"{end_date}T23:59:59Z"
            
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=start_time,
                timeMax=end_time,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            return events_result.get('items', [])
            
        except Exception as e:
            print(f"Error getting events: {e}")
            return []
    
    def create_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new calendar event"""
        try:
            event = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event_data
            ).execute()
            
            return event
            
        except Exception as e:
            print(f"Error creating event: {e}")
            raise e
    
    def delete_event(self, event_id: str) -> bool:
        """Delete a calendar event"""
        try:
            self.service.events().delete(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()
            
            return True
            
        except Exception as e:
            print(f"Error deleting event: {e}")
            raise e
    
    def update_event(self, event_id: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing calendar event"""
        try:
            event = self.service.events().update(
                calendarId=self.calendar_id,
                eventId=event_id,
                body=event_data
            ).execute()
            
            return event
            
        except Exception as e:
            print(f"Error updating event: {e}")
            raise e