#!/bin/bash
sudo docker exec -it spark-master spark-submit --master spark://spark-master:7077 --jars /opt/bitnami/spark/jars/ojdbc17.jar "$@"
