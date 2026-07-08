import pandas as pd
import os

DATA_FOLDER = "data"

files = [
    "technical.csv",
    "behavioral.csv",
    "system_design.csv",
    "hr.csv",
    "ai_ml.csv",
    "ai_ml_unique.csv",
]

all_data = []

for file in files:
    path = os.path.join(DATA_FOLDER, file)

    print(f"Reading {file}...")

    df = pd.read_csv(path)

    all_data.append(df)

merged = pd.concat(all_data, ignore_index=True)

# Remove duplicate questions if any
merged.drop_duplicates(subset=["Question"], inplace=True)

# Shuffle rows
merged = merged.sample(frac=1, random_state=42).reset_index(drop=True)

output = os.path.join(DATA_FOLDER, "interview_question_bank.csv")

merged.to_csv(output, index=False)

print()
print("=====================================")
print("Merged Successfully!")
print(f"Total Questions : {len(merged)}")
print(f"Saved to : {output}")
print("=====================================")