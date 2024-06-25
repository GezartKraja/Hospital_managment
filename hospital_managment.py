from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///hospital.db')
Session = sessionmaker(bind=engine)
session = Session()


class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    contact = Column(String, nullable=False)


class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    contact = Column(String, nullable=False)


class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    appointment_date = Column(Date, nullable=False)

    patient = relationship('Patient', back_populates='appointments')
    doctor = relationship('Doctor', back_populates='appointments')


Patient.appointments = relationship('Appointment', order_by=Appointment.id, back_populates='patient')
Doctor.appointments = relationship('Appointment', order_by=Appointment.id, back_populates='doctor')

Base.metadata.create_all(engine)


def add_patient(name, surname, age, gender, contact):
    new_patient = Patient(name=name, surname=surname, age=age, gender=gender, contact=contact)
    session.add(new_patient)
    session.commit()


def add_doctor(name, surname, specialization, contact):
    new_doctor = Doctor(name=name, surname=surname, specialization=specialization, contact=contact)
    session.add(new_doctor)
    session.commit()


def book_appointment(patient_id, doctor_id, appointment_date):
    try:
        appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
        new_appointment = Appointment(patient_id=patient_id, doctor_id=doctor_id, appointment_date=appointment_date)
        session.add(new_appointment)
        session.commit()
        print("Appointment booked successfully.")
    except ValueError:
        print("Invalid date format. Please enter the date in YYYY-MM-DD format.")


def get_patients():
    return session.query(Patient).all()


def get_doctors():
    return session.query(Doctor).all()


def get_appointments():
    return session.query(Appointment).all()


def update_patient(patient_id, new_name, new_surname, new_age, new_gender, new_contact):
    patient = session.query(Patient).filter_by(id=patient_id).first()
    if patient:
        patient.name = new_name
        patient.surname = new_surname
        patient.age = new_age
        patient.gender = new_gender
        patient.contact = new_contact
        session.commit()
        print("Patient information updated successfully.")
    else:
        print("Patient not found.")


def delete_patient(patient_id):
    patient = session.query(Patient).filter_by(id=patient_id).first()
    if patient:
        session.delete(patient)
        session.commit()
        print("Patient deleted successfully.")
    else:
        print("Patient not found.")


def search_patients(criteria):
    patients = session.query(Patient).filter(Patient.name.ilike(f'%{criteria}%')).all()
    return patients


def search_doctors(criteria):
    doctors = session.query(Doctor).filter(Doctor.name.ilike(f'%{criteria}%')).all()
    return doctors


def search_appointments(criteria):
    appointments = session.query(Appointment).filter_by(appointment_date=criteria).all()
    return appointments


def main():

    while True:
        print("Hospital Management System")
        print("1. Add Patient")
        print("2. Add Doctor")
        print("3. Book Appointment")
        print("4. View Patients")
        print("5. View Doctors")
        print("6. View Appointments")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter patient name: ")
            surname = input("Enter patient surname: ")
            age = int(input("Enter patient age: "))
            gender = input("Enter patient gender: ")
            contact = input("Enter patient contact: ")
            add_patient(name, surname, age, gender, contact)
        elif choice == '2':
            name = input("Enter doctor name: ")
            surname = input("Enter doctor surname: ")
            specialization = input("Enter doctor specialization: ")
            contact = input("Enter doctor contact: ")
            add_doctor(name, surname, specialization, contact)
        elif choice == '3':
            patient_id = int(input("Enter patient ID: "))
            doctor_id = int(input("Enter doctor ID: "))
            appointment_date = input("Enter appointment date (YYYY-MM-DD): ")
            book_appointment(patient_id, doctor_id, appointment_date)
        elif choice == '4':
            patients = get_patients()
            for patient in patients:
                print(
                    f"ID: {patient.id}, Name: {patient.name}, Surname: {patient.surname}, Age: {patient.age}, Gender: {patient.gender}, Contact: {patient.contact}")
        elif choice == '5':
            doctors = get_doctors()
            for doctor in doctors:
                print(
                    f"ID: {doctor.id}, Name: {doctor.name}, Surname: {doctor.surname}, Specialization: {doctor.specialization}, Contact: {doctor.contact}")
        elif choice == '6':
            appointments = get_appointments()
            for appointment in appointments:
                print(
                    f"ID: {appointment.id}, Patient ID: {appointment.patient_id}, Doctor ID: {appointment.doctor_id}, Date: {appointment.appointment_date}")
        elif choice == '7':
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
