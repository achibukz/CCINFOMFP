
--Creating a new supplier record
-- no supplier ID as it is automatically created
INSERT INTO suppliers (supName, contact)
VALUES ('%s', '%s');

-- Updating the supplier record if there is a change in the supplier’s details
UPDATE suppliers
SET supName = '%s',
    contact = '%s'
WHERE supId = '%s';

--Delete supplier Record
DELETE 
FROM suppliers
WHERE supId = '%s' AND supName = '%s';

--View for sql commands(TABLE)

SELECT 
    m.medName AS "Medicine Name",
    ms.dosage AS "Dosage",
    SUM(ms.stockBought) AS "InStock", 
    ms.dateBought AS "Date Bought",
    ms.priceBought AS "Price Bought"
FROM medicines m
JOIN medSup ms ON m.medID = ms.medID
JOIN suppliers s ON ms.supID = s.supID  
WHERE s.supID = '%s'  
AND s.supName = '%s'
GROUP BY m.medID, ms.dosage, ms.dateBought, ms.priceBought
ORDER BY ms.dateBought DESC;  

--View table by itself(suppliers)
SELECT supId, supName, contact
FROM suppliers;


-- Supplier Report (Supplier ID, Supplier Name, Contact, Medicines Supplied) for a given Year and Month. 
SELECT 
    s.supId AS "Supplier ID",
    s.supName AS "Supplier Name",
    s.contact AS "Contact",
    GROUP_CONCAT(m.medname SEPARATOR ', ') AS "Medicines Supplied",
    GROUP_CONCAT(ms.datebought SEPARATOR ', ') AS "Date of Purchase"
FROM suppliers s
JOIN medSup ms ON s.supId = ms.supId
JOIN medicines m ON ms.medId = m.medId
WHERE YEAR(ms.datebought) = '%s'  AND MONTH(ms.datebought) = '%s'
GROUP BY s.supId, s.supName, s.contact;

--not sure if needed

-- Deleting the supplier record if the supplier no longer provide any medicines
DELETE s
FROM suppliers s
LEFT JOIN medSup ms ON s.supId = ms.supId
WHERE ms.supId IS NULL;

-- Reading the supplier record to check if the supplier provides a specific type of medicine
SELECT s.supId, s.supName, s.contact
FROM suppliers s
JOIN medSup ms ON s.supplierId = ms.supplierId
JOIN medicines m ON ms.medId = m.medId
WHERE m.medType = '%s';


