import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from airflow.models import Variable
from dotenv import load_dotenv

job_type = 'local' # local ou airflow

if job_type == 'airflow':
    SOURCE_HOST = Variable.get("SOURCE_HOST")
    SOURCE_USER = Variable.get("SOURCE_USER")
    SOURCE_PASSWORD = Variable.get("SOURCE_PASSWORD")
    SOURCE_SERVICE = Variable.get("SOURCE_SERVICE")
    TARGET_HOST = Variable.get("TARGET_HOST")
    TARGET_USER = Variable.get("TARGET_USER")
    TARGET_PASSWORD = Variable.get("TARGET_PASSWORD")
    TARGET_SERVICE = Variable.get("TARGET_SERVICE")
    print(f'Conectado pelo local: host: {SOURCE_HOST}, user: {SOURCE_USER}')
elif job_type == 'local':
    load_dotenv("./local.env")
    SOURCE_HOST = os.getenv("SOURCE_HOST")
    SOURCE_USER = os.getenv("SOURCE_USER")
    SOURCE_PASSWORD = os.getenv("SOURCE_PASSWORD")
    SOURCE_SERVICE = os.getenv("SOURCE_SERVICE")
    TARGET_HOST = os.getenv("TARGET_HOST")
    TARGET_USER = os.getenv("TARGET_USER")
    TARGET_PASSWORD = os.getenv("TARGET_PASSWORD")
    TARGET_SERVICE = os.getenv("TARGET_SERVICE")
    print(f'Conectado pelo airflow: host: {SOURCE_HOST}, user: {SOURCE_USER}')
else: 
    print("Credenciais não encontradas!!!")

# Nome da tabela de origem e destino
SOURCE_TABLE = "RM.PFUNC" 
TARGET_TABLE = "DW_RAW.TESTE_RM_PFUNC"  

spark = SparkSession.builder \
    .appName("Usina Moreno Spark Transfer") \
    .config("spark.jars", "/opt/bitnami/spark/jars/ojdbc17.jar") \
    .getOrCreate()
    # .config("spark.driver.extraClassPath", "/opt/bitnami/spark/jars/ojdbc17.jar") \
    # .config("spark.executor.extraClassPath", "/opt/bitnami/spark/jars/ojdbc17.jar") \
    
# Propriedades de conexão com o banco Oracle de origem
SOURCE_URL = f"jdbc:oracle:thin:@//{SOURCE_HOST}:1521/{SOURCE_SERVICE}" 
SOURCE_PROPERTIES = {
    "user": SOURCE_USER,
    "password": SOURCE_PASSWORD,
    "driver": "oracle.jdbc.driver.OracleDriver"
}

# Leitura dos dados do banco Oracle de origem
df = spark.read.format("jdbc") \
    .option("url", SOURCE_URL) \
    .option("dbtable", SOURCE_TABLE) \
    .option("user", SOURCE_PROPERTIES["user"]) \
    .option("password", SOURCE_PROPERTIES["password"]) \
    .option("driver", SOURCE_PROPERTIES["driver"]) \
    .load()

# Exibe o esquema e alguns registros para verificação
df.printSchema()
df.show(10, truncate=False)

# Aplicando transformação (exemplo: adicionando uma coluna data da carga)
transformed_df = df.withColumn("data_carga", F.current_date())

# Propriedades de conexão com o banco Oracle de destino
TARGET_URL = f"jdbc:oracle:thin:@//{TARGET_HOST}:1521/{TARGET_SERVICE}"  
TARGET_PROPERTIES = {
    "user": TARGET_USER,
    "password": TARGET_PASSWORD,
    "driver": "oracle.jdbc.driver.OracleDriver"
}

# Escrita dos dados transformados no banco Oracle de destino
transformed_df.write.format("jdbc") \
    .option("url", TARGET_URL) \
    .option("dbtable", TARGET_TABLE) \
    .option("user", TARGET_PROPERTIES["user"]) \
    .option("password", TARGET_PROPERTIES["password"]) \
    .option("driver", TARGET_PROPERTIES["driver"]) \
    .mode("overwrite") \
    .save()

# Encerra a SparkSession
spark.stop()
