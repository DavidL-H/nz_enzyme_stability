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

def clean_and_find_wt(final_train_df):
    # Clean it up a bit
    final_train_df.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1, inplace=True)
    final_train_df = final_train_df[final_train_df["af_pdb_status"] == 1.0]
    # Need to extract the E-val (last word in ss query)
    final_train_df["e_val"] = final_train_df["fasta_ss_search_result"].str.split().str[-1]

    # Check all uniprot IDs for the wt (lowest e-val)
    # Check that there are at least 5 mutants of the wt (with same uniprot it)
    # Otherwise remove
    # Assign the version with lowest e-val as the wt. Not necessarily a true WT
    is_wt = pd.Series(["e_val"],dtype=bool)
    for upid in final_train_df["uniprot_id"].unique():
        final_train_df_sub = final_train_df[final_train_df["uniprot_id"] == upid]
        if len(final_train_df_sub) < 5:
            final_train_df = final_train_df[final_train_df["uniprot_id"] != upid]
        else:
            is_wt = is_wt.append(final_train_df_sub["e_val"] == final_train_df_sub["e_val"].min())

    # Using the 5 or over per enzyme/protein cutoff, we have reduced the training data to 3588 protein sequences of 137 proteins
    is_wt.drop(is_wt.index[0],inplace=True) 
    len(is_wt)
    len(final_train_df)
    len(final_train_df["uniprot_id"].unique())

    final_train_df["is_wt"] = is_wt
    final_train_df.to_csv("./data/221115_train_subset.csv")
    return final_train_df.head

# Find differences in sequence between WT and between mutants
###############################################################
# https://towardsdatascience.com/pairwise-sequence-alignment-using-biopython-d1a9d0ba861f

# Doesn't quite work...
from Bio import pairwise2
from Bio.Align import substitution_matrices
from Bio.pairwise2 import format_alignment

matrix = substitution_matrices.load("BLOSUM62")
train_reduced = pd.read_csv("./data/221115_train_subset.csv")

seq1 = train_reduced["protein_sequence"][0]
seq2 = train_reduced["protein_sequence"][1]
alng = pairwise2.align.globaldx(seq1, seq2, matrix)

for a in alng:
    print(format_alignment(*a))


# USE PYMOL TO DO MUTAGENESIS
# NEED TO USE PYMOL VENV
#https://sourceforge.net/p/pymol/mailman/message/11671708/
import pymol
import sys
pdb, selection, mutant = sys.argv[-3:]
pymol.cmd.wizard("mutagenesis")
pymol.cmd.fetch(pdb)
pymol.cmd.refresh_wizard()
pymol.cmd.get_wizard().do_select(selection)
pymol.cmd.get_wizard().set_mode(mutant)
pymol.cmd.get_wizard().apply()
pymol.cmd.set_wizard()
pymol.cmd.save("%s_m.pdb" % pdb, pdb)