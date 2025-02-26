sudo docker build -f Dockerfile.Spark . -t spark-air
sudo docker build -f Dockerfile.Airflow . -t airflow-spark

mkdir ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

sudo docker-compose -f docker-compose.Spark.yaml -f docker-compose.Airflow.yaml up -d



sudo docker exec -it 
  docker-spark-airflow-spark-worker-1 
  spark-submit   
  --master spark://b6328bd59653:7077 
  --jars /opt/moreno-spark/jars/ojdbc8.jar   
  --driver-class-path /opt/spark/jars/ojdbc8.jar   
  arquivo.py




spark_default {
  "queue": "root.default",
  "deploy_mode": "cluster",
  "spark_home": "/opt/bitnami/",
  "spark_binary": "spark-submit",
  "namespace": "default"
}


source_host = "cem-db-scan.grupomoreno.intranet"
source_user = "bi_moreno_risti"
source_password = "BIr1st!@2025"
source_service = "dbcem"

target_host = "cem-db-stby.grupomoreno.intranet"
target_user = "DW"
target_password = "kL0i:c3HzP+"
target_service = "dwcem"

