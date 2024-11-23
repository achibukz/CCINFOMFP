SELECT *
FROM medicines

DELETE FROM medicines
WHERE medID = 'A10004';

DELETE FROM medsup
WHERE medID = 'A10004';

SELECT *
FROM suppliers

SELECT *
FROM prescriptions

DELETE FROM prescriptions
WHERE presID = 'E10006';

UPDATE prescriptions
SET presID = CONCAT('E', LPAD(SUBSTRING(presID, 2) + 0, 5, '0'))
WHERE LENGTH(presID) = 7;

SELECT *
FROM sales


DELETE FROM sales
WHERE salesID LIKE 'S%';