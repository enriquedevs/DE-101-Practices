-- Create patient table
CREATE TABLE IF NOT EXISTS patient (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(100),
    last_name VARCHAR(100),
    address VARCHAR(200)
);

-- Create clinical_specialization table
CREATE TABLE IF NOT EXISTS clinical_specialization (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(100)
);

-- Create doctor table
CREATE TABLE IF NOT EXISTS doctor (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(100),
    last_name VARCHAR(100),
    clinical_specialization_id INT,
    CONSTRAINT fk_doctor_clinical_specialization FOREIGN KEY (clinical_specialization_id) REFERENCES clinical_specialization (id)
);

-- Create appointment table
CREATE TABLE IF NOT EXISTS appointment (
    id SERIAL PRIMARY KEY NOT NULL,
    date DATE,
    time TIME,
    patient_id INT,
    doctor_id INT,
    CONSTRAINT fk_appointment_doctor FOREIGN KEY (doctor_id) REFERENCES doctor (id),
    CONSTRAINT fk_appointment_patient FOREIGN KEY (patient_id) REFERENCES patient (id)
);