'''
This script defines some custom API functions to query EMBL-EBIs FASTA
sequence similarity search tool. This was found to be the fastest ss query option
for going from an unknown aa sequence to getting most similar protein in Uniprot.

Reference: 
"Search and sequence analysis tools services from EMBL-EBI in 2022."
https://europepmc.org/article/MED/35412617

Documentation:
https://www.ebi.ac.uk/Tools/common/tools/help/#!/Submit32job/post_run

David Lennox-Hvenekilde
221001

V2
Added function for AlphaFold2 .pdb retreival

'''
import requests


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


# Check status
def status_fasta_ss_search(jobID):
    '''
    Returns True when job is finished, else False
    '''
    URL = u'https://www.ebi.ac.uk/Tools/services/rest/fasta/status/'
    jobID_query = URL + jobID
    return requests.get(jobID_query).content == b'FINISHED'


# Return results
# Run this when the "status_fasta_ss_search" give True output
def get_plain_text_result(jobID):
    URL = u'https://www.ebi.ac.uk/Tools/services/rest/fasta/result/'+jobID+"/out"
    results_text = str(requests.get(URL).content)
    # Split by lines
    results_split = results_text.split("\\n")
    # Top hit is line 21
    return results_split[21]


# Get the Alphafold2 structure of a protein based on uniprot ID
def get_AF_pdb_from_uniprot_id(uniprotID, path):
    '''
    Download Alphafold2 structure of a protein based on uniprot ID to given path
    Adapted from: # https://www.blopig.com/blog/2022/08/retrieving-alphafold-models-from-alphafolddb/
    '''
    database_version = "v2"
    alphafold_ID = 'AF-'+uniprotID+'-F1'
    database_version = "v2"
    model_url = f'https://alphafold.ebi.ac.uk/files/{alphafold_ID}-model_{database_version}.pdb'
    response = requests.get(model_url)
    if str(response) == '<Response [200]>':
        open(path+alphafold_ID+".pdb", "wb").write(response.content)
    return response

