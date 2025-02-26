# Derruba os containers
# sudo docker-compose -f docker-compose.Spark.yaml -f docker-compose.Airflow.yaml down

# Builda o Spark
sudo docker build -f Dockerfile.Spark . -t spark-air

# Builda o Airflow
sudo docker build -f Dockerfile.Airflow . -t airflow-spark

# Sobe os containers
sudo docker-compose -f docker-compose.Spark.yaml -f docker-compose.Airflow.yaml up 