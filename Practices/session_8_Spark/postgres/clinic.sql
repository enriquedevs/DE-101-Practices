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
    clinical_specialization_id INT NOT NULL,
    CONSTRAINT fk_doctor_clinical_specialization FOREIGN KEY (clinical_specialization_id) REFERENCES clinical_specialization (id)
);

-- Create appointment table
CREATE TABLE IF NOT EXISTS appointment (
    id SERIAL PRIMARY KEY NOT NULL,
    date DATE,
    time TIME,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    CONSTRAINT fk_appointment_doctor FOREIGN KEY (doctor_id) REFERENCES doctor (id),
    CONSTRAINT fk_appointment_patient FOREIGN KEY (patient_id) REFERENCES patient (id)
);

-- Insert data into patient table
INSERT INTO patient (name, last_name, address)
VALUES
    ('John', 'Doe', '123 Main St'),
    ('Jane', 'Smith', '456 Park Ave'),
    ('Michael', 'Johnson', '789 Elm St'),
    ('Emily', 'Williams', '321 Oak St'),
    ('Matthew', 'Brown', '654 Pine St'),
    ('Abigail', 'Jones', '987 Cedar St'),
    ('Daniel', 'Miller', '246 Birch St'),
    ('Elizabeth', 'Davis', '369 Maple St'),
    ('William', 'Garcia', '159 Oak St'),
    ('David', 'Rodriguez', '753 Pine St'),
    ('Joseph', 'Martinez', '951 Cedar St'),
    ('Joshua', 'Anderson', '147 Birch St'),
    ('Andrew', 'Taylor', '369 Maple St'),
    ('James', 'Thomas', '753 Pine St'),
    ('Christopher', 'Moore', '951 Cedar St'),
    ('Daniel', 'Jackson', '147 Birch St'),
    ('Matthew', 'Perez', '369 Maple St'),
    ('Jacob', 'Turner', '753 Pine St'),
    ('Nicholas', 'Phillips', '951 Cedar St'),
    ('Ryan', 'Campbell', '147 Birch St'),
    ('Stephen', 'Parker', '369 Maple St'),
    ('Jonathan', 'Evans', '753 Pine St'),
    ('Adam', 'Edwards', '951 Cedar St'),
    ('Benjamin', 'Stewart', '123 Oak St');

-- Insert data into clinical_specialization table
INSERT INTO clinical_specialization (name)
VALUES
    ('Pediatrics'),
    ('Family Medicine'),
    ('Cardiology'),
    ('Dermatology'),
    ('Orthopedics'),
    ('Neurology'),
    ('Gastroenterology'),
    ('Endocrinology'),
    ('Rheumatology'),
    ('Ophthalmology'),
    ('Urology'),
    ('Physical Medicine'),
    ('Neurosurgery'),
    ('Pulmonology'),
    ('Anesthesiology'),
    ('Pathology');

