CREATE TABLE suppliers (
    supplierId VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact VARCHAR(50)
);

CREATE TABLE medicines (
    medId VARCHAR(50) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    dosage VARCHAR(50),
    expiry_date DATE,
    medType VARCHAR(255),
    inStock INT NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE medSup (
    medId VARCHAR(50),
    supplierId VARCHAR(50),
    inStock INT NOT NULL,
    dateOfPurch DATE,
    priceBought DECIMAL(10,2) NOT NULL,
    PRIMARY KEY(medId, supplierId),
    FOREIGN KEY (medId) REFERENCES medicines(medId),
    FOREIGN KEY (supplierId) REFERENCES suppliers(supplierId)
);

CREATE TABLE customers (
    customerId VARCHAR(50) PRIMARY KEY,
    customerLastName VARCHAR(50) NOT NULL,
    customerFirstName VARCHAR(50) NOT NULL,
    HasDisCard INT
);

CREATE TABLE doctors(
    docId VARCHAR(50) PRIMARY KEY,
    doctorLastName VARCHAR(50) NOT NULL,
    doctorFirstName VARCHAR(50) NOT NULL
);

CREATE TABLE prescriptions (
    presId VARCHAR(50) PRIMARY KEY,
    customerId VARCHAR(50),
    medId VARCHAR(50),
    docId VARCHAR(50),
    FOREIGN KEY (medId) REFERENCES medicines(medId),
    FOREIGN KEY (customerId) REFERENCES customers(customerId),
    FOREIGN KEY (docId) REFERENCES doctors(docId)
);

CREATE TABLE sales (
    salesID VARCHAR(50) PRIMARY KEY,
    salesDate DATE,
    quantitySold INT,
    totalPrice DECIMAL(10,2),
    medId VARCHAR(50),
    customerId VARCHAR(50),
    presId VARCHAR(50),
    mOP VARCHAR(50),
    discount FLOAT,
    FOREIGN KEY (medId) REFERENCES medicines(medId),
    FOREIGN KEY (customerId) REFERENCES customers(customerId),
    FOREIGN KEY (presId) REFERENCES prescriptions(presId)
);

INSERT INTO suppliers VALUES ('B10005', 'Andrews-White', '810.875.6137');
INSERT INTO suppliers VALUES ('B10006', 'Greene-Williams', '565.693.8258');
INSERT INTO suppliers VALUES ('B10007', 'Fisher, Diaz and Walker', '001-257-731-7834');
INSERT INTO suppliers VALUES ('B10008', 'Odonnell-Horne', '+1-842-018-5865x867');
INSERT INTO suppliers VALUES ('B10009', 'Perez, Green and Estrada', '(532)897-3956x472');
INSERT INTO suppliers VALUES ('B10010', 'Gibson Ltd', '828-228-2620x15121');
INSERT INTO suppliers VALUES ('B10011', 'Paul, Saunders and Wilson', '001-988-119-1066x88874');
INSERT INTO suppliers VALUES ('B10012', 'Torres-Stone', '+1-969-747-4917');
INSERT INTO suppliers VALUES ('B10013', 'Henderson Ltd', '7229597199');
INSERT INTO suppliers VALUES ('B10014', 'Fields LLC', '887.111.1312x372');
INSERT INTO suppliers VALUES ('B10015', 'Spencer-King', '(489)639-7350x370');
INSERT INTO suppliers VALUES ('B10016', 'Thompson Inc', '574-567-1370');
INSERT INTO suppliers VALUES ('B10017', 'Moran and Sons', '(500)682-3607x7416');
INSERT INTO suppliers VALUES ('B10018', 'Hoffman, Reynolds and Beck', '324.071.5997x52099');
INSERT INTO suppliers VALUES ('B10019', 'Hill Group', '(579)402-1210x169');
INSERT INTO suppliers VALUES ('B10020', 'Gordon Group', '(918)286-6717x9249');
INSERT INTO suppliers VALUES ('B10021', 'Thomas Group', '464.408.7048x4014');
INSERT INTO suppliers VALUES ('B10022', 'Oconnor, Young and Nguyen', '919.227.0316');
INSERT INTO suppliers VALUES ('B10023', 'Montes, Castro and Stephens', '(762)552-3666x018');
INSERT INTO suppliers VALUES ('B10024', 'Harper-Dean', '(310)951-6619');
INSERT INTO suppliers VALUES ('B10025', 'Griffin, Hebert and Aguilar', '442-999-0559');
INSERT INTO suppliers VALUES ('B10026', 'Andrews, Wagner and Fuller', '(739)476-9119');
INSERT INTO suppliers VALUES ('B10027', 'Ramirez-Weber', '423.153.6921');
INSERT INTO suppliers VALUES ('B10028', 'Hart-Swanson', '+1-363-230-4918');
INSERT INTO suppliers VALUES ('B10029', 'Wallace Group', '767.215.5308x678');
INSERT INTO suppliers VALUES ('B10030', 'Garner LLC', '902-652-2342x288');
INSERT INTO suppliers VALUES ('B10031', 'Rivera-Anderson', '597-913-2726x52843');
INSERT INTO suppliers VALUES ('B10032', 'Johnson and Sons', '(611)627-2516');
INSERT INTO suppliers VALUES ('B10033', 'Smith-Marks', '(218)568-0116');
INSERT INTO suppliers VALUES ('B10034', 'Reed Inc', '+1-316-373-2146');
INSERT INTO suppliers VALUES ('B10035', 'Davies, Carter and Chen', '(630)801-3422');
INSERT INTO suppliers VALUES ('B10036', 'Lynch Inc', '5581051023');
INSERT INTO suppliers VALUES ('B10037', 'Hoover and Sons', '181-129-0350x79744');
INSERT INTO suppliers VALUES ('B10038', 'Monroe Ltd', '+1-434-030-0613x40925');
INSERT INTO suppliers VALUES ('B10039', 'Gray-Cooper', '001-363-252-4601x888');
INSERT INTO suppliers VALUES ('B10040', 'Weiss Inc', '379-209-8566');
INSERT INTO suppliers VALUES ('B10041', 'Anderson, Wilkins and Jacobson', '404-258-0036x3884');
INSERT INTO suppliers VALUES ('B10042', 'Saunders, Hernandez and Armstrong', '957.647.9347');
INSERT INTO suppliers VALUES ('B10043', 'James, Butler and Young', '335-710-7881');
INSERT INTO suppliers VALUES ('B10044', 'Miller, Wolf and Smith', '365-831-0916');
INSERT INTO suppliers VALUES ('B10045', 'Edwards LLC', '001-079-822-3240x22896');
INSERT INTO suppliers VALUES ('B10046', 'Grant-Stephens', '(400)773-8276');
INSERT INTO suppliers VALUES ('B10047', 'Santana-Silva', '(016)560-9608x0620');
INSERT INTO suppliers VALUES ('B10048', 'Acosta, Porter and Good', '752.392.9392x556');
INSERT INTO suppliers VALUES ('B10049', 'Brady and Sons', '341-079-7510');
INSERT INTO suppliers VALUES ('B10050', 'Smith, Cook and Simpson', '578.652.5029');
INSERT INTO suppliers VALUES ('B10051', 'Wilkinson, Martinez and Valencia', '710-562-1981x416');
INSERT INTO suppliers VALUES ('B10052', 'Miller Ltd', '001-357-684-8809x590');
INSERT INTO suppliers VALUES ('B10053', 'Wallace, Contreras and Snow', '370.112.3152x104');
INSERT INTO suppliers VALUES ('B10054', 'Wang-Wood', '0383644826');

INSERT INTO medicines VALUES ('A10005', 'Your', '437mg', '2027-03-30', 'OTC', 66, 49.45);
INSERT INTO medicines VALUES ('A10006', 'Watch', '38mg', '2027-12-05', 'OTC', 52, 46.51);
INSERT INTO medicines VALUES ('A10007', 'More', '140mg', '2027-11-25', 'OTC', 33, 25.33);
INSERT INTO medicines VALUES ('A10008', 'Blood', '230mg', '2026-06-25', 'OTC', 100, 8.36);
INSERT INTO medicines VALUES ('A10009', 'Opportunity', '103mg', '2026-03-18', 'OTC', 26, 30.81);
INSERT INTO medicines VALUES ('A10010', 'Writer', '216mg', '2029-03-30', 'Prescription', 90, 46.63);
INSERT INTO medicines VALUES ('A10011', 'Which', '211mg', '2026-11-27', 'Prescription', 79, 26.68);
INSERT INTO medicines VALUES ('A10012', 'Task', '250mg', '2027-05-28', 'OTC', 50, 45.09);
INSERT INTO medicines VALUES ('A10013', 'Imagine', '193mg', '2028-12-01', 'OTC', 28, 31.08);
INSERT INTO medicines VALUES ('A10014', 'Pass', '417mg', '2027-04-29', 'OTC', 74, 30.77);
INSERT INTO medicines VALUES ('A10015', 'Would', '27mg', '2026-10-13', 'OTC', 87, 21.63);
INSERT INTO medicines VALUES ('A10016', 'Any', '389mg', '2026-05-13', 'Prescription', 72, 21.67);
INSERT INTO medicines VALUES ('A10017', 'Theory', '391mg', '2030-06-26', 'Prescription', 62, 11.15);
INSERT INTO medicines VALUES ('A10018', 'Catch', '27mg', '2025-05-10', 'OTC', 52, 28.94);
INSERT INTO medicines VALUES ('A10019', 'Realize', '43mg', '2028-09-03', 'OTC', 14, 40.07);
INSERT INTO medicines VALUES ('A10020', 'Key', '432mg', '2027-04-25', 'Prescription', 15, 16.57);
INSERT INTO medicines VALUES ('A10021', 'Can', '318mg', '2029-05-25', 'Prescription', 38, 30.75);
INSERT INTO medicines VALUES ('A10022', 'Yard', '26mg', '2030-07-02', 'OTC', 63, 28.27);
INSERT INTO medicines VALUES ('A10023', 'South', '48mg', '2027-12-21', 'Prescription', 76, 34.99);
INSERT INTO medicines VALUES ('A10024', 'Kid', '29mg', '2030-11-03', 'OTC', 32, 13.2);
INSERT INTO medicines VALUES ('A10025', 'Management', '275mg', '2026-08-08', 'OTC', 36, 42.58);
INSERT INTO medicines VALUES ('A10026', 'Water', '372mg', '2029-04-01', 'OTC', 14, 48.33);
INSERT INTO medicines VALUES ('A10027', 'Star', '482mg', '2026-01-02', 'OTC', 44, 36.77);
INSERT INTO medicines VALUES ('A10028', 'International', '354mg', '2030-03-30', 'OTC', 35, 21.72);
INSERT INTO medicines VALUES ('A10029', 'Myself', '400mg', '2025-12-19', 'OTC', 91, 9.32);
INSERT INTO medicines VALUES ('A10030', 'Offer', '465mg', '2029-09-21', 'OTC', 78, 47.58);
INSERT INTO medicines VALUES ('A10031', 'Trip', '149mg', '2028-03-17', 'OTC', 11, 41.6);
INSERT INTO medicines VALUES ('A10032', 'Movie', '291mg', '2025-06-08', 'Prescription', 47, 30.46);
INSERT INTO medicines VALUES ('A10033', 'Under', '307mg', '2026-09-04', 'OTC', 95, 41.98);
INSERT INTO medicines VALUES ('A10034', 'Believe', '322mg', '2027-09-28', 'OTC', 48, 34.08);
INSERT INTO medicines VALUES ('A10035', 'Can', '178mg', '2027-07-02', 'Prescription', 13, 12.04);
INSERT INTO medicines VALUES ('A10036', 'Run', '498mg', '2029-03-04', 'Prescription', 63, 49.53);
INSERT INTO medicines VALUES ('A10037', 'Break', '327mg', '2027-02-24', 'OTC', 73, 30.19);
INSERT INTO medicines VALUES ('A10038', 'Difference', '279mg', '2025-11-19', 'OTC', 67, 25.18);
INSERT INTO medicines VALUES ('A10039', 'Reflect', '313mg', '2028-01-05', 'Prescription', 50, 37.18);
INSERT INTO medicines VALUES ('A10040', 'Skill', '392mg', '2028-06-25', 'Prescription', 82, 37.24);
INSERT INTO medicines VALUES ('A10041', 'Public', '482mg', '2030-12-08', 'Prescription', 88, 16.31);
INSERT INTO medicines VALUES ('A10042', 'Not', '139mg', '2028-02-27', 'Prescription', 19, 22.54);
INSERT INTO medicines VALUES ('A10043', 'Top', '470mg', '2029-08-16', 'OTC', 18, 17.1);
INSERT INTO medicines VALUES ('A10044', 'Song', '51mg', '2027-12-22', 'Prescription', 89, 11.16);
INSERT INTO medicines VALUES ('A10045', 'Method', '426mg', '2028-06-27', 'OTC', 71, 48.11);
INSERT INTO medicines VALUES ('A10046', 'Character', '85mg', '2029-05-26', 'OTC', 93, 47.29);
INSERT INTO medicines VALUES ('A10047', 'Significant', '221mg', '2030-08-07', 'Prescription', 39, 17.24);
INSERT INTO medicines VALUES ('A10048', 'Blood', '33mg', '2030-02-05', 'Prescription', 70, 49.84);
INSERT INTO medicines VALUES ('A10049', 'Second', '490mg', '2025-02-11', 'OTC', 47, 23.3);
INSERT INTO medicines VALUES ('A10050', 'Boy', '280mg', '2027-05-13', 'OTC', 47, 41.37);
INSERT INTO medicines VALUES ('A10051', 'Own', '41mg', '2027-07-17', 'OTC', 68, 11.89);
INSERT INTO medicines VALUES ('A10052', 'Represent', '180mg', '2030-03-21', 'Prescription', 81, 21.08);
INSERT INTO medicines VALUES ('A10053', 'End', '108mg', '2025-05-12', 'OTC', 93, 8.48);
INSERT INTO medicines VALUES ('A10054', 'Record', '75mg', '2028-07-04', 'OTC', 70, 38.8);

INSERT INTO customers VALUES ('C10005', 'Green', 'Joshua', 1);
INSERT INTO customers VALUES ('C10006', 'Cline', 'Christopher', 1);
INSERT INTO customers VALUES ('C10007', 'Powers', 'Zachary', 0);
INSERT INTO customers VALUES ('C10008', 'Martin', 'Darryl', 0);
INSERT INTO customers VALUES ('C10009', 'Porter', 'Joel', 0);
INSERT INTO customers VALUES ('C10010', 'Coffey', 'Alyssa', 0);
INSERT INTO customers VALUES ('C10011', 'Anderson', 'Kimberly', 0);
INSERT INTO customers VALUES ('C10012', 'Wilkinson', 'Allison', 0);
INSERT INTO customers VALUES ('C10013', 'Rodriguez', 'Nathan', 1);
INSERT INTO customers VALUES ('C10014', 'Stone', 'Kimberly', 0);
INSERT INTO customers VALUES ('C10015', 'Wiggins', 'Caleb', 0);
INSERT INTO customers VALUES ('C10016', 'Graves', 'Amber', 0);
INSERT INTO customers VALUES ('C10017', 'Kaiser', 'Teresa', 1);
INSERT INTO customers VALUES ('C10018', 'Leblanc', 'Jonathan', 1);
INSERT INTO customers VALUES ('C10019', 'Fuller', 'Jesus', 0);
INSERT INTO customers VALUES ('C10020', 'Stephenson', 'Stephen', 0);
INSERT INTO customers VALUES ('C10021', 'Cross', 'Amanda', 1);
INSERT INTO customers VALUES ('C10022', 'Norman', 'David', 1);
INSERT INTO customers VALUES ('C10023', 'Leonard', 'Johnny', 0);
INSERT INTO customers VALUES ('C10024', 'Knapp', 'Brittney', 1);
INSERT INTO customers VALUES ('C10025', 'Moore', 'Christopher', 1);
INSERT INTO customers VALUES ('C10026', 'Henson', 'Jeffrey', 1);
INSERT INTO customers VALUES ('C10027', 'Crawford', 'Christopher', 1);
INSERT INTO customers VALUES ('C10028', 'May', 'Debra', 0);
INSERT INTO customers VALUES ('C10029', 'Martin', 'Alicia', 0);
INSERT INTO customers VALUES ('C10030', 'Klein', 'Jacqueline', 0);
INSERT INTO customers VALUES ('C10031', 'Hamilton', 'Jenny', 1);
INSERT INTO customers VALUES ('C10032', 'Castro', 'Hailey', 0);
INSERT INTO customers VALUES ('C10033', 'Benson', 'Timothy', 0);
INSERT INTO customers VALUES ('C10034', 'Walker', 'Barbara', 0);
INSERT INTO customers VALUES ('C10035', 'Graham', 'David', 1);
INSERT INTO customers VALUES ('C10036', 'Young', 'Elizabeth', 0);
INSERT INTO customers VALUES ('C10037', 'Odonnell', 'Noah', 1);
INSERT INTO customers VALUES ('C10038', 'Dunn', 'Luis', 1);
INSERT INTO customers VALUES ('C10039', 'Burke', 'Diane', 0);
INSERT INTO customers VALUES ('C10040', 'Rivera', 'Hannah', 0);
INSERT INTO customers VALUES ('C10041', 'Diaz', 'Brent', 0);
INSERT INTO customers VALUES ('C10042', 'Howell', 'Jessica', 0);
INSERT INTO customers VALUES ('C10043', 'Harris', 'Christopher', 1);
INSERT INTO customers VALUES ('C10044', 'Turner', 'Kathryn', 1);
INSERT INTO customers VALUES ('C10045', 'Richardson', 'Amy', 0);
INSERT INTO customers VALUES ('C10046', 'Rose', 'Jennifer', 1);
INSERT INTO customers VALUES ('C10047', 'Wagner', 'Rachel', 1);
INSERT INTO customers VALUES ('C10048', 'Schmidt', 'Madison', 1);
INSERT INTO customers VALUES ('C10049', 'Arnold', 'Mark', 1);
INSERT INTO customers VALUES ('C10050', 'Frost', 'Gregory', 1);
INSERT INTO customers VALUES ('C10051', 'Matthews', 'Kevin', 1);
INSERT INTO customers VALUES ('C10052', 'Fitzgerald', 'Carlos', 1);
INSERT INTO customers VALUES ('C10053', 'Taylor', 'Ashley', 0);
INSERT INTO customers VALUES ('C10054', 'Moreno', 'Lisa', 1);

INSERT INTO doctors VALUES ('D10005', 'Romero', 'Mary');
INSERT INTO doctors VALUES ('D10006', 'Campbell', 'Christopher');
INSERT INTO doctors VALUES ('D10007', 'Mccarthy', 'Julie');
INSERT INTO doctors VALUES ('D10008', 'Gomez', 'Susan');
INSERT INTO doctors VALUES ('D10009', 'Mendez', 'Christopher');
INSERT INTO doctors VALUES ('D10010', 'Richardson', 'Robin');
INSERT INTO doctors VALUES ('D10011', 'Carter', 'Tracy');
INSERT INTO doctors VALUES ('D10012', 'Smith', 'Miranda');
INSERT INTO doctors VALUES ('D10013', 'Wang', 'Wendy');
INSERT INTO doctors VALUES ('D10014', 'Townsend', 'James');
INSERT INTO doctors VALUES ('D10015', 'Castro', 'Paul');
INSERT INTO doctors VALUES ('D10016', 'Ward', 'William');
INSERT INTO doctors VALUES ('D10017', 'Miller', 'Christian');
INSERT INTO doctors VALUES ('D10018', 'Anderson', 'Sarah');
INSERT INTO doctors VALUES ('D10019', 'Thomas', 'John');
INSERT INTO doctors VALUES ('D10020', 'Robinson', 'Alexandra');
INSERT INTO doctors VALUES ('D10021', 'Park', 'Allison');
INSERT INTO doctors VALUES ('D10022', 'Hunt', 'Courtney');
INSERT INTO doctors VALUES ('D10023', 'Chapman', 'Adam');
INSERT INTO doctors VALUES ('D10024', 'Johnson', 'Diane');
INSERT INTO doctors VALUES ('D10025', 'Powers', 'Regina');
INSERT INTO doctors VALUES ('D10026', 'Miller', 'Susan');
INSERT INTO doctors VALUES ('D10027', 'Manning', 'Brenda');
INSERT INTO doctors VALUES ('D10028', 'Diaz', 'Danielle');
INSERT INTO doctors VALUES ('D10029', 'Ferguson', 'Natalie');
INSERT INTO doctors VALUES ('D10030', 'Jensen', 'Kathleen');
INSERT INTO doctors VALUES ('D10031', 'Butler', 'Maria');
INSERT INTO doctors VALUES ('D10032', 'Rodriguez', 'David');
INSERT INTO doctors VALUES ('D10033', 'Velez', 'John');
INSERT INTO doctors VALUES ('D10034', 'Young', 'Beverly');
INSERT INTO doctors VALUES ('D10035', 'Walls', 'Cynthia');
INSERT INTO doctors VALUES ('D10036', 'James', 'Robert');
INSERT INTO doctors VALUES ('D10037', 'Yang', 'Sandra');
INSERT INTO doctors VALUES ('D10038', 'Martin', 'Sierra');
INSERT INTO doctors VALUES ('D10039', 'Rhodes', 'Yvonne');
INSERT INTO doctors VALUES ('D10040', 'Jones', 'Meagan');
INSERT INTO doctors VALUES ('D10041', 'Carr', 'Susan');
INSERT INTO doctors VALUES ('D10042', 'Whitehead', 'Lori');
INSERT INTO doctors VALUES ('D10043', 'Peters', 'Ashley');
INSERT INTO doctors VALUES ('D10044', 'Bishop', 'Casey');
INSERT INTO doctors VALUES ('D10045', 'Williams', 'Katie');
INSERT INTO doctors VALUES ('D10046', 'Hunter', 'Adam');
INSERT INTO doctors VALUES ('D10047', 'White', 'Rachel');
INSERT INTO doctors VALUES ('D10048', 'Brooks', 'Anna');
INSERT INTO doctors VALUES ('D10049', 'Johnson', 'Emily');
INSERT INTO doctors VALUES ('D10050', 'Mckenzie', 'Lauren');
INSERT INTO doctors VALUES ('D10051', 'Smith', 'Jorge');
INSERT INTO doctors VALUES ('D10052', 'Hamilton', 'Daniel');
INSERT INTO doctors VALUES ('D10053', 'Powers', 'Clinton');
INSERT INTO doctors VALUES ('D10054', 'Davis', 'Stanley');

INSERT INTO medSup VALUES ('A10005', 'B10052', 47, '2020-11-17', 20.63);
INSERT INTO medSup VALUES ('A10006', 'B10041', 20, '2021-04-13', 11.94);
INSERT INTO medSup VALUES ('A10007', 'B10042', 5, '2024-08-08', 18.0);
INSERT INTO medSup VALUES ('A10008', 'B10005', 46, '2020-07-11', 12.55);
INSERT INTO medSup VALUES ('A10009', 'B10035', 13, '2022-03-06', 3.03);
INSERT INTO medSup VALUES ('A10010', 'B10054', 15, '2023-11-19', 21.6);
INSERT INTO medSup VALUES ('A10011', 'B10015', 38, '2020-01-21', 19.21);
INSERT INTO medSup VALUES ('A10012', 'B10014', 49, '2021-11-13', 22.31);
INSERT INTO medSup VALUES ('A10013', 'B10040', 41, '2023-03-09', 9.49);
INSERT INTO medSup VALUES ('A10014', 'B10054', 36, '2024-03-07', 14.03);
INSERT INTO medSup VALUES ('A10015', 'B10008', 38, '2020-07-24', 11.38);
INSERT INTO medSup VALUES ('A10016', 'B10020', 8, '2022-05-28', 5.23);
INSERT INTO medSup VALUES ('A10017', 'B10022', 45, '2024-08-15', 8.08);
INSERT INTO medSup VALUES ('A10018', 'B10030', 20, '2020-07-24', 17.45);
INSERT INTO medSup VALUES ('A10019', 'B10021', 27, '2021-12-25', 4.57);
INSERT INTO medSup VALUES ('A10020', 'B10033', 33, '2022-04-20', 13.04);
INSERT INTO medSup VALUES ('A10021', 'B10049', 10, '2021-04-20', 3.03);
INSERT INTO medSup VALUES ('A10022', 'B10024', 9, '2024-09-19', 14.77);
INSERT INTO medSup VALUES ('A10023', 'B10032', 40, '2023-12-12', 18.4);
INSERT INTO medSup VALUES ('A10024', 'B10014', 15, '2022-10-18', 5.42);
INSERT INTO medSup VALUES ('A10025', 'B10018', 25, '2021-09-23', 10.41);
INSERT INTO medSup VALUES ('A10026', 'B10018', 9, '2024-12-12', 17.82);
INSERT INTO medSup VALUES ('A10027', 'B10016', 20, '2020-05-23', 3.7);
INSERT INTO medSup VALUES ('A10028', 'B10034', 29, '2024-08-08', 5.26);
INSERT INTO medSup VALUES ('A10029', 'B10011', 32, '2024-04-26', 10.46);
INSERT INTO medSup VALUES ('A10030', 'B10051', 41, '2022-10-10', 12.56);
INSERT INTO medSup VALUES ('A10031', 'B10041', 15, '2024-11-24', 12.97);
INSERT INTO medSup VALUES ('A10032', 'B10048', 44, '2023-10-02', 5.8);
INSERT INTO medSup VALUES ('A10033', 'B10043', 7, '2021-03-03', 11.68);
INSERT INTO medSup VALUES ('A10034', 'B10045', 16, '2021-04-24', 11.77);
INSERT INTO medSup VALUES ('A10035', 'B10014', 38, '2022-11-17', 3.36);
INSERT INTO medSup VALUES ('A10036', 'B10029', 26, '2023-03-24', 23.7);
INSERT INTO medSup VALUES ('A10037', 'B10027', 17, '2020-10-18', 20.61);
INSERT INTO medSup VALUES ('A10038', 'B10042', 7, '2024-10-21', 23.48);
INSERT INTO medSup VALUES ('A10039', 'B10036', 30, '2023-10-08', 14.27);
INSERT INTO medSup VALUES ('A10040', 'B10046', 38, '2021-10-31', 14.8);
INSERT INTO medSup VALUES ('A10041', 'B10012', 5, '2022-06-17', 21.1);
INSERT INTO medSup VALUES ('A10042', 'B10011', 20, '2023-11-28', 22.64);
INSERT INTO medSup VALUES ('A10043', 'B10017', 42, '2024-10-11', 11.97);
INSERT INTO medSup VALUES ('A10044', 'B10011', 30, '2020-09-17', 7.17);
INSERT INTO medSup VALUES ('A10045', 'B10018', 10, '2021-06-04', 15.29);
INSERT INTO medSup VALUES ('A10046', 'B10027', 14, '2023-11-29', 20.71);
INSERT INTO medSup VALUES ('A10047', 'B10052', 45, '2024-08-17', 13.14);
INSERT INTO medSup VALUES ('A10048', 'B10036', 7, '2020-12-18', 12.33);
INSERT INTO medSup VALUES ('A10049', 'B10006', 26, '2022-05-11', 17.12);
INSERT INTO medSup VALUES ('A10050', 'B10020', 47, '2021-04-20', 23.29);
INSERT INTO medSup VALUES ('A10051', 'B10026', 40, '2024-05-04', 4.52);
INSERT INTO medSup VALUES ('A10052', 'B10008', 43, '2024-08-12', 19.91);
INSERT INTO medSup VALUES ('A10053', 'B10031', 14, '2023-06-08', 9.76);
INSERT INTO medSup VALUES ('A10054', 'B10012', 13, '2021-01-26', 5.11);

INSERT INTO prescriptions VALUES ('E100005', 'C10025', 'A10041', 'D10049');
INSERT INTO prescriptions VALUES ('E100006', 'C10041', 'A10041', 'D10016');
INSERT INTO prescriptions VALUES ('E100007', 'C10013', 'A10017', 'D10036');
INSERT INTO prescriptions VALUES ('E100008', 'C10054', 'A10031', 'D10029');
INSERT INTO prescriptions VALUES ('E100009', 'C10022', 'A10054', 'D10015');
INSERT INTO prescriptions VALUES ('E100010', 'C10027', 'A10013', 'D10007');
INSERT INTO prescriptions VALUES ('E100011', 'C10047', 'A10011', 'D10043');
INSERT INTO prescriptions VALUES ('E100012', 'C10038', 'A10051', 'D10020');
INSERT INTO prescriptions VALUES ('E100013', 'C10039', 'A10005', 'D10024');
INSERT INTO prescriptions VALUES ('E100014', 'C10045', 'A10050', 'D10026');
INSERT INTO prescriptions VALUES ('E100015', 'C10005', 'A10048', 'D10034');
INSERT INTO prescriptions VALUES ('E100016', 'C10008', 'A10038', 'D10036');
INSERT INTO prescriptions VALUES ('E100017', 'C10035', 'A10030', 'D10046');
INSERT INTO prescriptions VALUES ('E100018', 'C10051', 'A10006', 'D10007');
INSERT INTO prescriptions VALUES ('E100019', 'C10018', 'A10047', 'D10041');
INSERT INTO prescriptions VALUES ('E100020', 'C10014', 'A10027', 'D10032');
INSERT INTO prescriptions VALUES ('E100021', 'C10027', 'A10029', 'D10034');
INSERT INTO prescriptions VALUES ('E100022', 'C10024', 'A10016', 'D10032');
INSERT INTO prescriptions VALUES ('E100023', 'C10011', 'A10047', 'D10043');
INSERT INTO prescriptions VALUES ('E100024', 'C10053', 'A10043', 'D10010');
INSERT INTO prescriptions VALUES ('E100026', 'C10037', 'A10024', 'D10044');
INSERT INTO prescriptions VALUES ('E100027', 'C10044', 'A10036', 'D10047');
INSERT INTO prescriptions VALUES ('E100028', 'C10005', 'A10048', 'D10049');
INSERT INTO prescriptions VALUES ('E100029', 'C10028', 'A10052', 'D10026');
INSERT INTO prescriptions VALUES ('E100030', 'C10047', 'A10051', 'D10012');
INSERT INTO prescriptions VALUES ('E100031', 'C10035', 'A10016', 'D10010');
INSERT INTO prescriptions VALUES ('E100032', 'C10046', 'A10029', 'D10029');
INSERT INTO prescriptions VALUES ('E100033', 'C10009', 'A10046', 'D10049');
INSERT INTO prescriptions VALUES ('E100034', 'C10045', 'A10012', 'D10040');
INSERT INTO prescriptions VALUES ('E100035', 'C10047', 'A10049', 'D10024');
INSERT INTO prescriptions VALUES ('E100036', 'C10044', 'A10006', 'D10043');
INSERT INTO prescriptions VALUES ('E100037', 'C10051', 'A10011', 'D10044');
INSERT INTO prescriptions VALUES ('E100038', 'C10016', 'A10053', 'D10018');
INSERT INTO prescriptions VALUES ('E100039', 'C10005', 'A10034', 'D10010');
INSERT INTO prescriptions VALUES ('E100040', 'C10046', 'A10027', 'D10018');
INSERT INTO prescriptions VALUES ('E100041', 'C10018', 'A10037', 'D10018');
INSERT INTO prescriptions VALUES ('E100042', 'C10009', 'A10039', 'D10041');
INSERT INTO prescriptions VALUES ('E100043', 'C10044', 'A10046', 'D10015');
INSERT INTO prescriptions VALUES ('E100044', 'C10028', 'A10050', 'D10043');
INSERT INTO prescriptions VALUES ('E100045', 'C10048', 'A10019', 'D10009');
INSERT INTO prescriptions VALUES ('E100046', 'C10040', 'A10050', 'D10026');
INSERT INTO prescriptions VALUES ('E100047', 'C10009', 'A10035', 'D10049');
INSERT INTO prescriptions VALUES ('E100048', 'C10048', 'A10015', 'D10050');
INSERT INTO prescriptions VALUES ('E100049', 'C10011', 'A10032', 'D10045');
INSERT INTO prescriptions VALUES ('E100050', 'C10047', 'A10018', 'D10037');
INSERT INTO prescriptions VALUES ('E100051', 'C10030', 'A10045', 'D10050');
INSERT INTO prescriptions VALUES ('E100052', 'C10054', 'A10012', 'D10023');
INSERT INTO prescriptions VALUES ('E100054', 'C10035', 'A10010', 'D10038');

INSERT INTO sales VALUES ('F10005', '2023-11-29', 6, 66.96, 'A10021', 'C10008', 'E100019', 'E-wallet', 0.0);
INSERT INTO sales VALUES ('F10006', '2023-04-19', 5, 133.4, 'A10010', 'C10007', 'E100044', 'Card', 0.0);
INSERT INTO sales VALUES ('F10007', '2022-02-07', 1, 39.62, 'A10039', 'C10021', 'E100019', 'Cash', 0.2);
INSERT INTO sales VALUES ('F10008', '2024-07-27', 5, 199.36, 'A10043', 'C10024', 'E100026', 'E-wallet', 0.2);
INSERT INTO sales VALUES ('F10009', '2022-06-23', 1, 47.29, 'A10050', 'C10010', 'E100023', 'E-wallet', 0.0);
INSERT INTO sales VALUES ('F10010', '2022-06-07', 4, 98.4, 'A10045', 'C10051', 'E100010', 'Cash', 0.2);
INSERT INTO sales VALUES ('F10011', '2023-04-23', 1, 37.3, 'A10020', 'C10013', 'E100029', 'Cash', 0.2);
INSERT INTO sales VALUES ('F10012', '2024-04-09', 2, 34.61, 'A10006', 'C10038', 'E100009', 'Card', 0.2);
INSERT INTO sales VALUES ('F10013', '2024-11-27', 6, 220.62, 'A10027', 'C10014', 'E100014', 'E-wallet', 0.0);
INSERT INTO sales VALUES ('F10014', '2023-04-14', 5, 59.45, 'A10012', 'C10023', 'E100005', 'Card', 0.0);
INSERT INTO sales VALUES ('F10015', '2023-04-04', 5, 144.7, 'A10008', 'C10014', 'E100023', 'Card', 0.0);
INSERT INTO sales VALUES ('F10016', '2023-05-15', 3, 50.59, 'A10016', 'C10047', 'E100011', 'Card', 0.2);
INSERT INTO sales VALUES ('F10017', '2024-01-11', 5, 249.2, 'A10036', 'C10040', 'E100015', 'E-wallet', 0.0);
INSERT INTO sales VALUES ('F10018', '2023-09-18', 5, 199.36, 'A10048', 'C10006', 'E100028', 'Card', 0.2);
INSERT INTO sales VALUES ('F10019', '2023-12-29', 6, 255.48, 'A10016', 'C10011', 'E100009', 'Cash', 0.0);
INSERT INTO sales VALUES ('F10020', '2023-08-10', 2, 83.96, 'A10015', 'C10032', 'E100018', 'Cash', 0.0);
INSERT INTO sales VALUES ('F10021', '2022-07-14', 1, 13.26, 'A10029', 'C10049', 'E100009', 'E-wallet', 0.2);
INSERT INTO sales VALUES ('F10022', '2024-12-22', 6, 139.8, 'A10015', 'C10019', 'E100037', 'E-wallet', 0.0);
INSERT INTO sales VALUES ('F10023', '2022-08-25', 3, 111.72, 'A10015', 'C10029', 'E100018', 'E-wallet', 0.0);
INSERT INTO sales VALUES ('F10024', '2022-06-23', 8, 266.24, 'A10046', 'C10054', 'E100049', 'Cash', 0.2);
INSERT INTO sales VALUES ('F10025', '2023-01-30', 5, 240.55, 'A10034', 'C10008', 'E100048', 'Cash', 0.0);
INSERT INTO sales VALUES ('F10026', '2023-10-23', 2, 73.54, 'A10029', 'C10034', 'E100047', 'Card', 0.0);
INSERT INTO sales VALUES ('F10027', '2022-04-05', 5, 52.8, 'A10010', 'C10049', 'E100024', 'E-wallet', 0.2);
INSERT INTO sales VALUES ('F10028', '2023-07-04', 5, 237.9, 'A10009', 'C10030', 'E100052', 'Card', 0.0);
INSERT INTO sales VALUES ('F10029', '2023-01-03', 4, 123.0, 'A10013', 'C10008', 'E100007', 'Card', 0.0);
INSERT INTO sales VALUES ('F10030', '2024-05-07', 6, 66.96, 'A10026', 'C10034', 'E100039', 'Cash', 0.0);
INSERT INTO sales VALUES ('F10031', '2024-04-24', 7, 217.28, 'A10051', 'C10052', 'E100044', 'Card', 0.2);
INSERT INTO sales VALUES ('F10032', '2022-10-20', 8, 223.94, 'A10035', 'C10052', 'E100011', 'Card', 0.2);
INSERT INTO sales VALUES ('F10033', '2022-02-09', 8, 268.67, 'A10040', 'C10005', 'E100014', 'E-wallet', 0.2);
INSERT INTO sales VALUES ('F10034', '2022-07-26', 3, 33.45, 'A10027', 'C10040', 'E100045', 'Card', 0.0);
INSERT INTO sales VALUES ('F10035', '2022-09-08', 10, 111.6, 'A10021', 'C10041', 'E100043', 'Cash', 0.0);
INSERT INTO sales VALUES ('F10036', '2023-02-18', 7, 151.69, 'A10030', 'C10041', 'E100054', 'E-wallet', 0.0);
INSERT INTO sales VALUES ('F10037', '2024-10-02', 6, 71.34, 'A10036', 'C10015', 'E100020', 'Cash', 0.0);
INSERT INTO sales VALUES ('F10038', '2023-05-28', 1, 37.24, 'A10015', 'C10023', 'E100015', 'Card', 0.0);
INSERT INTO sales VALUES ('F10039', '2022-06-13', 9, 334.62, 'A10051', 'C10023', 'E100054', 'Card', 0.0);
INSERT INTO sales VALUES ('F10040', '2023-09-12', 10, 466.3, 'A10022', 'C10032', 'E100054', 'Cash', 0.0);
INSERT INTO sales VALUES ('F10041', '2023-08-09', 2, 93.02, 'A10047', 'C10015', 'E100013', 'E-wallet', 0.0);
INSERT INTO sales VALUES ('F10042', '2023-11-23', 8, 89.2, 'A10050', 'C10042', 'E100016', 'Cash', 0.0);
INSERT INTO sales VALUES ('F10043', '2022-12-01', 2, 90.18, 'A10040', 'C10008', 'E100028', 'Cash', 0.0);
INSERT INTO sales VALUES ('F10044', '2024-01-29', 9, 181.3, 'A10019', 'C10017', 'E100045', 'Cash', 0.2);
INSERT INTO sales VALUES ('F10045', '2024-12-17', 9, 124.13, 'A10029', 'C10046', 'E100022', 'Card', 0.2);
INSERT INTO sales VALUES ('F10046', '2024-08-02', 1, 38.66, 'A10020', 'C10026', 'E100020', 'Card', 0.2);
INSERT INTO sales VALUES ('F10047', '2024-07-27', 9, 335.16, 'A10015', 'C10009', 'E100026', 'E-wallet', 0.0);
INSERT INTO sales VALUES ('F10048', '2024-06-28', 7, 121.35, 'A10045', 'C10038', 'E100035', 'E-wallet', 0.2);
INSERT INTO sales VALUES ('F10049', '2023-07-10', 9, 240.12, 'A10024', 'C10028', 'E100006', 'Cash', 0.0);
INSERT INTO sales VALUES ('F10050', '2024-01-22', 9, 306.58, 'A10037', 'C10021', 'E100051', 'E-wallet', 0.2);
INSERT INTO sales VALUES ('F10051', '2022-07-04', 2, 77.6, 'A10039', 'C10012', 'E100028', 'E-wallet', 0.0);
INSERT INTO sales VALUES ('F10052', '2022-10-24', 8, 95.12, 'A10007', 'C10020', 'E100019', 'Cash', 0.0);
INSERT INTO sales VALUES ('F10053', '2023-12-01', 8, 202.64, 'A10038', 'C10009', 'E100011', 'Card', 0.0);
INSERT INTO sales VALUES ('F10054', '2022-01-12', 4, 199.36, 'A10026', 'C10007', 'E100038', 'E-wallet', 0.0);