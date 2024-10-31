# Meeting Scheduler System

A Python-based system that processes natural language availability statements and finds optimal meeting times for multiple participants. The system understands various formats of availability expressions and considers individual preferences while scheduling.

## Features

- Natural language processing for availability statements
- Support for recurring availability patterns
- Handling of blocked time slots and exceptions
- Preference-based meeting slot ranking
- Flexible scheduling constraints
- User-friendly interface for availability input

## Requirements

- Python 3.7+
- No external dependencies required

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MinhTienTH/AI-Problem---Meeting-Scheduler-System.git
cd meeting-scheduler
```

2. Run the demo:
```bash
python meeting_scheduler.py
```

## Usage

### Basic Usage

```python
from meeting_scheduler import MeetingScheduler

# Initialize the scheduler
scheduler = MeetingScheduler()

# Add user availability
scheduler.process_availability_message(
    "user1",
    "I am available every morning from 9 to 11 AM, except on Wednesdays."
)

# Find common slots
common_slots = scheduler.find_common_slots(duration_hours=1)
```

### Example Availability Statements

The system can understand various formats of availability statements:

1. Recurring availability:
```python
"I am available every morning from 9 to 11 AM, except on Wednesdays."
```

2. Specific day preferences:
```python
"I am free on Tuesdays, but if possible, I prefer an early morning slot."
```

3. Blocked times:
```python
"I already have a meeting booked on Friday from 2 to 4 PM."
```

## System Design

### Core Components

1. `TimeSlot` class:
   - Represents a specific time period
   - Contains day, start time, and end time

2. `Availability` class:
   - Stores user availability information
   - Contains available slots, preferences, and blocked times

3. `MeetingScheduler` class:
   - Main scheduling logic
   - Natural language processing
   - Common slot finding algorithm

### Key Methods

1. `process_availability_message(user_id: str, message: str)`:
   - Processes natural language availability statements
   - Returns structured availability data

2. `find_common_slots(duration_hours: int = 1)`:
   - Finds common available time slots
   - Returns sorted list based on preferences

## Assumptions and Limitations

1. Time-related assumptions:
   - Working hours: 9 AM to 5 PM
   - Weekdays only
   - Single timezone
   - Whole hour slots only

2. Language processing:
   - Limited to common English phrases
   - Basic time format understanding
   - Simple preference expressions

## Future Enhancements

1. Time handling improvements:
   - Multiple timezone support
   - 30-minute slot granularity
   - Weekend availability

2. Feature additions:
   - Calendar integration (Google Calendar, Outlook)
   - More complex natural language processing
   - Recurring meeting patterns
   - Meeting priority handling

3. User interface:
   - Web interface
   - REST API
   - Command-line tool

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Testing

Run the included demo to test the system:

```python
if __name__ == "__main__":
    demo_scheduler()
```

The demo includes example availability statements and demonstrates the scheduling process.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - Nguyen Minh Tien
Project Link: https://github.com/MinhTienTH/AI-Problem---Meeting-Scheduler-System.git