-- Insert data into doctor table
INSERT INTO doctor (name, last_name, clinical_specialization_id)
VALUES ('Jane', 'Smith', (SELECT id FROM clinical_specialization WHERE name = 'Pediatrics')),
       ('Michael', 'Johnson', (SELECT id FROM clinical_specialization WHERE name = 'Family Medicine')),
       ('Emily', 'Williams', (SELECT id FROM clinical_specialization WHERE name = 'Cardiology')),
       ('Matthew', 'Brown', (SELECT id FROM clinical_specialization WHERE name = 'Cardiology')),
       ('Abigail', 'Jones', (SELECT id FROM clinical_specialization WHERE name = 'Dermatology')),
       ('Daniel', 'Miller', (SELECT id FROM clinical_specialization WHERE name = 'Orthopedics')),
       ('Elizabeth', 'Davis', (SELECT id FROM clinical_specialization WHERE name = 'Neurology')),
       ('William', 'Garcia', (SELECT id FROM clinical_specialization WHERE name = 'Gastroenterology')),
       ('David', 'Rodriguez', (SELECT id FROM clinical_specialization WHERE name = 'Neurology')),
       ('Joseph', 'Martinez', (SELECT id FROM clinical_specialization WHERE name = 'Endocrinology')),
       ('Joshua', 'Anderson', (SELECT id FROM clinical_specialization WHERE name = 'Rheumatology')),
       ('Andrew', 'Taylor', (SELECT id FROM clinical_specialization WHERE name = 'Ophthalmology')),
       ('James', 'Thomas', (SELECT id FROM clinical_specialization WHERE name = 'Urology')),
	   ('Christopher', 'Moore', (SELECT id FROM clinical_specialization WHERE name = 'Physical Medicine')),
	   ('Daniel', 'Jackson', (SELECT id FROM clinical_specialization WHERE name = 'Neurosurgery')),
	   ('Matthew', 'Perez', (SELECT id FROM clinical_specialization WHERE name = 'Gastroenterology')),
	   ('Jacob', 'Turner', (SELECT id FROM clinical_specialization WHERE name = 'Neurology')),
	   ('Nicholas', 'Phillips', (SELECT id FROM clinical_specialization WHERE name = 'Anesthesiology')),
	   ('Ryan', 'Campbell', (SELECT id FROM clinical_specialization WHERE name = 'Pathology')),
	   ('Stephen', 'Parker', (SELECT id FROM clinical_specialization WHERE name = 'Rheumatology')),
	   ('Jonathan', 'Evans', (SELECT id FROM clinical_specialization WHERE name = 'Pulmonology')),
	   ('Adam', 'Edwards', (SELECT id FROM clinical_specialization WHERE name = 'Rheumatology')),
	   ('Benjamin', 'Stewart', (SELECT id FROM clinical_specialization WHERE name = 'Cardiology'));

