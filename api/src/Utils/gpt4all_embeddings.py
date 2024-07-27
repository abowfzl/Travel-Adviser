import csv
import pandas as pd
from nomic import embed


def generate_embeddings(file_name, limit=None):
    csvfile_out = open(file_name, 'w', encoding='utf8', newline='')
    fieldnames = ['attractionId', 'embedding']
    output_plot = csv.DictWriter(csvfile_out, fieldnames=fieldnames)
    output_plot.writeheader()

    attractions_df = pd.read_csv('C:/Users/Abolfazl/OneDrive/Abolfazl/OneDrive/Desktop/Cities/attractions.csv')

    attractions = attractions_df[['attractionId', 'city_name', 'name', 'title', 'text']]

    print(len(attractions))

    for attraction in attractions.iterrows():
        attraction = attraction[1]
        print(attraction['title'])

        text = f"{attraction['city_name']}, {attraction['name']}, {attraction['title']}: {attraction['text']}"

        embeddings = embed.text([text], model="nomic-embed-text-v1.5", inference_mode="local")['embeddings']

        output_plot.writerow({
            'attractionId': attraction['attractionId'],
            'embedding': embeddings[0]
        })

    csvfile_out.close()


generate_embeddings('C:/Users/Abolfazl/OneDrive/Abolfazl/OneDrive/Desktop/Cities/attraction-embeddings.csv')
