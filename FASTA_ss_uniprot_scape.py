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
train_df['fasta_ss_search_result'] = pd.NA

# Test
for n in range(len(train_df)):
    test_seq = train_df["protein_sequence"][n]
    jobID = fas.post_fasta_ss_search(fas.aaseq_to_request_string(test_seq, "test_title"))
    # Wait til job is done, before getting results
    while not fas.status_fasta_ss_search(jobID):
        print(jobID + " still running. Waiting 2 seconds")
        time.sleep(2)
    print("Job done, getting results")
    train_df['fasta_ss_search_result'][n] = fas.get_plain_text_result(jobID)
    # Save results
    train_df.to_csv("./data/train_updated_uniprot_ss_search.csv")




# For later
# Extract key data from ss search
'''
train_df["uniprot_id"][n] = job_result[0]
train_df["protein_id"][n]  = job_result[1]
if len(job_result) > 7:
    train_df["protein_name"][n] = " ".join(job_result[2:(len(job_result)-5)])
else:
    train_df["protein_name"][n] = job_result[2]
train_df["e_val"][n] = float(job_result[-1])
train_df["score_bits"][n] = float(job_result[-2])
train_df["not_sure"][n] = int(job_result[-3])
train_df['length'][0] = int(job_result[-4][:-1])
'''

