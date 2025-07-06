from langchain.tools import tool
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

def get_calendar_tools(calendar_service):
    """Get all calendar-related tools"""
    
    @tool
    def check_availability(start_date: str, end_date: str) -> str:
        """Check calendar availability for a date range.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
        """
        try:
            events = calendar_service.get_events(start_date, end_date)
            if not events:
                return f"No events found between {start_date} and {end_date}. You're free!"
            
            event_list = []
            for event in events:
                start = event.get('start', {}).get('dateTime', event.get('start', {}).get('date'))
                end = event.get('end', {}).get('dateTime', event.get('end', {}).get('date'))
                summary = event.get('summary', 'No title')
                event_list.append(f"- {summary}: {start} to {end}")
            
            return f"Events between {start_date} and {end_date}:\n" + "\n".join(event_list)
            
        except Exception as e:
            return f"Error checking availability: {str(e)}"
    
    @tool
    def book_appointment(title: str, start_datetime: str, duration_minutes: int = 60, description: str = "") -> str:
        """Book an appointment on the calendar.
        
        Args:
            title: Title of the appointment
            start_datetime: Start date and time in ISO format (YYYY-MM-DDTHH:MM:SS)
            duration_minutes: Duration in minutes (default 60)
            description: Optional description
        """
        try:
            # Calculate end time
            start_dt = datetime.fromisoformat(start_datetime.replace('Z', '+00:00'))
            end_dt = start_dt + timedelta(minutes=duration_minutes)
            
            event_data = {
                'summary': title,
                'description': description,
                'start': {
                    'dateTime': start_dt.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_dt.isoformat(),
                    'timeZone': 'UTC',
                },
            }
            
            event = calendar_service.create_event(event_data)
            
            return f"✅ Appointment booked successfully!\n" \
                   f"Title: {title}\n" \
                   f"Start: {start_datetime}\n" \
                   f"Duration: {duration_minutes} minutes\n" \
                   f"Event ID: {event.get('id')}"
                   
        except Exception as e:
            return f"Error booking appointment: {str(e)}"
    
    @tool
    def list_upcoming_appointments(days_ahead: int = 7) -> str:
        """List upcoming appointments.
        
        Args:
            days_ahead: Number of days ahead to check (default 7)
        """
        try:
            start_date = datetime.now().date().isoformat()
            end_date = (datetime.now() + timedelta(days=days_ahead)).date().isoformat()
            
            events = calendar_service.get_events(start_date, end_date)
            
            if not events:
                return f"No upcoming appointments in the next {days_ahead} days."
            
            event_list = []
            for event in events:
                start = event.get('start', {}).get('dateTime', event.get('start', {}).get('date'))
                summary = event.get('summary', 'No title')
                event_list.append(f"- {summary}: {start}")
            
            return f"Upcoming appointments ({days_ahead} days):\n" + "\n".join(event_list)
            
        except Exception as e:
            return f"Error listing appointments: {str(e)}"
    
    @tool
    def cancel_appointment(event_id: str) -> str:
        """Cancel an appointment by event ID.
        
        Args:
            event_id: The Google Calendar event ID
        """
        try:
            calendar_service.delete_event(event_id)
            return f"✅ Appointment {event_id} cancelled successfully!"
            
        except Exception as e:
            return f"Error cancelling appointment: {str(e)}"
    
    return [check_availability, book_appointment, list_upcoming_appointments, cancel_appointment]