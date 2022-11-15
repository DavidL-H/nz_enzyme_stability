'''
We now have an extended dataframe which contains protein sequences, pH and their Tm (thermostability) value
Aditionally, we now have columns that describe best uniprot hit and the corresponding AlphaFold structure (.pdb)
is available in the './data/alphafold/' folder. The next step is to identify the groups of proteins and their
respective WT sequences. Then identify sequences in the clusters with single point mutations/deletions compared to the WT.
These will serve as the best training data for the test case we have. We can generate individual mutant 3d structures for 
relevant sequences using the pymol mutagenisis wizard.

David
221114
'''
# Read it in
import pandas as pd
import re
final_train_df = pd.read_csv("./data/train_updated_uniprot_ss_search_pdb.csv")

# Clean it up a bit
final_train_df.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1, inplace=True)
final_train_df = final_train_df[final_train_df["af_pdb_status"] == 1.0]
# Need to extract the E-val (last word in ss query)
final_train_df["e_val"] = final_train_df["fasta_ss_search_result"].str.split().str[-1]


# lets group by the AF/uniprot ID
#final_train_df.set_index(['uniprot_id', 'seq_id'], inplace=True)

final_train_df.head

# Check all uniprot IDs for the wt (lowest e-val)
# Check that there are at least 5 mutants of the wt (with same uniprot it)
# Otherwise remove
final_train_df = final_train_df[final_train_df["e_val"] != "YqzM"] # Issue for 'pd.astype(float)'
final_train_df["e_val"] = final_train_df["e_val"].astype(float)

is_wt = pd.Series(["e_val"],dtype=bool)
i = 0
for upid in final_train_df["uniprot_id"].unique():
    final_train_df_sub = final_train_df[final_train_df["uniprot_id"] == upid]
    if len(final_train_df_sub) < 5:
        final_train_df = final_train_df[final_train_df["uniprot_id"] != upid]
    else:
        #final_train_df_sub["wt_protein"] = final_train_df_sub["e_val"] == final_train_df_sub["e_val"].min()
        #print(final_train_df_sub)
        #print(final_train_df_sub["e_val"] == final_train_df_sub["e_val"].min())
        #print(final_train_df_sub)
        is_wt = is_wt.append(final_train_df_sub["e_val"] == final_train_df_sub["e_val"].min())

is_wt


# Using the 5 or over per enzyme/protein cutoff, we have reduced the training data to 3588 protein sequences of 137 proteins
is_wt.drop(is_wt.index[0],inplace=True) 
len(is_wt)
len(final_train_df)
len(final_train_df["uniprot_id"].unique())


final_train_df["is_wt"] = is_wt
final_train_df.to_csv("./data/221115_train_subset.csv")