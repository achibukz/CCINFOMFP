SELECT *
FROM medicines

DELETE FROM medicines
WHERE medID = 'A10004';

DELETE FROM medsup
WHERE medID = 'A10004';

SELECT *
FROM medsup