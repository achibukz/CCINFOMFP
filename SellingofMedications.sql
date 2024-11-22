-- Universal command to check if an ID is existing in other tables
SELECT 'Medicines' AS Table_Name, md.medID AS ID
FROM medicines md
WHERE md.medID = '%s'
UNION
SELECT 'Suppliers' AS Table_Name, sp.supID AS ID
FROM suppliers sp
WHERE sp.supID = '%s'
UNION
SELECT 'Sales' AS Table_Name, sl.salesID AS ID
FROM sales sl
WHERE sl.salesID = '%s'
UNION
SELECT 'Prescriptions' AS Table_Name, pr.presID AS ID
FROM prescriptions pr
WHERE pr.presID = '%s'
UNION
SELECT 'Doctors' AS Table_Name, dc.docID AS ID
FROM doctors dc
WHERE dc.docID = '%s'
UNION
SELECT 'Customers' AS Table_Name, ct.customerID AS ID
FROM customers ct
WHERE ct.customerID = '%s';

-- Reading the customer record to check the type of medication (over-the-counter or prescription)
SELECT ct.customerID, ct.customerLastName, ct.customerFirstName,
	CASE
		WHEN pr.presID IS NOT NULL THEN 'Prescription'
        ELSE 'Over-the-Counter'
	END AS MedType
FROM customers ct
LEFT JOIN prescriptions pr ON ct.customerID = pr.customerID
WHERE ct.customerID = '%s';

-- Reading the prescription record to check if the customer is allowed to buy the medicine
SELECT presID
FROM prescriptions pr
JOIN customers ct ON pr.customerID = ct.customerID
JOIN medicines md ON pr.medID = md.medID
JOIN medSup ms ON pr.medID = ms.medID
WHERE pr.presID = '%s' AND ct.customerID = '%s' AND md.medID = '%s' AND ms.dosage = '%s' AND ms.expiry_date = '%s';

-- Reading the medicine record to check the details of medicines to be sold (e.g. dosage, availability, price per piece)
SELECT medID, name, dosage, expiry_date, medType, stockBought, price
FROM medicines
WHERE medID = '%s' AND dosage = '%s';

-- Recording the transaction with the sale date, total amount of medicine sold, discount, and total price
INSERT INTO sales (salesID, salesDate, quantitySold, totalPrice, medID, customerID, presID, mOP, discount)
VALUES ('%s', CURDATE(), ?, ?, '%s', '%s', '%s', '%s', ?);

-- Updating medicine records to deduct medications bought by a customer
UPDATE medicines
SET stockBought = stockBought - ?
WHERE medID = '%s';

-- Deleting a sales record to be voided
DELETE 
FROM sales
WHERE salesID = '%s';
-- Added this to bring back the stock since voided transaction
UPDATE medicines
SET stockBought = stockBought + ?
WHERE medID = '%s';

-- Check if stock is enough
SELECT stockBought
FROM medSup
WHERE medID = '%s' AND stockBought >= '%s';

-- Sales Report for a given Year and Month. 
SELECT sl.salesID, sl.salesDate, md.medName, ms.dosage, ct.customerLastName, ct.customerFirstName, sl.quantitySold, sl.mOP, sl.totalPrice, sl.discount
FROM sales sl
JOIN medicines md ON sl.medID = md.medID
JOIN medSup ms ON ms.medID = md.medID
JOIN customers ct ON sl.customerID = ct.customerID
WHERE YEAR(sl.salesDate) = ? AND MONTH(sl.salesDate) = ?
ORDER BY sl.salesDate;
