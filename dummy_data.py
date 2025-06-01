import random

# Base lists for generating diverse data

INSTITUTION_NAMES = [
    "Global Health Clinic",
    "Apex Medical Center",
    "Vitality Hospital",
    "Pinnacle Healthcare Group",
    "Evergreen Medical Institute",
    "Compassionate Care Hospital",
    "The Wellness Hub",
    "Premier Diagnostic Center",
    "Serene Medical Clinic",
    "Bridgepoint Health Systems",
    "Phoenix Medical Group",
    "Unity Wellness Clinic",
    "Grand Central Hospital",
    "Elite Medical Solutions",
    "Horizon Health Center",
    "New Dawn Clinic",
    "Summit Medical Plaza",
    "Harbor Light Hospital"
]

INSTITUTION_TYPES = ["Private", "Public"]

INSTITUTION_ADDRESSES = [
    "123 Dr. Zoran Đinđića, Belgrade, Central Serbia 11000",
    "45 Bulevar Oslobođenja, Novi Sad, Vojvodina 21000",
    "78 Vojvode Stepe, Niš, Southern and Eastern Serbia 18000",
    "101 Kralja Milana, Kragujevac, Šumadija and Western Serbia 34000",
    "20 Trg Slobode, Subotica, Vojvodina 24000",
    "30 Karađorđeva, Valjevo, Šumadija and Western Serbia 14000",
    "40 Knez Mihailova, Belgrade, Central Serbia 11000",
    "55 Partizanska, Bor, Eastern Serbia 19210",
    "60 Nikole Pašića, Leskovac, Southern and Eastern Serbia 16000",
    "75 Dostojevskog, Čačak, Šumadija and Western Serbia 32000",
    "88 Ulica Branislava Nušića, Pančevo, Vojvodina 26000",
    "99 Vojvode Mišića, Zaječar, Eastern Serbia 19000",
    "15 Kosovska, Užice, Šumadija and Western Serbia 31000",
    "25 Topličina, Prokuplje, Southern and Eastern Serbia 18400",
    "35 Kralja Petra I, Sremska Mitrovica, Vojvodina 22000",
    "50 Dunavska, Belgrade, Central Serbia 11000",
    "11 Đure Jakšića, Sombor, Vojvodina 25000",
    "200 Kraljice Marije, Kraljevo, Šumadija and Western Serbia 36000"
]

FIRST_NAMES = [
    "Ana", "Luka", "Marko", "Ivana", "Stefan", "Milica", "Nikola",
    "Sofija", "Filip", "Dunja", "Pavle", "Marija", "Vuk", "Teodora", "Uros",
    "Katarina", "Petar", "Anja", "Djordje",
    "Ema", "Andrej", "Mina", "Dimitrije",
    "Sara", "David", "Lena", "Vukasin", "Jana", "Aleksa", "Mia", "Novak",
    "Lara", "Milos",
    "Isidora", "Vasilije", "Masa",
    "Boris", "Tara", "Ivan"
]
LAST_NAMES = [
    "Petrovic",
    "Jovanovic",
    "Kostic",
    "Ilic",
    "Nikolic",
    "Djordjevic",
    "Pavlovic",
    "Popovic",
    "Stankovic",
    "Simic",
    "Zivkovic",
    "Todorovic",
    "Markovic",
    "Milosevic",
    "Stojanovic",
    "Antic",
    "Djuric",
    "Radovanovic",
    "Vasic",
    "Kovacevic",
    "Ristic",
    "Mihajlovic",
    "Lazarevic",
    "Mitrovic",
    "Savic",
    "Stevanovic",
    "Cvetkovic"
]
SPECIALIZATION_TO_INTERESTS = {
    "Cardiologist": ["Heart Disease", "Hypertension", "Arrhythmias", "Coronary Artery Disease"],
    "Dermatologist": ["Skin Cancer", "Acne Treatment", "Eczema", "Psoriasis", "Cosmetic Dermatology"],
    "Neurologist": ["Epilepsy", "Migraine Treatment", "Stroke Rehabilitation", "Parkinson's Disease", "Alzheimer's Disease"],
    "Orthopedic Surgeon": ["Sports Injuries", "Joint Replacement", "Spinal Surgery", "Fracture Repair", "Arthroscopy"],
    "Pediatrician": ["Child Development", "Vaccine Administration", "Childhood Obesity", "Adolescent Health", "Infectious Diseases in Children"],
    "Gastroenterologist": ["Digestive Disorders", "Crohn's Disease", "Colitis", "Endoscopy", "Liver Disease"],
    "Pulmonologist": ["Asthma", "COPD", "Lung Cancer", "Respiratory Infections", "Sleep Apnea"],
    "Endocrinologist": ["Diabetes Management", "Thyroid Disorders", "Hormone Imbalance", "Adrenal Gland Disorders"],
    "Oncologist": ["Cancer Research", "Chemotherapy", "Radiation Therapy", "Palliative Care", "Targeted Therapy"],
    "Radiologist": ["Diagnostic Imaging", "MRI Interpretation", "X-ray Analysis", "CT Scans", "Ultrasound"],
    "Psychiatrist": ["Mental Health", "Depression Treatment", "Anxiety Disorders", "Bipolar Disorder", "Schizophrenia"],
    "Ophthalmologist": ["Eye Surgery", "Cataract Removal", "Glaucoma Treatment", "Retinal Disorders"],
    "Urologist": ["Urinary Tract Infections", "Kidney Stones", "Prostate Health", "Bladder Disorders"],
    "Nephrologist": ["Kidney Disease", "Dialysis", "Kidney Transplants", "Hypertension-related Kidney Issues"],
    "Infectious Disease Specialist": ["Vaccine Development", "Bacterial Infections", "Viral Diseases", "Global Health"],
    "Rheumatologist": ["Autoimmune Disorders", "Arthritis Management", "Lupus", "Gout"],
    "Allergist": ["Allergy Testing", "Asthma Management", "Food Allergies", "Immunotherapy"],
    "General Practitioner": ["Preventive Medicine", "Chronic Disease Management", "General Check-ups", "Minor Illnesses"],
    "Dentist": ["Oral Health", "Dental Fillings", "Root Canals", "Orthodontics", "Gum Disease"],
    "Physiatrist": ["Rehabilitation Medicine", "Pain Management", "Spasticity", "Nerve Damage"]
}

