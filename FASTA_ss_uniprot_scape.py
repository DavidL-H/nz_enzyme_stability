"""
Use the FASTA sequence similarity search API to query with nz protein stability test data aa sequences.
The data will be saved as a txt file, with the protein ids given in the test data as the keys, and the output from
the ss seach as the results/values. The idea is that we want a uniprot entru associated with each of the 
sequences in the test data set, to use for gathering AlphaFold structures down the line.
"""

import FASTA_ss_search as fas
import time
test_seq = "AAAAKAAALALLGEAPEVVDIWLPAGWRQPFRVFRLERKGDGVLVGMIKDAGDDPDVTHGAEIQAFVRFASEDRLEGGEGVGVVTKPGLGVPVGEPAINPVPRRMIWEAVREVTERPLAVTIAIPGGEELAKKTLNPRLGILGGLSVLGTTGVVKPYSTSAFRMSVVQAVGVARANGLLEIAATTGGKSERFAQRLLPHLPEMAFIEMGDFVGDVLRAARKVGVEVVRVVGMIGKISKMADGKTMTHAAGGEVNLSLLLSLLKEAGASPKALKEAEGAATARRFLEIALEEGLELFFVNLVRLAQEKLQAYIGERPFVSVALTDFDEGRCLAAWPDREVYR"

jobID = fas.post_fasta_ss_search(fas.aaseq_to_request_string(test_seq, "test_title"))

# Wait til job is done, before getting results
while not fas.status_fasta_ss_search(jobID):
    print(jobID + " still running. Waiting 2 seconds")
    time.sleep(2)
print("Job done, getting results")
print(get_plain_text_result(jobID))