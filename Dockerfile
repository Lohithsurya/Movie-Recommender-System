FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN apt-get update
RUN ls -R ./movies
CMD ["python", "movie_recommender_system.py"]
