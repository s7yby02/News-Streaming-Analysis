from pyspark.sql import SparkSession
import logging

def createSparkSession():
    s_coon = None

    try:
        SparkSession.builder.appName("pfa Spark")\
            .config('spark.jars.packages',"org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.1")\
            .getOrCreate()
        
        logging.info("Spark Session created Successfully!!!!!")
    except Exception as e:
        logging.error(f"Couldn't create the spark session due to exception {e}")

    return s_coon

if __name__ == '__main__':

    s_conn = createSparkSession()
    