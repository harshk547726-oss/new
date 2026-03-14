DISEASE_METADATA = {
    "Flu": {
        "description": "Influenza is a contagious respiratory illness caused by influenza viruses.",
        "precautions": ["Rest well", "Stay hydrated", "Avoid close contact"],
        "medications": ["Paracetamol", "Antiviral drugs (if prescribed)"],
        "doctor": "General Physician",
    },
    "COVID-19": {
        "description": "COVID-19 is a respiratory disease caused by SARS-CoV-2.",
        "precautions": ["Wear a mask", "Isolate when symptomatic", "Monitor oxygen levels"],
        "medications": ["Fever reducers", "Doctor-prescribed antivirals"],
        "doctor": "Pulmonologist",
    },
}


DEFAULT_INFO = {
    "description": "This appears to be a symptomatic condition requiring clinical validation.",
    "precautions": ["Take adequate rest", "Stay hydrated", "Observe symptom progression"],
    "medications": ["Only take medicines prescribed by a doctor"],
    "doctor": "General Physician",
}


def get_disease_info(disease: str):
    return DISEASE_METADATA.get(disease, DEFAULT_INFO)