-- Insert data into appointment table
INSERT INTO appointment (date, time, patient_id, doctor_id)
SELECT TO_DATE('2022-01-01', 'YYYY-MM-DD'), to_timestamp('10:00 AM', 'HH:MI AM'), id, (SELECT id FROM doctor WHERE name = 'Jane' AND last_name = 'Smith')
FROM patient WHERE name = 'John' AND last_name = 'Doe'
UNION ALL SELECT TO_DATE('2022-01-02', 'YYYY-MM-DD'), to_timestamp('11:00 AM', 'HH:MI AM'), id, (SELECT id FROM doctor WHERE name = 'Michael' AND last_name = 'Johnson')
FROM patient WHERE name = 'Jane' AND last_name = 'Smith'
UNION ALL SELECT TO_DATE('2022-01-03', 'YYYY-MM-DD'), to_timestamp('12:00 PM', 'HH:MI AM'), id, (SELECT id FROM doctor WHERE name = 'Emily' AND last_name = 'Williams')
FROM patient WHERE name = 'Michael' AND last_name = 'Johnson'
UNION ALL SELECT TO_DATE('2022-01-04', 'YYYY-MM-DD'), to_timestamp('1:00 PM', 'HH:MI AM'), id, (SELECT id FROM doctor WHERE name = 'Matthew' AND last_name = 'Brown')
FROM patient WHERE name = 'Emily' AND last_name = 'Williams'
UNION ALL SELECT TO_DATE('2022-01-05', 'YYYY-MM-DD'), to_timestamp('2:00 PM', 'HH:MI AM'), id, (SELECT id FROM doctor WHERE name = 'Abigail' AND last_name = 'Jones')
FROM patient WHERE name = 'Matthew' AND last_name = 'Brown'
UNION ALL SELECT TO_DATE('2022-01-06', 'YYYY-MM-DD'), to_timestamp('3:00 PM', 'HH:MI AM'), id, (SELECT id FROM doctor WHERE name = 'Daniel' AND last_name = 'Miller')
FROM patient WHERE name = 'Abigail' AND last_name = 'Jones'
UNION ALL SELECT TO_DATE('2022-01-07', 'YYYY-MM-DD'), to_timestamp('4:00 PM', 'HH:MI AM'), id, (SELECT id FROM doctor WHERE name = 'Elizabeth' AND last_name = 'Davis')
FROM patient WHERE name = 'Daniel' AND last_name = 'Miller'
UNION ALL SELECT TO_DATE('2022-01-08', 'YYYY-MM-DD'), to_timestamp('5:00 PM', 'HH:MI AM'), id, (SELECT id FROM doctor WHERE name = 'William' AND last_name = 'Garcia')
FROM patient WHERE name = 'Elizabeth' AND last_name = 'Davis'
UNION ALL SELECT TO_DATE('2022-01-09', 'YYYY-MM-DD'), to_timestamp('6:00 PM', 'HH:MI AM'), id, (SELECT id FROM doctor WHERE name = 'David' AND last_name = 'Rodriguez')
FROM patient WHERE name = 'William' AND last_name = 'Garcia'
UNION ALL SELECT TO_DATE('2022-01-10', 'YYYY-MM-DD'), to_timestamp('7:00 PM', 'HH:MI AM'), id, (SELECT id FROM doctor WHERE name = 'Joseph' AND last_name = 'Martinez')
FROM patient WHERE name = 'David' AND last_name = 'Rodriguez'
UNION ALL SELECT TO_DATE('2022-01-11', 'YYYY-MM-DD'), to_timestamp('8:00 PM', 'HH:MI AM'), id, (SELECT id FROM doctor WHERE name = 'Joshua' AND last_name = 'Anderson')
FROM patient WHERE name = 'Joseph' AND last_name = 'Martinez'
UNION ALL SELECT TO_DATE('2022-01-12', 'YYYY-MM-DD'), to_timestamp('9:00 PM', 'HH:MI AM'), id, (SELECT id FROM doctor WHERE name = 'Andrew' AND last_name = 'Taylor')
FROM patient WHERE name = 'Joshua' AND last_name = 'Anderson'
UNION ALL SELECT TO_DATE('2022-01-13', 'YYYY-MM-DD'), to_timestamp('10:00 PM', 'HH:MI AM'), id, (SELECT id FROM doctor WHERE name = 'James' AND last_name = 'Thomas')
FROM patient WHERE name = 'Andrew' AND last_name = 'Taylor'
UNION ALL SELECT TO_DATE('2022-01-14', 'YYYY-MM-DD'), to_timestamp('11:00 PM', 'HH:MI AM'), id, (SELECT id FROM doctor WHERE name = 'Christopher' AND last_name = 'Moore')
FROM patient WHERE name = 'James' AND last_name = 'Thomas'
UNION ALL SELECT TO_DATE('2022-01-15', 'YYYY-MM-DD'), to_timestamp('12:00 PM', 'HH:MI AM'), id, (SELECT id FROM doctor WHERE name = 'Daniel' AND last_name = 'Jackson')
FROM patient WHERE name = 'Christopher' AND last_name = 'Moore'
UNION ALL SELECT TO_DATE('2022-01-16', 'YYYY-MM-DD'), to_timestamp('1:00 PM', 'HH:MI AM'), id, (SELECT id FROM doctor WHERE name = 'Matthew' AND last_name = 'Perez')
FROM patient WHERE name = 'Daniel' AND last_name = 'Jackson'
UNION ALL SELECT TO_DATE('2022-01-17', 'YYYY-MM-DD'), to_timestamp('2:00 PM', 'HH:MI AM'), id, (SELECT id FROM doctor WHERE name = 'Jacob' AND last_name = 'Turner')
FROM patient WHERE name = 'Matthew' AND last_name = 'Perez'
UNION ALL SELECT TO_DATE('2022-01-18', 'YYYY-MM-DD'), to_timestamp('3:00 PM', 'HH:MI AM'), id, (SELECT id FROM doctor WHERE name = 'Nicholas' AND last_name = 'Phillips')
FROM patient WHERE name = 'Jacob' AND last_name = 'Turner'
UNION ALL SELECT TO_DATE('2022-01-19', 'YYYY-MM-DD'), to_timestamp('4:00 PM', 'HH:MI AM'), id, (SELECT id FROM doctor WHERE name = 'Ryan' AND last_name = 'Campbell')
FROM patient WHERE name = 'Nicholas' AND last_name = 'Phillips'
UNION ALL SELECT TO_DATE('2022-01-20', 'YYYY-MM-DD'), to_timestamp('5:00 PM', 'HH:MI AM'), id, (SELECT id FROM doctor WHERE name = 'Stephen' AND last_name = 'Parker')
FROM patient WHERE name = 'Ryan' AND last_name = 'Campbell';

COMMIT;