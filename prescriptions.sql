--Create new presc record--
INSERT INTO prescriptions (p.presId)
VALUES (%s);

INSERT INTO customers (customerId, customerLastName, customerFirstName)
VALUES (%s, %s, %s);

INSERT INTO medicines (medId, name)
VALUES(%s, %s)

INSERT INTO doctors (docId, doctorLastName, doctorFirstName)
VALUES (%s, %s, %s);

--Reading the customer record to check if the customer is existing or not--
SELECT * 
FROM customers
WHERE customerId = %s;

--Updating the prescription to change to a new prescription of a customer--
UPDATE prescriptions p
JOIN customers c ON p.customerId = c.customerId
SET p.medId = %s
WHERE p.presId = %s AND c.customerFirstName = %s AND c.customerLastName = %s;

--Deleting the prescription record of a customer if not or no longer valid--
DELETE FROM prescriptions
WHERE presId = %s;

--Prescription record Report--
SELECT 
    p.presId,
    c.customerId,
    CONCAT(c.customerLastName, ', ', c.customerFirstName) AS CustomerName,
    m.medId,
    m.name,
    CONCAT(d.doctorLastName, ', ', d.doctorFirstName) AS DoctorName,
FROM Prescription p
JOIN customers c ON p.customerID = c.customerID
JOIN medicines m ON p.medId = m.medId
JOIN doctors d ON p.docID = d.docID
WHERE YEAR(p.dateIssued) = %s AND MONTH(p.dateIssued) = %s;

