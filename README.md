# Instagram Best Places

## Purpose
Find best cities, countries, restaurants, hotels, beaches and more, based on posts of the most popular Instagram’s accounts. 

## Steps
1. Fetch all posts from the most popular Instagram accounts using the API. To make the data more consistent, I targeted only french female profile. I managed to scrap `170 Instagram accounts`. Mostly TV stars, models, singers and actresses and professional instagrammers. That represents more than `202.000 posts scrapped`.
2. Filter posts to keep only the `87.000 posts with a location tagged` (43% of the posts).
3. Sort locations in a dictionary by popularity (based on the number of times one location has been tagged). I found `19.000 unique locations`.
4. Fetch information of the `4.200 most popular locations` (tagged more than 4 times) from the Instagram API. Metadata include the city and category of the location for instance.
5. Design the output. To make the information easy to read, I chose to use the CSV format. I formatted 4 files: _cities.csv_, _countries.csv_, _hotels.csv_, _restauratns.csv_ and _others.csv_.

## Outcome
[Sheets](https://docs.google.com/spreadsheets/d/1v5NAD6TRsS3Br76XNsmnkFyHj9XzDeaSU3JVa57xJFc/edit?usp=sharing)


