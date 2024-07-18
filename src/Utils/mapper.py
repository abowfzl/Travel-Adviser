import pandas as pd

# Load the CSV files into dataframes
attractions_df = pd.read_csv('C:/Users/Abolfazl/OneDrive/Abolfazl/OneDrive/Desktop/شهر ها/attractions.csv')

cities_df = pd.read_csv('C:/Users/Abolfazl/OneDrive/Abolfazl/OneDrive/Desktop/شهر ها//Cities.csv')
attractions_df['attractionId'] = range(1, len(attractions_df) + 1)
attractions_df.to_csv('C:/Users/Abolfazl/OneDrive/Abolfazl/OneDrive/Desktop/شهر ها/attractions.csv', index=False)

# Merge the dataframes on the shared columns
merged_df = pd.merge(attractions_df, cities_df, left_on='city_name', right_on='Name')

# Create the resulting dataframe with attractionId and cityId columns
result_df = merged_df[['attractionId', 'cityId']]

# Save the resulting dataframe to a new Excel file
result_df.to_csv('C:/Users/Abolfazl/OneDrive/Abolfazl/OneDrive/Desktop/شهر ها/attraction_city_connections.csv', index=False)
