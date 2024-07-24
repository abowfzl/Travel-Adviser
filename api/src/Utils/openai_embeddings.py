import csv
import pandas as pd
from openai import AsyncOpenAI

client = AsyncOpenAI()


async def generate_embeddings(file_name):
    csvfile_out = open(file_name, 'w', encoding='utf8', newline='')
    fieldnames = ['attractionId', 'embedding']
    output_plot = csv.DictWriter(csvfile_out, fieldnames=fieldnames)
    output_plot.writeheader()

    attractions_df = pd.read_csv('C:/Users/Abolfazl/OneDrive/Abolfazl/OneDrive/Desktop/شهر ها/attractions.csv')

    attractions = attractions_df[['attractionId', 'city_name', 'name', 'title', 'text']]

    print(len(attractions))

    for attraction in attractions.iterrows():
        attraction = attraction[1]
        print(attraction['title'])

        text = f"{attraction['city_name']}, {attraction['name']}, {attraction['title']}: {attraction['text']}"

        embedding = await client.embeddings.create(input=[text], model="text-embedding-ada-002")
        embed = embedding["data"][0]["embedding"]

        output_plot.writerow({
            'attractionId': attraction['attractionId'],
            'embedding': embed
        })

    csvfile_out.close()


generate_embeddings('C:/Users/Abolfazl/OneDrive/Abolfazl/OneDrive/Desktop/شهر ها/attraction-embeddings.csv')
