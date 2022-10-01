'''
This script used the training set for nz thermostability kaggle competition
Here we gather the 3d structure data for each sequence in the training data (~30 000)
This is done by blast querying Uniprot (trembl/swiss-prot) with the API of EMBL-EBI for each
sequence, extracting the top hit, and getting the AlphaFold structure of said hit.
 
This may take a while for 30 000 structures... Let's see

Reference: 
"Search and sequence analysis tools services from EMBL-EBI in 2022."
https://europepmc.org/article/MED/35412617

Documentation:
https://www.ebi.ac.uk/Tools/common/tools/help/#!/Submit32job/post_run

David Lennox-Hvenekilde
221001
'''

import requests
import os

# Where to save scraped 3d structure data
root = "./data/AF_scaped_data"
test_seq = "AAAAKAAALALLGEAPEVVDIWLPAGWRQPFRVFRLERKGDGVLVGMIKDAGDDPDVTHGAEIQAFVRFASEDRLEGGEGVGVVTKPGLGVPVGEPAINPVPRRMIWEAVREVTERPLAVTIAIPGGEELAKKTLNPRLGILGGLSVLGTTGVVKPYSTSAFRMSVVQAVGVARANGLLEIAATTGGKSERFAQRLLPHLPEMAFIEMGDFVGDVLRAARKVGVEVVRVVGMIGKISKMADGKTMTHAAGGEVNLSLLLSLLKEAGASPKALKEAEGAATARRFLEIALEEGLELFFVNLVRLAQEKLQAYIGERPFVSVALTDFDEGRCLAAWPDREVYR"

# Request string needed for FASTA sequence similarity query job
# Not the most beutiful API wrapper, but does the job
def aaseq_to_request_string(sequence, title, email = "davidlh3@gmail.com"):
    '''
    This function takes an AA sequence and job title as input.
    Converts it to a formatted string which can be used for POSTing a fasta ss search request.
    Basically translates to unicode and concetanates everything.
    '''
    request_string = "email="+ email.replace("@","%40") + "&"
    request_string = request_string + "title="+title+"&program=fasta&stype=protein&"
    request_string = request_string + "sequence=" + sequence
    request_string = request_string + '&database=uniprotkb_swissprot'

    return request_string

request_string = aaseq_to_request_string(test_seq, "a test ss search")

# POST a sequence similarity search
def post_fasta_ss_search(request_string):
    URL = u'https://www.ebi.ac.uk/Tools/services/rest/fasta/run'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/plain'
    }
    response = requests.post(URL, headers=headers, data=request_string)
    # Returns only jobID
    return str(response.content)[2:-1]

# The job is now posted

jobID = post_fasta_ss_search(request_string)


def status_fasta_ss_search(jobID):
    '''
    Returns True when job is finished, else False
    '''
    URL = u'https://www.ebi.ac.uk/Tools/services/rest/fasta/status/'
    jobID_query = URL + jobID
    return requests.get(jobID_query).content == b'FINISHED'

status_fasta_ss_search(jobID)




"""
POST a FASTA job
https://www.ebi.ac.uk/Tools/services/rest/fasta/run
curl -X POST --header 'Content-Type: application/x-www-form-urlencoded' --header 'Accept: text/plain' -d 'email=davidlh3%40gmail.com&title=TestTitle&program=fasta&stype=protein&sequence=AAAAKAAALALLGEAPEVVDIWLPAGWRQPFRVFRLERKGDGVLVGMIKDAGDDPDVTHGAEIQAFVRFASEDRLEGGEGVGVVTKPGLGVPVGEPAINPVPRRMIWEAVREVTERPLAVTIAIPGGEELAKKTLNPRLGILGGLSVLGTTGVVKPYSTSAFRMSVVQAVGVARANGLLEIAATTGGKSERFAQRLLPHLPEMAFIEMGDFVGDVLRAARKVGVEVVRVVGMIGKISKMADGKTMTHAAGGEVNLSLLLSLLKEAGASPKALKEAEGAATARRFLEIALEEGLELFFVNLVRLAQEKLQAYIGERPFVSVALTDFDEGRCLAAWPDREVYR&database=uniprotkb_swissprot' 'https://www.ebi.ac.uk/Tools/services/rest/fasta/run'
response fasta-R20221001-105833-0261-53038124-p1m
"""