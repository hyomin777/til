from datasets import load_dataset

data_files = {"train": "drugsComTrain_raw.tsv", "test": "drugsComTest_raw.tsv"}
# \t is the tab character in Python
drug_dataset = load_dataset("csv", data_files=data_files, delimiter="\t")

# to verify that the number of IDs matches the number of rows in each split
for split in drug_dataset.keys():
    assert len(drug_dataset[split]) == len(drug_dataset[split].unique("Unnamed: 0"))

# We can use the DatasetDict.rename_column() function to rename the column across both splits in one go
drug_dataset = drug_dataset.rename_column(
    original_column_name="Unnamed: 0", new_column_name="patient_id"
)


# To normalize all the condition labels
def lowercase_condition(example):
    return {"condition": example["condition"].lower()}

# normalize
drug_dataset = drug_dataset.filter(lambda x: x['condition'] is not None)
drug_dataset = drug_dataset.map(lowercase_condition)
print(f"Check that lowercasing worked: \n {drug_dataset["train"]["condition"][:3]} \n")


def compute_review_length(example):
    return {"review_length": len(example["review"].split())}

drug_dataset = drug_dataset.map(compute_review_length)
print(f"Insepct the first training example: \n {drug_dataset["train"][0]} \n")


# remove reviews that contain fewer than 30 words
drug_dataset = drug_dataset.filter(lambda x: x["review_length"] > 30)
print(drug_dataset.num_rows)


# use Dataset.map() to unescape all the HTML characters in our corpus
import html
drug_dataset = drug_dataset.map(lambda x: {"review": html.unescape(x["review"])})

'''
When you specify batched=True the function receives a dictionary with the fields of the dataset, but each value is now a list of values, and not just a single value.
The return value of Dataset.map() should be the same: a dictionary with the fields we want to update or add to our dataset, and a list of values.
For example, here is another way to unescape all HTML characters, but using batched=True:
'''
new_drug_dataset = drug_dataset.map(
    lambda x: {"review": [html.unescape(o) for o in x["review"]]}, batched=True
)

from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

def tokenize_and_split(examples):
    result = tokenizer(
        examples["review"],
        truncation=True,
        max_length=128,
        return_overflowing_tokens=True,
    )
    # Extract mapping between new and old indices
    sample_map = result.pop("overflow_to_sample_mapping")
    for key, values in examples.items():
        result[key] = [values[i] for i in sample_map]
    return result

tokenized_dataset = drug_dataset.map(tokenize_and_split, batched=True)


# convert dataset to Pandas
drug_dataset.set_format("pandas")
print(drug_dataset["train"][:3])

train_df = drug_dataset["train"][:]

frequencies = (
    train_df["condition"]
    .value_counts()
    .to_frame()
    .reset_index()
    .rename(columns={"index": "condition", "count": "frequency"})
)
print(frequencies.head())

# we can always create a new Dataset object by using the Dataset.from_pandas() function
from datasets import Dataset
freq_dataset = Dataset.from_pandas(frequencies)
print(freq_dataset)


# reset the output format of drug_dataset from "pandas" to "arrow"
drug_dataset.reset_format()

# create a validation set
drug_dataset_clean = drug_dataset["train"].train_test_split(train_size=0.8, seed=42)
# Rename the default "test" split to "validation"
drug_dataset_clean["validation"] = drug_dataset_clean.pop("test")
# Add the "test" set to our `DatasetDict`
drug_dataset_clean["test"] = drug_dataset["test"]


'''
when you'll want to save a dataset to disk.
Datasets provides three main functions to save your dataset in different format
Arrow: Dataset.save_to_disk()
Csv: Dataset.to_csv()
Json: Dataset.to_json()
'''
# drug_dataset_clean.save_to_disk("drug-reviews")