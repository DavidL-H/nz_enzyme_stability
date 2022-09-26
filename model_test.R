# Notes and adhoc test of modeling for nz kaggle competition
dir("./data")
train_dat <- read.csv("./data/train.csv")
test_dat <- read.csv("./data/test.csv")
head(train_dat)

# Strategy
# Gather public data on the training data
# The most obvious approach is to use alphafold
# Get the closes structure in Uniprot
# Write a pipeline that pBLASTs every sequence and return top hit and
# alpha-fold.pdb


train_dat$protein_sequence[1]
