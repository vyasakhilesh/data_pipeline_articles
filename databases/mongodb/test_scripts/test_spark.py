from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MongoDB Spark Connector Example") \
    .config("spark.mongodb.uri", "mongodb://mongoadmin:password@localhost:27017/test_db.test_collection") \
    .getOrCreate()

dataFrame = spark.read\
                 .format("mongodb")\
                 .option("database", "test_db")\
                 .option("collection", "test_collection")\
                 .load()
                 
print(dataFrame.printSchema())

print(dataFrame.show())