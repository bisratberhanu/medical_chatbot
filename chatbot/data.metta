(Name Bisrat)
(Name Amina )
(Name Jamil)
(Name Sara)
(Name Omar)
(Name Layla)
(Name Tariq)

( = (findAllUsers)
    (collapse (match &self (Name $name) $name))
)

( = (findUser $name)
    (collapse (match &self (Name $name) $name))
)

( = (findDiseaseFromUser $name)
    (collapse (match &self (Has $name $disease) $disease))
)

( = (findDisreaseFromVulnerability $vulnerable)
    (collapse (match &self (Vulnerable $disease $vulnerable) $disease))
)


; Parasites and Types
(Parasite Typoiad Bacteria)
(Parasite Cold Virus)
(Parasite Malaria Protozoa)
(Parasite Giardia ParasiticProtozoa)
(Parasite Toxoplasma ParasiticProtozoa)
(Parasite Lyme Bacteria)
(Parasite Chagas ParasiticInsect)
(Parasite Schistosoma Worm)
; Diseases and Causes

(CausedBy Typoiad notWashingHands)
(CausedBy Typoiad ByTouchingPeople)
(CausedBy Cold Virus)
(CausedBy Malaria MosquitoBite)
(CausedBy Giardia ContaminatedWater)
(CausedBy Toxoplasma CatFeces)
(CausedBy Lyme TickBite)
(CausedBy Chagas InsectBite)
(CausedBy Schistosoma WaterExposure)
(CausedBy Flu Virus)
(CausedBy Pneumonia Bacteria)
(CausedBy Tuberculosis AirborneBacteria)
(CausedBy Hepatitis ContaminatedFood)
; Vulnerabilities

(Vulnerable Cold lowImmuneSystem)
(Vulnerable Flu lowImmuneSystem)
(Vulnerable Malaria TropicalClimate)
(Vulnerable Giardia poorSanitation)
(Vulnerable Toxoplasma weakenedImmunity)
(Vulnerable Lyme OutdoorActivity)
(Vulnerable Tuberculosis CrowdedLiving)
(Vulnerable Hepatitis poorHygiene)
(Vulnerable Pneumonia elderly)
(Vulnerable Alzheimer agedPerson)
; Correlations Between Conditions

( = (findDisreaseFromVulnerability $vulnerable )
    (match &self (Vulnerable $disease $vulnerable) $disease)

)

(Correlated Cold Flu)
(Correlated Flu Pneumonia)
(Correlated Malaria Dengue)
(Correlated Giardia Dysentery)
(Correlated Toxoplasma Schizophrenia)
(Correlated Lyme Arthritis)
(Correlated Tuberculosis HIV)
(Correlated Hepatitis Cirrhosis)
; Genetic Predispositions
(Has Bisrat Flu)
(Has Amina Malaria)
(Has Jamil Tuberculosis)
(Has Sara Alzheimer)
(Has Omar SickleCell)
(Has Layla CysticFibrosis)
(Has Tariq Huntington)
; Likelihood Scenarios

(Likely Alzheimer agedPerson)
(Likely Diabetes obesity)
(Likely Malaria tropicalResident)
(Likely Cold coldWeather)
(Likely Flu seasonalChange)
(Likely Pneumonia postFlu)
(Likely Tuberculosis immuneDeficiency)
(Likely SickleCell africanDescent)
; Additional Patterns
; Symptoms:


(SymptomOf Typoiad Fever)
(SymptomOf Cold Cough)
(SymptomOf Malaria Chills)
(SymptomOf Giardia Diarrhea)
(SymptomOf Flu Fatigue)
(SymptomOf Alzheimer MemoryLoss)
(SymptomOf Pneumonia ShortnessOfBreath)
(SymptomOf Tuberculosis NightSweats)
; Treatments:

(TreatedBy Typoiad Antibiotics)
(TreatedBy Cold Rest)
(TreatedBy Malaria Antimalarials)
(TreatedBy Giardia Antiparasitics)
(TreatedBy Flu Antivirals)
(TreatedBy Alzheimer Medication)
(TreatedBy Pneumonia Antibiotics)
(TreatedBy Tuberculosis Antibiotics)

; Transmission:

(TransmittedBy Cold Airborne)
(TransmittedBy Flu Contact)
(TransmittedBy Malaria Mosquito)
(TransmittedBy Tuberculosis Cough)
(TransmittedBy Hepatitis Blood)

; Complications:
(Complicates Flu Pneumonia)
(Complicates Malaria OrganFailure)
(Complicates Tuberculosis LungDamage)
(Complicates Alzheimer Dementia)
(Complicates Diabetes Blindness)

; Prevention:
(PreventedBy Typoiad HandWashing)
(PreventedBy Cold Vaccination)
(PreventedBy Malaria MosquitoNet)
(PreventedBy Tuberculosis Ventilation)
(PreventedBy Flu Hygiene)

; Rare Diseases and Specific Cases
(Parasite Fabry EnzymeDeficiency)
(CausedBy Fabry GeneticMutation)
(Vulnerable Fabry Children)
(SymptomOf Fabry Pain)
(TreatedBy Fabry EnzymeReplacement)
(Has Khalid Fabry)
(Parasite Pompe GlycogenStorage)
(CausedBy Pompe Genetic)
(SymptomOf Pompe MuscleWeakness)
(Vulnerable Pompe Infants)
(TreatedBy Pompe EnzymeTherapy)
(Parasite Gaucher LipidStorage)
(CausedBy Gaucher GeneticMutation)
(SymptomOf Gaucher Fatigue)
(TreatedBy Gaucher EnzymeReplacement)
(Vulnerable Gaucher Adults)


( = (causedBy $disease)
    (collapse (match &self (CausedBy $disease $cause) $cause))

)



( = (findParasite $disease)
    (collapse (match &self (Parasite $disease $parasite) $parasite))

)



( = (getDiseaseAndCorrelatedDisease $name)

    (let $disease  (match &self (Has $name $disease) $disease)
        ($disease (match &self (Correlated $disease $correlated) $correlated))
    )
)

(= (parasiteSymptoms $type)
    (let $disease (match &self (Parasite $disease $type) $disease)
        ($disease ("symptoms are") (match &self (SymptomOf $disease $symptom) $symptom)))
)


(= (vulnerableTreatments $condition)
    (let $disease (match &self (Vulnerable $disease $condition) $disease)
        ($disease (match &self (TreatedBy $disease $treatment) $treatment)))
)

(= (userDiseaseCauses $name)
    (let $disease (match &self (Has $name $disease) $disease)
        ($disease (match &self (CausedBy $disease $cause) $cause)))
)