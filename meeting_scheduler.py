from datetime import datetime, timedelta
import re
from typing import List, Dict, Set
from dataclasses import dataclass
import calendar

@dataclass
class TimeSlot:
    day: str
    start_time: int  # 24-hour format, hours only
    end_time: int    # 24-hour format, hours only

@dataclass
class Availability:
    user_id: str
    available_slots: List[TimeSlot]
    preferences: Dict[str, str]  # Store preferences like "early morning"
    blocked_slots: List[TimeSlot]

class MeetingScheduler:
    def __init__(self):
        self.users: Dict[str, Availability] = {}
        self.weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        
        # Define time periods for preference matching
        self.time_periods = {
            'early morning': (9, 11),
            'morning': (9, 12),
            'afternoon': (12, 17),
            'late afternoon': (15, 17)
        }

    def convert_12h_to_24h(self, time: int, period: str) -> int:
        """Convert 12-hour format to 24-hour format"""
        if period.upper() == 'PM' and time != 12:
            return time + 12
        elif period.upper() == 'AM' and time == 12:
            return 0
        return time

    def process_availability_message(self, user_id: str, message: str):
        """Process natural language availability message"""
        message = message.lower()
        availability = Availability(user_id, [], {}, [])

        # Process recurring availability
        if "every morning" in message:
            time_range = re.search(r'from (\d+)(?:\s*)(am|pm)? to (\d+)(?:\s*)(am|pm)?', message, re.IGNORECASE)
            if time_range:
                start_time = int(time_range.group(1))
                start_period = time_range.group(2) or 'AM'
                end_time = int(time_range.group(3))
                end_period = time_range.group(4) or 'AM'
                
                start_time = self.convert_12h_to_24h(start_time, start_period)
                end_time = self.convert_12h_to_24h(end_time, end_period)
                
                # Handle "except" cases
                excluded_days = []
                if "except" in message:
                    excluded_days = [day for day in self.weekdays 
                                  if day in message.split("except")[1]]

                # Add available slots for all weekdays except excluded ones
                for day in self.weekdays:
                    if day not in excluded_days:
                        availability.available_slots.append(
                            TimeSlot(day, start_time, end_time)
                        )

        # Process specific day availability
        for day in self.weekdays:
            if day in message:
                if "free" in message or "available" in message:
                    if "early morning" in message:
                        availability.preferences[day] = "early morning"
                        availability.available_slots.append(
                            TimeSlot(day, 9, 11)
                        )
                    else:
                        # Default full day availability
                        availability.available_slots.append(
                            TimeSlot(day, 9, 17)
                        )

        # Process blocked times
        if "meeting" in message and "from" in message:
            time_range = re.search(r'from (\d+)(?:\s*)(am|pm)? to (\d+)(?:\s*)(am|pm)', message, re.IGNORECASE)
            if time_range:
                start_time = int(time_range.group(1))
                start_period = time_range.group(2) or 'PM'  # Default to PM if not specified
                end_time = int(time_range.group(3))
                end_period = time_range.group(4) or 'PM'    # Default to PM if not specified
                
                start_time = self.convert_12h_to_24h(start_time, start_period)
                end_time = self.convert_12h_to_24h(end_time, end_period)
                
                # Add default availability for the mentioned day
                for day in self.weekdays:
                    if day in message:
                        # Add full day availability except for blocked time
                        availability.available_slots.append(TimeSlot(day, 9, start_time))
                        availability.available_slots.append(TimeSlot(day, end_time, 17))
                        availability.blocked_slots.append(TimeSlot(day, start_time, end_time))

        # If no specific availability is mentioned, assume standard work hours
        if not availability.available_slots and not availability.blocked_slots:
            for day in self.weekdays:
                availability.available_slots.append(TimeSlot(day, 9, 17))

        self.users[user_id] = availability
        return availability

    def find_common_slots(self, duration_hours: int = 1) -> List[TimeSlot]:
        """Find common available time slots for all users"""
        if not self.users:
            return []

        # Get all possible time slots
        common_slots = []
        for day in self.weekdays:
            for start_hour in range(9, 17):  # 9 AM to 5 PM
                slot = TimeSlot(day, start_hour, start_hour + duration_hours)
                
                # Check if slot works for all users
                slot_works = True
                for user_id, availability in self.users.items():
                    # Check if slot is in user's available slots
                    slot_available = False
                    for avail_slot in availability.available_slots:
                        if (avail_slot.day == slot.day and 
                            avail_slot.start_time <= slot.start_time and 
                            avail_slot.end_time >= slot.end_time):
                            slot_available = True
                            break
                    
                    # Check if slot conflicts with blocked slots
                    for blocked_slot in availability.blocked_slots:
                        if (blocked_slot.day == slot.day and 
                            not (slot.end_time <= blocked_slot.start_time or 
                                 slot.start_time >= blocked_slot.end_time)):
                            slot_available = False
                            break
                    
                    if not slot_available:
                        slot_works = False
                        break
                
                if slot_works:
                    common_slots.append(slot)

        # Sort slots based on preferences
        def preference_score(slot: TimeSlot) -> int:
            score = 0
            for user_id, availability in self.users.items():
                if slot.day in availability.preferences:
                    pref = availability.preferences[slot.day]
                    if pref == "early morning" and slot.start_time <= 11:
                        score += 1
            return score

        return sorted(common_slots, key=preference_score, reverse=True)

def demo_scheduler():
    scheduler = MeetingScheduler()
    
    # Process example messages
    messages = [
        ("User_A", "I am available every morning from 9 to 11 AM, except on Wednesdays."),
        ("User_B", "I am free on Tuesdays, but if possible, I prefer an early morning slot."),
        ("User_C", "I already have a meeting booked on Friday from 2 to 4 PM.")
    ]
    
    print("Processing availability messages:")
    print("-" * 50)
    for user_id, message in messages:
        print(f"\nProcessing message from {user_id}:")
        print(f"Message: {message}")
        availability = scheduler.process_availability_message(user_id, message)
        print(f"Processed availability slots: {availability.available_slots}")
        print(f"Blocked slots: {availability.blocked_slots}")
        print(f"Preferences: {availability.preferences}")
    
    print("\nFinding common available slots:")
    print("-" * 50)
    common_slots = scheduler.find_common_slots(duration_hours=1)
    
    if common_slots:
        print("\nPossible meeting slots (in order of preference):")
        for slot in common_slots:
            day_name = slot.day.capitalize()
            start_time = f"{slot.start_time}:00"
            end_time = f"{slot.end_time}:00"
            print(f"- {day_name}: {start_time} - {end_time}")
    else:
        print("\nNo common slots found!")

if __name__ == "__main__":
    demo_scheduler()