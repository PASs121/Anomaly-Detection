import libs.stream as strm

stream = strm.DataStream('data/Water_Heater/Water_Heater_1/Normal/water_heater_1_day2.csv')

while True:
    try:
        reading = stream.next_reading
        print(reading)
    except StopIteration:
        print("Data stream has been exhausted.")
        break
