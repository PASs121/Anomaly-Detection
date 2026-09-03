import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('data/Water_Heater/Water_Heater_1/Normal/water_heater_1_day1.csv')

# Display the first few rows of the dataset
print(data.head())


# Convert the timestamp column to datetime format
data['Time'] = pd.to_datetime(data['ctime'])

# Set the timestamp column as the index
data.set_index('Time', inplace=True)
print(data.tail())
# Display summary statistics
print(data.describe())

plt.figure(figsize=(10, 6))
plt.plot(data.index , data.activePower , label='Power Consumption')
plt.xlabel('Time')
plt.ylabel('Power Consumption')
plt.legend()
plt.show()