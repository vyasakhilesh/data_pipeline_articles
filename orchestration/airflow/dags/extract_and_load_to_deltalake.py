import argparse
import pyspark
from delta import *
import zipfile
import os
import shutil
import time

# Function to extract JSON files from a large zipped file
def extract_json_from_zip(zip_file_path, extract_to_folder):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_folder)

# Function to find all JSON files in directory and subdirectories
def find_json_files(directory):
    json_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files

def main(zip_file_path, extract_to_folder, delta_table_path):
    start_time = time.time()  # Start timing
    # Initialize Spark session
    builder = pyspark.sql.SparkSession.builder.appName("Extract_Load") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

    spark = configure_spark_with_delta_pip(builder).getOrCreate()

    # Extract JSON files
    extract_json_from_zip(zip_file_path, extract_to_folder)

    # Load JSON files into a DataFrame
    # Function to find all JSON files in directory and subdirectories
    # Find all JSON files in directory and subdirectories
    json_files = find_json_files(extract_to_folder)
    # print('###################################',json_files[0:10])
    df = spark.read.format('json').load(json_files)
    
    # Check if the Delta table exists
    if DeltaTable.isDeltaTable(spark, delta_table_path):
        # Read existing data from Delta Lake
        existing_df = spark.read.format("delta").load(delta_table_path)

        # Merge new data into existing data using incremental updates
        merged_df = existing_df.unionByName(df).dropDuplicates()

        # Write merged data back to Delta Lake
        merged_df.write.format("delta").mode("overwrite").save(delta_table_path)
    else:
        # If the Delta table does not exist, write the new data to Delta Lake
        df.write.format("delta").mode("overwrite").save(delta_table_path)

    # Stop the Spark session
    spark.stop()

    # Optional: Clean up extracted files if no longer needed
    shutil.rmtree(extract_to_folder)
    end_time = time.time()  # End timing
    elapsed_time = end_time - start_time
    print(f"Script executed in {elapsed_time} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract JSON from zip and incrementally load into Delta Lake")
    parser.add_argument("zip_file_path", help="Path to the zipped file")
    parser.add_argument("extract_to_folder", help="Folder to extract JSON files")
    parser.add_argument("delta_table_path", help="Delta Lake table path")

    # args = parser.parse_args()

    # main(args.zip_file_path, args.extract_to_folder, args.delta_table_path)
    main("/opt/spark/data/raw_data/sample_data/resync_datadump_sample220218.zip",
         "/opt/spark/data/raw_data/sample_data/resync_datadump_sample220218/", 
         "/opt/spark/data/delta_table/core_data")