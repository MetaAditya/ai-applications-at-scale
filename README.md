How to use this Repo..

1) Log in to Hugging face and get yout HF_token.
2) **Download the data**:Paste the token inside download_dataset.py and run it , this downloads the data in parquet to your disk
3) **Create the database and table in postgres**In your postgres execute the following commands

    CREATE DATABASE vector_search;
   
   \c vector_search;
   
   CREATE EXTENSION IF NOT EXISTS vector;
   
   CREATE TABLE IF NOT EXISTS wikipedia_embeddings (
    id BIGSERIAL PRIMARY KEY,
    wiki_id INT,
    url TEXT,
    title TEXT,
    text TEXT,
    emb vector(1024)
);

4) **Ingest data to postgres**Run the jupyter notebook ingestData.ipynb , this will sink the the parquet data to postgres.
5) Run/Observe the notebook IndexComparison.ipynb for comparison.
