import gc
from datasets import load_dataset
import pyarrow as pa
import pyarrow.parquet as pq

# Replace with your Hugging Face token
HF_TOKEN = "<your HF token>"

# Pass token to authenticate the stream
ds = load_dataset(
    "CohereLabs/wikipedia-2023-11-embed-multilingual-v3",
    "en",
    split="train",
    streaming=True,
    token=HF_TOKEN
)

TARGET_ROWS = 1_000_000
BATCH_SIZE = 50_000
OUTPUT_FILE = "cohere_wikipedia_en_1M.parquet"

batch_data = []
writer = None

print("Streaming 1 million rows with authentication...")

for idx, row in enumerate(ds):
    batch_data.append(row)

    # Save every 50,000 rows
    if len(batch_data) == BATCH_SIZE or (idx + 1) == TARGET_ROWS:
        print(f"Saving batch: rows {idx - len(batch_data) + 1:,} to {idx + 1:,}...")

        table = pa.Table.from_pylist(batch_data)

        if writer is None:
            writer = pq.ParquetWriter(OUTPUT_FILE, table.schema, compression="snappy")

        writer.write_table(table)

        # Clear batch from memory
        batch_data = []
        del table
        gc.collect()

    if idx + 1 >= TARGET_ROWS:
        break

if writer:
    writer.close()

print(f"Successfully written {TARGET_ROWS:,} rows to '{OUTPUT_FILE}'.")



