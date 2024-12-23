FROM python:3.10
WORKDIR /app
COPY . /app
RUN apt-get update
RUN apt-get install -y unzip
RUN unzip movies.zip -d ./movies
RUN ls -R ./movies
CMD ["python", "movie_recommender_system.py"]
