# nz_enzyme_stability
![Kaggle](https://img.shields.io/badge/Kaggle-035a7d?style=for-the-badge&logo=kaggle&logoColor=white)  
https://www.kaggle.com/competitions/novozymes-enzyme-stability-prediction  

The training data is a collection of publically available protein sequences and associated Tm (temperature stability). There represent a wide array of proteins
which vary widely in structure, function, sequence etc. However the prediction data is just ONE protein with different point mutations and deletion.
The training data seems to not be really generally applicable to the test data. To get good predictions for the test data, the model will have to be significantly over-fitted
for the specific enzyme in question (nz's protease).

**General strategy outline - Data gathering, and wrangling:**  
Step 1
 - Blast protein sequences of training data against UniProt
 - Fetch AlphaFold .pdb structure based on UniProt ID
 - Group training data by enzyme (save best BLAST hit/AlphaFold structure)
 
DONE

Step 2  
 - ID the wt enzyme/protein in each group
 - Find single mutations deletion in these groups
 - Make derivatives of the .pdb file of the WT, using pymol mutagenesis wizard
 - Transform 3d structures into 2d images: contact maps
 - Transform 3d structures into graphs: residue interaction networks

**General strategy outline - Modelling: **  
 Step 1  
  - Try out CNNs on a combination of 2d images and graphs
 
