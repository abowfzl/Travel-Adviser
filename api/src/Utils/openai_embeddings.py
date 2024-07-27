import csv
import pandas as pd
from openai import OpenAI

client = OpenAI()


def is_invalid_text(value):
    return pd.isna(value) or value is None or value.strip() == ''


def generate_embeddings(file_name):
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

        if is_invalid_text(attraction['text']):
            continue

        attraction['text'] = (attraction['text'][:7500] + '..') if len(attraction['text']) > 7500 else attraction['text']

        text = f"جاذبه گردشگری در شهر {attraction['city_name']} به نام {attraction['name']}. عنوان: {attraction['title']}. توضیحات: {attraction['text']}. این مکان یکی از بهترین جاهای دیدنی و تفریحی در {attraction['city_name']} است و می‌تواند گزینه مناسبی برای سفر شما باشد."

        embedding = client.embeddings.create(input=[text], model="text-embedding-ada-002",)
        embed = embedding.data[0].embedding

        output_plot.writerow({
            'attractionId': attraction['attractionId'],
            'embedding': embed
        })

    csvfile_out.close()


generate_embeddings('C:/Users/Abolfazl/OneDrive/Abolfazl/OneDrive/Desktop/Cities/attraction-embeddings-openai.csv')
