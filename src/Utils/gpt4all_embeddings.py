import csv
import os

import pandas as pd
from neo4j import GraphDatabase
from nomic import embed


def get_movie_plots(limit=None):
    driver = GraphDatabase.driver(
        os.getenv('NEO4J_URI'),
        auth=(os.getenv('NEO4J_USERNAME'), os.getenv('NEO4J_PASSWORD'))
    )

    driver.verify_connectivity()

    query = """MATCH (m:Movie) WHERE m.plot IS NOT NULL
    RETURN m.movieId AS movieId, m.title AS title, m.plot AS plot"""

    if limit is not None:
        query += f' LIMIT {limit}'

    movies, summary, keys = driver.execute_query(
        query
    )

    driver.close()

    return movies


def generate_embeddings(file_name, limit=None):
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

        embeddings = embed.text([text], model="nomic-embed-text-v1.5", inference_mode="local")['embeddings']

        output_plot.writerow({
            'attractionId': attraction['attractionId'],
            'embedding': embeddings[0]
        })

    csvfile_out.close()


generate_embeddings('C:/Users/Abolfazl/OneDrive/Abolfazl/OneDrive/Desktop/شهر ها/attraction-embeddings.csv')
