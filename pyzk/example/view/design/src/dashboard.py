import pandas as pd
from datetime import datetime, timedelta

# Example data structure fetched from the database
data = [
    (1, 'in', '2023-07-01', '08:00:00'),
    (1, 'out', '2023-07-01', '17:00:00'),
    (1, 'in', '2023-07-02', '08:30:00'),
    (1, 'out', '2023-07-02', '16:45:00'),
    # Add more entries
]


# Create a DataFrame from the data
df = pd.DataFrame(data, columns=['id_employee', 'event_type', 'event_date', 'event_time'])

# Combine event_date and event_time into a single datetime column
df['event_datetime'] = pd.to_datetime(df['event_date'] + ' ' + df['event_time'])

# Sort values by id_employee and event_datetime
df.sort_values(by=['id_employee', 'event_datetime'], inplace=True)

# Calculate work durations
work_durations = []

for id_employee, group in df.groupby('id_employee'):
    in_time = None
    total_time = timedelta()
    
    for index, row in group.iterrows():
        if row['event_type'] == 'in':
            in_time = row['event_datetime']
        elif row['event_type'] == 'out' and in_time:
            duration = row['event_datetime'] - in_time
            work_durations.append((id_employee, in_time.date(), duration))
            in_time = None

work_df = pd.DataFrame(work_durations, columns=['id_employee', 'work_date', 'duration'])

# Calculate daily working time
daily_work = work_df.groupby(['id_employee', 'work_date']).sum().reset_index()

# Calculate weekly working time
daily_work['week'] = daily_work['work_date'].dt.isocalendar().week
weekly_work = daily_work.groupby(['id_employee', 'week']).sum().reset_index()

# Calculate monthly working time
daily_work['month'] = daily_work['work_date'].dt.to_period('M')
monthly_work = daily_work.groupby(['id_employee', 'month']).sum().reset_index()

# Calculate average working time
average_work = daily_work.groupby('id_employee')['duration'].mean().reset_index()

# Convert duration to hours for easier interpretation
average_work['average_duration_hours'] = average_work['duration'].apply(lambda x: x.total_seconds() / 3600)

print("Daily Work:")
print(daily_work)
print("\nWeekly Work:")
print(weekly_work)
print("\nMonthly Work:")
print(monthly_work)
print("\nAverage Work Duration:")
print(average_work)
