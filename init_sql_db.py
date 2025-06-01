import os
from sqlalchemy import create_engine, Column, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import IntegrityError

from dummy_data import generate_institutions, generate_doctors


# Define the base for declarative models
Base = declarative_base()

# Define the Institution model
class Institution(Base):
    __tablename__ = 'institutions'
    name = Column(String, primary_key=True)  # Name as primary key
    type = Column(String)  # "Private" or "Public"
    address = Column(String)
    # Define the relationship to Doctor
    doctors = relationship("Doctor", back_populates="institution", cascade="all, delete-orphan")

# Define the Doctor model
class Doctor(Base):
    __tablename__ = 'doctors'
    full_name = Column(String, primary_key=True)  # Full name as primary key
    specialization = Column(String)
    field_of_interest = Column(String)
    # Foreign key referencing institutions.name
    institution_name = Column(String, ForeignKey('institutions.name'))
    # Define the relationship to Institution
    institution = relationship("Institution", back_populates="doctors")

# Define the database file path
DB_FILE = "data/medical.db"

# --- Database Initialization and Population ---
def initialize_database():
    # Ensure the 'data' directory exists
    os.makedirs('data', exist_ok=True)

    # Create the database engine
    engine = create_engine(f"sqlite:///{DB_FILE}")

    # Dispose of any lingering connections from previous runs
    engine.dispose() 
    
    print(f"Connecting to database: {DB_FILE}")

    # Drop all existing tables before recreating them
    Base.metadata.drop_all(engine)
    print("Existing database tables dropped.")

    # Create all tables defined in Base with the new schema
    Base.metadata.create_all(engine)
    print("Database tables created with new schema.")

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # --- Generate and Add Institutions ---
        institutions_data = generate_institutions()
        institutions_objects = [Institution(**data) for data in institutions_data]
        session.add_all(institutions_objects)
        session.commit()
        print(f"Added {len(institutions_objects)} dummy institutions.")

        # --- Generate and Add Doctors ---
        doctors_data = generate_doctors() # Generates 120 doctors by default
        doctors_objects = [Doctor(**data) for data in doctors_data]
        session.add_all(doctors_objects)
        session.commit()
        print(f"Added {len(doctors_objects)} dummy doctors.")

        print("\n✅ Database populated with dummy data.")


    except IntegrityError as e:
        session.rollback()
        print(f"Error populating database: {e}")
        print("This might happen if you try to add duplicate primary keys or violate foreign key constraints.")
    except Exception as e:
        session.rollback()
        print(f"An unexpected error occurred during data population: {e}")
    finally:
        session.close()
        # Ensure the engine is disposed after all operations
        engine.dispose()

if __name__ == "__main__":
    initialize_database()