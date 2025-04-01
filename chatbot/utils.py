# chatbot/utils.py
from hyperon import MeTTa
import os

# Initialize MeTTa instance
metta = MeTTa()

# Load the MeTTa data file (adjust path if needed)
data_file_path = os.path.join(os.path.dirname(__file__), 'data.metta')
with open(data_file_path, 'r') as file:
    metta.run(file.read())

def caused_by(disease):
    """
    Runs the MeTTa query !(causedBy <disease> ) to find causes of a disease.
    Input:
        disease (str): The disease name (e.g., "Typoiad").
    Returns:
        List of MeTTa query results (causes).
    """
    query = f"!(causedBy {disease} )"
    return metta.run(query)

def find_parasite(disease):
    """
    Runs the MeTTa query !(findParasite <disease> ) to find parasite-related info.
    Input:
        disease (str): The disease name (e.g., "Typoiad").
    Returns:
        List of MeTTa query results (parasite info).
    """
    query = f"!(findParasite {disease} )"
    return metta.run(query)

def get_disease_and_correlated_disease(person):
    """
    Runs the MeTTa query !(getDiseaseAndCorrelatedDisease <person> ) to find diseases and their correlations for a person.
    Input:
        person (str): The person’s name (e.g., "Bisrat").
    Returns:
        List of MeTTa query results (disease and correlated disease pairs).
    """
    query = f"!(getDiseaseAndCorrelatedDisease {person} )"
    return metta.run(query)

def find_disease_from_vulnerability(vulnerability):
    """
    Runs the MeTTa query !(findDisreaseFromVulnerability <vulnerability> ) to find diseases linked to a vulnerability.
    Input:
        vulnerability (str): The vulnerability condition (e.g., "lowImmuneSystem").
    Returns:
        List of MeTTa query results (diseases).
    """
    query = f"!(findDisreaseFromVulnerability {vulnerability} )"  # Note: "Disrease" seems to be a typo; adjust if meant "Disease"
    return metta.run(query)

def find_all_users():
    """
    Runs the MeTTa query !(findAllUsers ) to find all users in the dataset.
    No input required.
    Returns:
        List of MeTTa query results (users).
    """
    query = "!(findAllUsers )"
    return metta.run(query)



def parasite_symptoms(parasite_type):
    """
    Executes the MeTTa query !(parasiteSymptoms <type>) to find diseases caused by a parasite type and their symptoms.
    Input:
        parasite_type (str): The type of parasite (e.g., "Bacteria", "Virus").
    Returns:
        List of MeTTa query results (e.g., [disease, "symptoms are", [symptoms]]).
    """
    query = f"!(parasiteSymptoms {parasite_type})"
    return metta.run(query)

def vulnerable_treatments(condition):
    """
    Executes the MeTTa query !(vulnerableTreatments <condition>) to find diseases linked to a vulnerability condition and their treatments.
    Input:
        condition (str): The vulnerability condition (e.g., "lowImmuneSystem").
    Returns:
        List of MeTTa query results (e.g., [disease, [treatments]]).
    """
    query = f"!(vulnerableTreatments {condition})"
    return metta.run(query)

def user_disease_causes(name):
    """
    Executes the MeTTa query !(userDiseaseCauses <name>) to find diseases a person has and their causes.
    Input:
        name (str): The person’s name (e.g., "Bisrat").
    Returns:
        List of MeTTa query results (e.g., [disease, [causes]]).
    """
    query = f"!(userDiseaseCauses {name})"
    return metta.run(query)


print(parasite_symptoms("Bacteria"))
print(vulnerable_treatments("lowImmuneSystem"))