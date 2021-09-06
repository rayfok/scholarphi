import os
import json

input_dir = "src/data"

merged = {}
for data_e in os.scandir(input_dir):
    id = os.path.splitext(data_e.name)[0]

    if id == "skimmingData":
        continue

    with open(data_e.path, "r") as f:
        merged[id] = json.load(f)

with open(f"{input_dir}/skimmingData.json", "w") as out:
    json.dump(merged, out, indent=2)
