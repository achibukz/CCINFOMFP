--Create new presc record--
INSERT INTO prescriptions (presId, customerId, medId, docId)
VALUES (%s, %s, %s, %s);

--Updating the prescription to change to a new prescription of a customer--
UPDATE prescriptions p
JOIN medSup m ON m.medId = p.medId
SET p.medName = %s
WHERE p.presId = %s;

UPDATE prescriptions p
JOIN medSup m ON m.medId = p.medId
SET p.dosage = %s
WHERE p.presId = %s;

UPDATE prescriptions p
JOIN doctors d ON d.docId = p.docId
SET p.doctorFirstName = %s
WHERE p.presId = %s;

UPDATE prescriptions p
JOIN doctors d ON d.docId = p.docId
SET p.doctorLastName = %s
WHERE p.presId = %s;

--Deleting the prescription record of a customer if not or no longer valid--
DELETE FROM prescriptions
WHERE presId = %s;

--Prescription record Report--
SELECT 
    p.presId,
    CONCAT(c.customerLastName, ', ', c.customerFirstName) AS CustomerName,
    m.medName, 
    m.dosage,
    CONCAT(d.doctorLastName, ', ', d.doctorFirstName) AS DoctorName,
FROM prescriptions p
JOIN customers c ON p.customerId = c.customerId
JOIN medSup m ON p.medId = m.medId
JOIN doctors d ON p.docId = d.docId
WHERE YEAR(p.dateIssued) = %s AND MONTH(p.dateIssued) = %s
ORDER BY presId;


--SQL commands for viewing tables--
SELECT DISTINCT CONCAT(c.customerLastName,', ', c.customerFirstName) AS CustomerName
FROM prescriptions p
JOIN customers c ON c.customerId = p.customerId;

SELECT presId
FROM prescriptions
JOIN customers c ON c.customerId = p.customerId
WHERE c.customerFirstName = (SELECT customerFirstName
                              FROM prescriptions)
  AND c.customerLastName = (SELECT customerLastName
                              FROM prescriptions);

SELECT DISTINCT m.medName
FROM prescriptions p
LEFT JOIN medSup m ON m.medId = p.medId;

SELECT m.dosage
FROM prescriptions p
JOIN medSup m ON m.medId = p.medId
WHERE m.medName = (SELECT medName 
                FROM prescriptions);

SELECT DISTINCT CONCAT(d.doctorLastName, ', ', d.doctorFirstName) AS DoctorName
FROM prescriptions p
LEFT JOIN doctors d ON d.docID = p.docID;
