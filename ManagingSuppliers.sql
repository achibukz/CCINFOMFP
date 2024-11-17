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

-- Deleting the supplier record if the supplier no longer provide any medicines
DELETE s
FROM suppliers s
LEFT JOIN medSup ms ON s.supplierId = ms.supplierId
WHERE ms.supplierId IS NULL;

-- Supplier Report (Supplier ID, Supplier Name, Contact, Medicines Supplied) for a given Year and Month. 
SELECT 
    s.supplierId AS "Supplier ID",
    s.name AS "Supplier Name",
    s.contact AS "Contact",
    GROUP_CONCAT(m.name SEPARATOR ', ') AS "Medicines Supplied"
FROM suppliers s
JOIN medSup ms ON s.supplierId = ms.supplierId
JOIN medicines m ON ms.medId = m.medId
WHERE YEAR(ms.dateOfPurch) = '%s'  AND MONTH(ms.dateOfPurch) = '%s'
GROUP BY s.supplierId, s.name, s.contact;