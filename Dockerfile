FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y unzip && \
    unzip movies.zip -d ./movies
RUN ls -R ./movies
CMD ["python", "movie_recommender_system.py"]
