-- Creating a new sales record for every transaction (Is this needed/necessary pa ba?)

-- Reading the customer record to check the type of medication (over-the-counter or prescription)
SELECT c.customerId, c.customerLastName, c.customerFirstName,
	CASE
		WHEN p.presId IS NOT NULL THEN 'Prescription'
        ELSE 'Over-the-Counter'
	END AS MedType
FROM customers c
LEFT JOIN prescriptions p ON c.customerId = p.customerId
WHERE c.customerId = '%s';

-- Reading the prescription record to check if the customer is allowed to buy the medicine
SELECT presId
FROM prescriptions
WHERE presId = '%s' AND customerId = '%s' AND medId = '%s';

-- Reading the medicine record to check the details of medicines to be sold (e.g. dosage, availability, price per piece)
SELECT medId, name, dosage, expiry_date, medType, inStock, price
FROM medicines
WHERE medId = '%s';

-- Recording the transaction with the sale date, total amount of medicine sold, discount, and total price
INSERT INTO sales (salesID, salesDate, quantitySold, totalPrice, medId, customerId, presId, mOP, discount)
VALUES ('%s', CURDATE(), ?, ?, '%s', '%s', '%s', '%s', ?);
-- Need na ba dito yung computation for total price or ...

-- Updating medicine records to deduct medications bought by a customer
UPDATE medicines
SET inStock = inStock - ?
WHERE medId = '%s';

-- Deleting a sales record to be voided
DELETE 
FROM sales
WHERE salesID = '%s';
-- Added this to bring back the stock since voided transaction
UPDATE medicines
SET inStock = inStock + ?
WHERE medId = '%s';

-- Sales Report (Quantity sold, Sold ID, Sale ID, Medicine ID, Customer ID) for a given Year and Month. 
SELECT s.salesID, s.quantitySold, s.medId, m.name, s.customerId, c.customerLastName, c.customerFirstName
FROM sales s
JOIN medicines m ON s.medId = m.medId
JOIN customers c ON s.customerId = c.customerId
WHERE YEAR(s.salesDate) = ? AND MONTH(s.salesDate) = ?
ORDER BY s.salesDate;