# Ensure all specializations have at least one interest, and vice-versa (for robustness)
ALL_SPECIALIZATIONS = list(SPECIALIZATION_TO_INTERESTS.keys())
# Create a fallback for interests if a specialization somehow isn't in the mapping
GENERAL_FIELDS_OF_INTEREST = list(set(sum(SPECIALIZATION_TO_INTERESTS.values(), []))) # Flatten all interests

def generate_institutions():
    """Generates a list of institution data."""
    institutions_data = []
    # Ensure unique names from the start
    unique_institution_names = list(set(INSTITUTION_NAMES))[:len(INSTITUTION_NAMES)]
    
    for i, name in enumerate(unique_institution_names):
        institutions_data.append({
            "name": name,
            "type": random.choice(INSTITUTION_TYPES),
            "address": INSTITUTION_ADDRESSES[i % len(INSTITUTION_ADDRESSES)]
        })
    return institutions_data

def generate_doctors(num_doctors=120):
    """
    Generates a list of doctor data, ensuring coherent specialization
    and field of interest combinations.
    """
    doctors_data = []
    
    # Get the names of the institutions that will be created
    current_institution_names = [inst["name"] for inst in generate_institutions()]
    if not current_institution_names:
        raise ValueError("No institutions generated. Cannot assign doctors.")

    generated_full_names = set() # To ensure unique full names for primary key

    for i in range(num_doctors):
        # Generate a unique full name
        while True:
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            full_name = f"{first} {last}"
            if full_name not in generated_full_names:
                generated_full_names.add(full_name)
                break

        specialization = random.choice(ALL_SPECIALIZATIONS)
        
        # Select field of interest based on the chosen specialization
        possible_interests = SPECIALIZATION_TO_INTERESTS.get(specialization, GENERAL_FIELDS_OF_INTEREST)
        field_of_interest = random.choice(possible_interests)
        
        doctors_data.append({
            "full_name": full_name,
            "specialization": specialization,
            "field_of_interest": field_of_interest,
            "institution_name": random.choice(current_institution_names) # Randomly assign to any institution
        })
    return doctors_data

if __name__ == "__main__":
    print("Generated Institutions:")
    for inst in generate_institutions():
        print(inst)
    
    print("\nGenerated Doctors (first 10, showing coherence):")
    generated_doctors = generate_doctors(num_doctors=10) # Just 10 for display
    for doc in generated_doctors:
        print(f"  - {doc['full_name']} | {doc['specialization']} | {doc['field_of_interest']} | {doc['institution_name']}")
    print(f"\nTotal doctors generated: {len(generate_doctors())}") # Show total if default is used