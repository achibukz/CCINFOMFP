CREATE TABLE suppliers (
    supID VARCHAR(50) PRIMARY KEY,
    supName VARCHAR(100) NOT NULL,
    contact VARCHAR(50)
);

CREATE TABLE medicines (
    medID VARCHAR(50) PRIMARY KEY,
    medName VARCHAR(50) NOT NULL,
    medType VARCHAR(255),
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE medSup (
    medID VARCHAR(50),
    supID VARCHAR(50),
    dosage VARCHAR(50),
    expiry_date DATE,
    stockBought INT NOT NULL,
    dateBought DATE,
    priceBought DECIMAL(10,2) NOT NULL,
    PRIMARY KEY(medID, supID),
    FOREIGN KEY (medID) REFERENCES medicines(medID) ON DELETE CASCADE,
    FOREIGN KEY (supID) REFERENCES suppliers(supID) ON DELETE CASCADE
);

CREATE TABLE customers (
    customerID VARCHAR(50) PRIMARY KEY,
    customerLastName VARCHAR(50) NOT NULL,
    customerFirstName VARCHAR(50) NOT NULL,
    HasDisCard INT
);

CREATE TABLE doctors (
    docID VARCHAR(50) PRIMARY KEY,
    doctorLastName VARCHAR(50) NOT NULL,
    doctorFirstName VARCHAR(50) NOT NULL
);

CREATE TABLE prescriptions (
    presID VARCHAR(50) PRIMARY KEY,
    customerID VARCHAR(50),
    medID VARCHAR(50),
    docID VARCHAR(50),
    FOREIGN KEY (medID) REFERENCES medicines(medID) ON DELETE CASCADE,
    FOREIGN KEY (customerID) REFERENCES customers(customerID) ON DELETE CASCADE,
    FOREIGN KEY (docID) REFERENCES doctors(docID) ON DELETE CASCADE
);

CREATE TABLE sales (
    salesID VARCHAR(50) PRIMARY KEY,
    salesDate DATE,
    quantitySold INT,
    totalPrice DECIMAL(10,2),
    medID VARCHAR(50),
    customerID VARCHAR(50),
    presID VARCHAR(50),
    mOP VARCHAR(50),
    discount FLOAT,
    FOREIGN KEY (medID) REFERENCES medicines(medID) ON DELETE CASCADE,
    FOREIGN KEY (customerID) REFERENCES customers(customerID) ON DELETE CASCADE,
    FOREIGN KEY (presID) REFERENCES prescriptions(presID) ON DELETE CASCADE
);

INSERT INTO suppliers (supID, supName, contact) VALUES
('B10005', 'Andrews-White', '09171234567'),
('B10006', 'Greene-Williams', '09181234568'),
('B10007', 'Fisher, Diaz and Walker', '09191234569');

INSERT INTO medicines (medID, medName, medType, price) VALUES
('A10001', 'Paracetamol', 'OTC', 49.45),
('A10002', 'Ibuprofen', 'OTC', 46.51),
('A10003', 'Cetirizine', 'OTC', 25.33);

INSERT INTO medSup (medID, supID, dosage, expiry_date, stockBought, dateBought, priceBought) VALUES
('A10001', 'B10005', '500mg', '2026-12-30', 100, '2023-11-10', 45.00),
('A10002', 'B10006', '200mg', '2027-01-15', 200, '2023-11-15', 42.00),
('A10003', 'B10007', '10mg', '2026-11-20', 150, '2023-11-18', 22.00);

INSERT INTO customers (customerID, customerLastName, customerFirstName, HasDisCard) VALUES
('C10001', 'Green', 'Joshua', 1),
('C10002', 'Cline', 'Christopher', 1),
('C10003', 'Powers', 'Zachary', 0);

INSERT INTO doctors (docID, doctorLastName, doctorFirstName) VALUES
('D10001', 'Romero', 'Mary'),
('D10002', 'Campbell', 'Christopher'),
('D10003', 'Mccarthy', 'Julie');

INSERT INTO prescriptions (presID, customerID, medID, docID) VALUES
('E10001', 'C10001', 'A10001', 'D10001'),
('E10002', 'C10002', 'A10002', 'D10002'),
('E10003', 'C10003', 'A10003', 'D10003');

INSERT INTO sales (salesID, salesDate, quantitySold, totalPrice, medID, customerID, presID, mOP, discount) VALUES
('F10001', '2023-01-01', 2, 98.90, 'A10001', 'C10001', 'E10001', 'Cash', 0.20),
('F10002', '2023-02-15', 1, 46.51, 'A10002', 'C10002', 'E10002', 'E-wallet', 0.20),
('F10003', '2023-03-10', 3, 75.99, 'A10003', 'C10003', 'E10003', 'Card', 0.00);
