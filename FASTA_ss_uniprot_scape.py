"""
Use the FASTA sequence similarity search API to query with nz protein stability test data aa sequences.
The data will be saved as a txt file, with the protein ids given in the test data as the keys, and the output from
the ss seach as the results/values. The idea is that we want a uniprot entru associated with each of the 
sequences in the test data set, to use for gathering AlphaFold structures down the line.

David Lennox-Hvenekilde
221001
"""
import FASTA_ss_search as fas
import time
import pandas as pd

# Impor the updated dataset.
train_df = pd.read_csv("./data/train_updated.csv")
train_df.head()

# Add new columns
train_df['uniprot_id'] = pd.NA
train_df['protein_id'] = pd.NA
train_df['protein_name'] = pd.NA
train_df['length'] = pd.NA
train_df['not_sure'] = pd.NA
train_df['score_bits'] = pd.NA
train_df['e_val'] = pd.NA

# Test
test_seq = train_df["protein_sequence"][0]
jobID = fas.post_fasta_ss_search(fas.aaseq_to_request_string(test_seq, "test_title"))
# Wait til job is done, before getting results
while not fas.status_fasta_ss_search(jobID):
    print(jobID + " still running. Waiting 2 seconds")
    time.sleep(2)
print("Job done, getting results")
job_result_string = fas.get_plain_text_result(jobID)
job_result = job_result_string.split(" ")

# Extract key data from ss search
uniprot_id = job_result[0]
protein_id = job_result[1]
if len(job_result) > 7:
    protein_name = " ".join(job_result[2:(len(job_result)-5)])
else:
    protein_name = job_result[2]
e_val = float(job_result[-1])
score_bits = float(job_result[-2])
not_sure = int(job_result[-3])
length = int(job_result[-4][:-1])


train_df.to_csv("./data/train_updated_unirpto_ss_search.csv")