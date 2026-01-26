# Duty Scheduler (근무공정표)

## Overview
A Korean military duty assignment scheduler that generates monthly duty schedules for military personnel. The application takes worker data and exception lists as input and produces CSV files with duty assignments.

## Recent Changes
- 2026-01-26: Initial import and Replit environment setup

## Project Architecture
- **main.py**: Main entry point - handles user input and orchestrates the duty assignment process
- **data_structures.py**: Custom data structures (Circular_List, List_Pointer, ChainingHashTable)
- **duty_engine.py**: Core logic for loading data, assigning duties, and exporting results
- **date.py**: Date utility functions
- **filter.py**: Filtering logic for duty assignments

## Data Files
- **worker_list.csv**: List of workers with their information
- **exception_list.csv**: List of duty exceptions
- **result_by_date.csv**: Generated output - duties organized by date
- **result_by_person.csv**: Generated output - duties organized by person

## How to Run
Run the application using Python 3.12:
```
python3 main.py
```

The application will prompt for:
1. Last duty holder for each position (enter to skip)
2. Year and month for schedule generation (e.g., "2026 1")

## Output
The application generates two CSV files:
- `result_by_date.csv`: Schedule organized by date
- `result_by_person.csv`: Schedule organized by person

## Technology Stack
- Python 3.12
- CSV file handling
- Custom data structures for circular scheduling
