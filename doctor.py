import pandas as pd
df=pd.read_csv("Datasets/doctors.csv")
split_times = df['Time'].str.split('-', expand=True)

# Rename the columns
split_times.columns = ['Start Time', 'End Time']
df = pd.concat([df, split_times], axis=1)


def find_best_doctor(city, time, day, specialist):
    # Read the dataset from the CSV file
    # Assuming df is already defined
    
    # Filter the dataset based on user input criteria
    filtered_df = df[(df['Address'].str.contains(city, case=False)) &
                     (df['Day'] == day) &
                     (df['Specialty'] == specialist)]
    
    # If no doctors match the criteria, return None
    if filtered_df.empty:
        return None
    
    # Split the time range into separate rows
    filtered_df = filtered_df.assign(Time=filtered_df['Time'].str.split('-')).explode('Time')
    
    # Extract the start and end times
    time = pd.to_datetime(time).time()
    
    filtered_df['Start Time'] = pd.to_datetime(filtered_df['Start Time']).dt.time
    filtered_df['End Time'] = pd.to_datetime(filtered_df['End Time']).dt.time
    
    # Filter doctors available at the given time
    filtered_df = filtered_df[(filtered_df['Start Time'] <= time) & (filtered_df['End Time'] >= time)]

    # If no doctors are available at the given time, return None
    if filtered_df.empty:
        return None
    
    # Find the doctor with the highest user rating
    best_doctor = filtered_df.loc[filtered_df['User Rating'].idxmax()]
    
    if best_doctor is None:
        return  "No doctors found that meet all requirements."
    return best_doctor[['Name']]

# Test the function
# Cardiologist	123 Main St	Monday	09:00-17:00	
# city = 'Main St'
# time = '11:30'
# day = 'Monday'
# specialist = 'Cardiologist'
# best_doctor = find_best_doctor(city, time, day, specialist)

# if best_doctor is not None:
#     print("Best Doctor Matched:")
#     print(best_doctor)
# else:
#     print("No matching doctor found for the given criteria.")
