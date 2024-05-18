from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr

def createSparkSession():
    s_conn = None

    try:
        s_conn = SparkSession.builder.appName("pfa Spark")\
            .config('spark.jars.packages',"org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
            .getOrCreate()
        # s_conn.sparkContext.setLogLevel("WARN")
        print("GOAAAAAAAAAAAAAAAAAAAAAAAAAL\nSpark Session Created")
    except Exception as e:
        print("TFUUUUUUUUUUUUUUUUUUU")

    return s_conn

def createKafkaSession(spark_session):
    spark_df = None
    try:
        spark_df = spark_session.readStream \
            .format('kafka') \
            .option('kafka.bootstrap.servers', 'localhost:9092') \
            .option('subscribe', 'captions') \
            .option('startingOffsets', 'earliest')\
            .load()
        print("kafka dataframe created successfully")
    except Exception as e:
        print(f"kafka dataframe could not be created because: {e}")

    return spark_df


if __name__ == '__main__':

    s_conn = createSparkSession()
    print(s_conn)

    if s_conn:
        print("Spark session is active")
        k_conn = createKafkaSession(s_conn)
        
        if k_conn:
            print("Kafka connection is active")

            k_conn = k_conn.selectExpr("CAST(value AS STRING)")
            print("data is read!!!!!!!!!!!!!")

            processed_df = k_conn.withColumn("value", expr("upper(value)"))  # Example transformation
            print("Data is processed!!!!!!!!!!!!!!!!!!!!!!")
            # Write the stream to the console (or any other sink)
            query = processed_df.writeStream \
                .outputMode("append") \
                .format("console") \
                .start()
            print("QUERYYYYYYYYY DOOONE")
            query.awaitTermination()

