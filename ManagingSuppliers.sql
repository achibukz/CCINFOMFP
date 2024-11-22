
--Creating a new supplier record
-- no supplier ID as it is automatically created
INSERT INTO suppliers (name, contact)
VALUES ('%s', '%s');

-- Reading the supplier record to check if the supplier provides a specific type of medicine
SELECT s.supplierId, s.name, s.contact
FROM suppliers s
JOIN medSup ms ON s.supplierId = ms.supplierId
JOIN medicines m ON ms.medId = m.medId
WHERE m.medType = '%s';

-- Updating the supplier record if there is a change in the supplier’s details
UPDATE suppliers
SET name = '%s',
    contact = '%s'
WHERE supplierId = '%s';

--Delete supplier Record
DELETE 
FROM suppliers
WHERE supplierId = '%s' AND name = '%s';


-- Supplier Report (Supplier ID, Supplier Name, Contact, Medicines Supplied) for a given Year and Month. 
SELECT 
    s.supplierId AS "Supplier ID",
    s.name AS "Supplier Name",
    s.contact AS "Contact",
    GROUP_CONCAT(m.name SEPARATOR ', ') AS "Medicines Supplied"
    GROUP_CONCAT(ms.dateOfPurch SEPARATOR ', ') AS "Date of Purchase"
FROM suppliers s
JOIN medSup ms ON s.supplierId = ms.supplierId
JOIN medicines m ON ms.medId = m.medId
WHERE YEAR(ms.dateOfPurch) = '%s'  AND MONTH(ms.dateOfPurch) = '%s'
GROUP BY s.supplierId, s.name, s.contact;

--not sure if needed

-- Deleting the supplier record if the supplier no longer provide any medicines
DELETE s
FROM suppliers s
LEFT JOIN medSup ms ON s.supplierId = ms.supplierId
WHERE ms.supplierId IS NULL;


