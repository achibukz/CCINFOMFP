import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import mysql.connector as sql
from datetime import date
from decimal import Decimal

connection = None
onTable = None
arrF = []  

#----------------------------------------- UNIVERSAL FUNCTIONS -----------------------------------------#

def showFrame(nextF):
    # REMEMBER TO ADD NEW FRAMES TO THIS LIST
    listF = [loginF, mainMenuF, medMenuF, medTableF, cusMenuF,cusTableF, docMenuF, docTableF, presMenuF, presTableF, saleMenuF, saleTableF, supMenuF, supTableF, addMedicineF
             , updateMedicineF, deleteMedicineF, lowStockF, expirationDatesF, inventoryReportF, createCustomerF, createDoctorF, createSupplierF
             , updateCustomerF, updateSupplierF, updateDoctorF, deleteCustomerF, deleteDoctorF, deleteSupplierF, addPrescriptionF, updatePrescriptionF, viewTableF, deletePrescriptionF
             , selectCustomerF, selectOTCMedicineF, selectPrescriptionMedicineF, confirmSaleF, deleteSalesF, generateReportF]

    if not arrF or nextF != arrF[-1]:
        arrF.append(nextF)
    for frame in listF:
        frame.pack_forget()
    nextF.pack(fill="both", expand=True)

def goBack():
    if len(arrF) > 1: 
        arrF.pop()  
        prevF = arrF[-1]
        showFrame(prevF)

def connectServer():
    global connection
    try:
        connection = sql.connect(
            host=hostInput.get(),
            user=userInput.get(),
            password=passInput.get(),
            database="maindbpharma"
        )
        msg.showinfo("Success", "Connected to your Database.")
        showFrame(mainMenuF) 
        getTables()
    except sql.Error as e:
        msg.showerror("Error", f"Failed to connect to the database: {e}")
    except Exception as e:
        msg.showerror("Error", f"Unexpected error occurred: {e}")

def getTables():
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        tableDisplay.delete(0, tk.END)
        for table in tables:
            if table[0] != "medsup":
                tableDisplay.insert(tk.END, table[0])
    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch tables: {e}")

def selectTable():
    global onTable
    select = tableDisplay.curselection()
    if not select:
        msg.showerror("Error", "Please select a table.")
        return
    onTable = tableDisplay.get(select)

    tableFrame = {
        "medicines": medMenuF,
        "customers": cusMenuF,
        "doctors": docMenuF,
        "prescriptions": presMenuF,
        "sales": saleMenuF,
        "suppliers": supMenuF,
    }

    nextFrame = tableFrame.get(onTable)
    showFrame(nextFrame) 

def letterKeyRemover(Id):
    num = ''.join(filter(str.isdigit, Id))  
    return int(num) if num else 0 

def checkIDExists(id):
    try:
        cursor = connection.cursor()

        if id.startswith("A"):
            mainTab = "medID"
            tables_to_check = [
                "prescriptions",
                "sales"
            ]
        elif id.startswith("B"):
            mainTab = "supID"
            tables_to_check = [
                "medSup"
            ]
        elif id.startswith("C"):
            mainTab = "customerID"
            tables_to_check = [
                "prescriptions",
                "sales"
            ]
        elif id.startswith("D"):
            mainTab = "docID"
            tables_to_check = [
                "prescriptions"
            ]
        elif id.startswith("E"):
            mainTab = "presID"
            tables_to_check = [
                "sales"
            ]
        else:
            msg.showerror("Error", "Invalid ID format.")
            return 0

        for table in tables_to_check:
            query = f"SELECT COUNT(*) FROM {table} WHERE {mainTab} = %s;"
            cursor.execute(query, (id,))
            if cursor.fetchone()[0] > 0:
                return 1  

        return 0  

    except sql.Error as e:
        msg.showerror("Error", f"Failed to check ID existence: {e}")
        return 0

def getDeletableIDs(table_name, id_prefix):
    try:
        cursor = connection.cursor()
        query = f"SELECT {id_prefix}, CONCAT({table_name[:-1]}FirstName, ' ', {table_name[:-1]}LastName) AS fullName FROM {table_name};"
        cursor.execute(query)
        all_ids = cursor.fetchall()

        deletable_ids = []
        for row in all_ids:
            id = row[0]
            if not checkIDExists(id):  # Check if the ID is not referenced in other tables
                deletable_ids.append(f"{id} - {row[1]}")
        
        return deletable_ids
    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch deletable IDs: {e}")
        return []

def viewTable(table_type):
    """
    View details for the selected table type: customers, suppliers, doctors, or sales.

    Args:
        table_type (str): The type of table to view ('customers', 'suppliers', 'doctors', 'sales').
    """
    try:
        cursor = connection.cursor()

        if table_type == "customers":
            query = """
                SELECT customerID, customerLastName, customerFirstName, 
                       CASE WHEN HasDisCard = 1 THEN 'Yes' ELSE 'No' END AS HasDiscountCard
                FROM customers;
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = ["Customer ID", "Last Name", "First Name", "Has Discount Card"]

        elif table_type == "suppliers":
            query = """
                SELECT s.supID AS SupplierID, s.supName AS SupplierName,
                       m.medName AS MedicineName, ms.dosage AS Dosage, 
                       ms.stockBought AS StockBought, ms.dateBought AS DateBought, 
                       ms.priceBought AS PriceBought
                FROM suppliers s
                LEFT JOIN medSup ms ON s.supID = ms.supID
                LEFT JOIN medicines m ON ms.medID = m.medID;
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = ["Supplier ID", "Supplier Name", "Medicine Name", "Dosage", "Stock Bought", "Date Bought", "Price Bought"]

        elif table_type == "doctors":
            query = """
                SELECT docID, doctorLastName, doctorFirstName
                FROM doctors;
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = ["Doctor ID", "Last Name", "First Name"]

        elif table_type == "sales":
            # Query for sales
            query = """
                SELECT s.salesID, s.salesDate, s.quantitySold, s.totalPrice, 
                       m.medName AS MedicineName, 
                       CONCAT(c.customerLastName, ', ', c.customerFirstName) AS CustomerName,
                       CASE WHEN s.presID IS NULL THEN 'OTC' ELSE s.presID END AS Prescription,
                       s.mOP AS ModeOfPayment,
                       CASE WHEN s.discount > 0 THEN CONCAT(s.discount * 100, '%') ELSE 'No' END AS Discount
                FROM sales s
                JOIN medicines m ON s.medID = m.medID
                JOIN customers c ON s.customerID = c.customerID;
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = ["Sale ID", "Sale Date", "Quantity Sold", "Total Price", "Medicine Name", "Customer Name", "Prescription/OTC", "Mode of Payment", "Discount"]

        else:
            msg.showerror("Error", "Invalid table type.")
            return

        # Populate Treeview with data
        viewTree.delete(*viewTree.get_children())  # Clear existing data
        viewTree["columns"] = columns
        viewTree["show"] = "headings"

        for col in columns:
            viewTree.heading(col, text=col)
            viewTree.column(col, width=200, anchor="center")

        for row in rows:
            viewTree.insert("", tk.END, values=row)

        # Set frame title dynamically
        viewTitleLabel.config(text=f"Viewing {table_type.capitalize()} Table")
        showFrame(viewTableF)

    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch {table_type} data: {e}")

def generateMonthlyReport(report_type, year=None, month=None):
    """
    Generate a monthly report based on the given type, year, and month.

    Args:
        report_type (str): The type of report to generate ('sales', 'suppliers', 'prescriptions', 'medicines').
        year (int, optional): The year for the report (not needed for inventory reports).
        month (int, optional): The month for the report (not needed for inventory reports).
    """
    try:
        cursor = connection.cursor()

        if report_type == "sales":
            query = """
                SELECT sl.salesID, sl.salesDate, md.medName, ms.dosage, 
                       ct.customerLastName, ct.customerFirstName, 
                       sl.quantitySold, sl.mOP, sl.totalPrice, sl.discount
                FROM sales sl
                JOIN medicines md ON sl.medID = md.medID
                JOIN medSup ms ON ms.medID = md.medID
                JOIN customers ct ON sl.customerID = ct.customerID
                WHERE YEAR(sl.salesDate) = %s AND MONTH(sl.salesDate) = %s
                ORDER BY sl.salesDate;
            """
            params = (year, month)
            columns = ["Sale ID", "Date", "Medicine Name", "Dosage", "Customer Last Name", "Customer First Name", "Quantity Sold", "Mode of Payment", "Total Price", "Discount"]

        elif report_type == "suppliers":
            query = """
                SELECT 
                    s.supId AS "Supplier ID",
                    s.supName AS "Supplier Name",
                    s.contact AS "Contact",
                    GROUP_CONCAT(m.medname SEPARATOR ', ') AS "Medicines Supplied",
                    GROUP_CONCAT(ms.datebought SEPARATOR ', ') AS "Date of Purchase"
                FROM suppliers s
                JOIN medSup ms ON s.supId = ms.supId
                JOIN medicines m ON ms.medId = m.medId
                WHERE YEAR(ms.datebought) = %s AND MONTH(ms.datebought) = %s
                GROUP BY s.supId, s.supName, s.contact;
            """
            params = (year, month)
            columns = ["Supplier ID", "Supplier Name", "Contact", "Medicines Supplied", "Date of Purchase"]

        elif report_type == "prescriptions":
            query = """
                SELECT 
                    p.presId,
                    CONCAT(c.customerLastName, ', ', c.customerFirstName) AS CustomerName,
                    m.medName, 
                    m.dosage,
                    CONCAT(d.doctorLastName, ', ', d.doctorFirstName) AS DoctorName
                FROM prescriptions p
                JOIN customers c ON p.customerId = c.customerId
                JOIN medSup ms ON ms.medId = p.medId
                JOIN doctors d ON p.docId = d.docId
                WHERE YEAR(p.dateIssued) = %s AND MONTH(p.dateIssued) = %s
                ORDER BY presId;
            """
            params = (year, month)
            columns = ["Prescription ID", "Customer Name", "Medicine Name", "Dosage", "Doctor Name"]

        elif report_type == "medicines":
            query = """
                SELECT 
                    m.medID, 
                    m.medName, 
                    m.medType, 
                    m.price, 
                    ms.dosage,
                    SUM(ms.stockBought) AS TotalStockBought,
                    GROUP_CONCAT(DISTINCT s.supName SEPARATOR ', ') AS Suppliers
                FROM medicines m
                JOIN medSup ms ON m.medID = ms.medID
                JOIN suppliers s ON ms.supID = s.supID
                WHERE ms.stockBought > 0
                GROUP BY m.medID, m.medName, m.medType, m.price, ms.dosage
                ORDER BY m.medName;
            """
            params = ()
            columns = ["Medicine ID", "Medicine Name", "Type", "Price", "Dosage", "Total Stock", "Suppliers"]

        else:
            msg.showerror("Error", "Invalid report type.")
            return

        # Execute the query
        cursor.execute(query, params)
        rows = cursor.fetchall()

        # Populate Treeview with data
        viewTree.delete(*viewTree.get_children())  # Clear existing data
        viewTree["columns"] = columns
        viewTree["show"] = "headings"

        for col in columns:
            viewTree.heading(col, text=col)
            viewTree.column(col, width=200, anchor="center")

        for row in rows:
            viewTree.insert("", tk.END, values=row)

        # Set frame title dynamically
        title = f"{report_type.capitalize()} Report: {year}-{month:02d}" if year and month else f"{report_type.capitalize()} Inventory Report"
        viewTitleLabel.config(text=title)
        showFrame(viewTableF)

    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch {report_type} data: {e}")

def navGenerateMonthlyReport():
    """
    Navigate to the monthly report generation frame.
    """
    if connection is None:
        msg.showerror("Error", "Please connect to the database first.")
        return

    showFrame(generateReportF)  



#----------------------------------------- MEDICINE FUNCTIONS -----------------------------------------#
def navAddMed():
    if connection is None:  # Ensure a connection exists before fetching suppliers
        msg.showerror("Error", "Please connect to the database first.")
        return

    suppliers = getSuppliersNON()  # Fetch suppliers from the database
    if suppliers:
        supplierDropdownMed["values"] = suppliers  # Set values in the dropdown
        supplierVarMed.set("")  # Clear current selection

    showFrame(addMedicineF)  # Navigate to Add Medicine frame

def navUpdateMed():
    if connection is None:  
        msg.showerror("Error", "Please connect to the database first.")
        return
    getMedName()  
    showFrame(updateMedicineF)

def navDeleteMedicine():
    getDeletableMed()
    showFrame(deleteMedicineF)

def navLowStock():
    displayLowStock()
    showFrame(lowStockF)

def navExpirationDates():
    displayExpirationDates()
    showFrame(expirationDatesF)

def navInventoryReport():
    showFrame(inventoryReportF)

def getSuppliersNON():
    try:
        cursor = connection.cursor()
        query = "SELECT supID, supName FROM suppliers;"
        cursor.execute(query)
        suppliers = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]  # Combine ID and name for clarity

        if not suppliers:
            msg.showinfo("Info", "No suppliers found in the database.")  # Inform if no suppliers exist

        return suppliers  # Return the fetched suppliers
    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch suppliers: {e}")
        return []

def getMedName():
    try:
        cursor = connection.cursor()
        query = """
            SELECT m.medID, m.medName, ms.dosage, ms.supID, s.supName
            FROM medicines m
            JOIN medSup ms ON m.medID = ms.medID
            JOIN suppliers s ON ms.supID = s.supID;
        """
        cursor.execute(query)
        medicines = [f"{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]}" for row in cursor.fetchall()]
        medicineIDVar.set("")  # Reset dropdown
        medicineIDDropdown["values"] = medicines  # Populate dropdown
    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch medicines: {e}")

def getDeletableMed():
    try:
        cursor = connection.cursor()
        query = "SELECT m.medID, m.medName, ms.dosage FROM medicines m JOIN medSup ms ON m.medID = ms.medID;"
        cursor.execute(query)
        medicines = cursor.fetchall()

        deletable_medicines = []
        for medID, medName, dosage in medicines:
            if not checkIDExists(medID):  # Only include medicines not referenced in other tables
                deletable_medicines.append(f"{medName} - {dosage}")

        deletableMedicineDropdown["values"] = deletable_medicines
        deletableMedicineVar.set("")  # Reset selection

    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch deletable medicines: {e}")

def getPrescMeds(dropdown_var):
    try:
        cursor = connection.cursor()
        query = """
            SELECT m.medID, m.medName, ms.dosage
            FROM medicines AS m
            JOIN medSup AS ms ON m.medID = ms.medID
            WHERE m.medType = 'Prescription';
        """
        cursor.execute(query)
        medicines = [f"{row[0]} - {row[1]} - {row[2]}" for row in cursor.fetchall()]  # Format: Med Name - Dosage

        dropdown_var.set("")  # Reset selection
        return medicines
    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch prescription-only medicines: {e}")
        return []

def showTableMed(sort_by="ID"):

    sort_column_map = {
        "ID": "medId",
        "Name": "name",
        "Dosage": "dosage",
        "Expiry Date": "expiry_date",
        "MedType": "medType",
        "Quantity In Stock": "inStock"
    }
    sort_column = sort_column_map.get(sort_by, "medId")  
    
    try:
        cursor = connection.cursor()
        query = f"""
            SELECT *
            FROM {onTable}
            ORDER BY {sort_column};
        """
        cursor.execute(query)
        data = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]
        medTree.delete(*medTree.get_children()) 
        medTree["columns"] = columns
        medTree["show"] = "headings"

        for col in columns:
            medTree.heading(col, text=col)
            medTree.column(col, width=200, anchor="center")

        for row in data:
            medTree.insert("", tk.END, values=row)
        
        showFrame(medTableF)

    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch data: {e}")

def addNewMedicine():
    check = 1  # Indicator for validation success
    try:
        name = nameInput.get().strip()
        med_type = medTypeVar.get().strip()
        price = priceInput.get().strip()
        supplier = supplierVarMed.get().strip()
        dosage = dosageInput.get().strip()
        expiry_date = expiryInput.get().strip()
        stock_bought = inStockInput.get().strip()
        price_bought = priceBoughtInput.get().strip()
        date_bought = date.today().isoformat()

        # Validation
        if not all([name, med_type, price, supplier, dosage, expiry_date, stock_bought, price_bought]):
            msg.showerror("Error", "All fields must be filled out.")
            check = 0
            return

        if len(name) > 50:
            msg.showerror("Error", "Medicine name must not exceed 50 characters.")
            check = 0
            return

        if med_type not in ["OTC", "Prescription"]:
            msg.showerror("Error", "Medicine type must be 'OTC' or 'Prescription'.")
            check = 0
            return

        try:
            price = float(price)
            price_bought = float(price_bought)
            if price <= 0 or price_bought <= 0:
                msg.showerror("Error", "Price and Price Bought must be greater than 0.")
                check = 0
                return
        except ValueError:
            msg.showerror("Error", "Price and Price Bought must be valid decimal numbers.")
            check = 0
            return

        if " - " not in supplier:
            msg.showerror("Error", "Please select a valid supplier from the dropdown.")
            check = 0
            return
        supID = supplier.split(" - ")[0]

        try:
            dosage_value = float(dosage)
            if dosage_value <= 0:
                msg.showerror("Error", "Dosage must be a positive float.")
                check = 0
                return
            dosage = f"{dosage_value}mg"
        except ValueError:
            msg.showerror("Error", "Dosage must be a valid float.")
            check = 0
            return

        try:
            expiry_date_obj = date.fromisoformat(expiry_date)
            if expiry_date_obj <= date.today():
                msg.showerror("Error", "Expiry date must be a future date.")
                check = 0
                return
        except ValueError:
            msg.showerror("Error", "Expiry date must be in the format YYYY-MM-DD.")
            check = 0
            return

        try:
            stock_bought = int(stock_bought)
            if stock_bought <= 0:
                msg.showerror("Error", "Stock Bought must be a positive integer.")
                check = 0
                return
        except ValueError:
            msg.showerror("Error", "Stock Bought must be a valid integer.")
            check = 0
            return

        # Check for uniqueness (medName, dosage, supID)
        cursor = connection.cursor()
        query = """
            SELECT COUNT(*)
            FROM medicines
            JOIN medSup ON medicines.medID = medSup.medID
            WHERE medicines.medName = %s AND medSup.dosage = %s AND medSup.supID = %s;
        """
        cursor.execute(query, (name, dosage, supID))
        exists = cursor.fetchone()[0]

        if exists:
            msg.showerror("Error", "A medicine with the same name, dosage, and supplier already exists.")
            check = 0
            return

        if check:
            # Generate new medID
            cursor.execute("SELECT MAX(medID) FROM medicines;")
            result = cursor.fetchone()
            numMedID = letterKeyRemover(result[0]) + 1 if result[0] else 1
            next_medID = f"A{numMedID:04d}"

            # Insert into medicines
            cursor.execute(
                "INSERT INTO medicines (medID, medName, medType, price) VALUES (%s, %s, %s, %s);",
                (next_medID, name, med_type, price)
            )

            # Insert into medSup
            cursor.execute(
                """
                INSERT INTO medSup (medID, supID, dosage, expiry_date, stockBought, dateBought, priceBought)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """,
                (next_medID, supID, dosage, expiry_date, stock_bought, date_bought, price_bought)
            )

            connection.commit()
            msg.showinfo("Success", f"New medicine added with ID: {next_medID}")

            # Clear inputs after successful insertion
            nameInput.delete(0, tk.END)
            medTypeVar.set("OTC")
            priceInput.delete(0, tk.END)
            supplierVarMed.set("")
            dosageInput.delete(0, tk.END)
            expiryInput.delete(0, tk.END)
            inStockInput.delete(0, tk.END)
            priceBoughtInput.delete(0, tk.END)

    except sql.Error as e:
        msg.showerror("Error", f"Failed to add new medicine: {e}")
    except Exception as e:
        msg.showerror("Error", f"Unexpected error: {e}")

def updateMedicine():
    try:
        selected_medicine = medicineIDVar.get()
        if not selected_medicine or " - " not in selected_medicine:
            msg.showerror("Error", "Please select a valid medicine.")
            return

        # Extracting values from the new dropdown format
        medID, medName, dosage, supID, supName = selected_medicine.split(" - ")

        new_name = newNameInput.get().strip()
        new_med_type = newMedTypeVar.get().strip()
        new_price = newPriceInput.get().strip()
        new_dosage = newDosageInput.get().strip()
        new_stock = newStockInput.get().strip()

        # Ensure updated medicine does not duplicate an existing record
        try:
            cursor = connection.cursor()

            if new_name and new_name != "NA" and new_dosage and new_dosage != "NA":
                new_dosage_value = f"{float(new_dosage)}mg"
                duplicate_check_query = """
                    SELECT COUNT(*)
                    FROM medicines m
                    JOIN medSup ms ON m.medID = ms.medID
                    WHERE m.medName = %s AND ms.dosage = %s AND ms.supID = %s AND m.medID != %s;
                """
                cursor.execute(duplicate_check_query, (new_name, new_dosage_value, supID, medID))
                exists = cursor.fetchone()[0]

                if exists:
                    msg.showerror(
                        "Error",
                        f"A medicine with the name '{new_name}', dosage '{new_dosage_value}', and supplier '{supName}' already exists."
                    )
                    return

        except ValueError:
            msg.showerror("Error", "Dosage must be a valid number.")
            return

        # Prepare updates for the medicines table
        update_queries = []
        update_values = []

        if new_name and new_name != "NA":
            update_queries.append("medName = %s")
            update_values.append(new_name)
        if new_med_type and new_med_type != "NA":
            if new_med_type not in ["OTC", "Prescription"]:
                msg.showerror("Error", "Medicine type must be 'OTC' or 'Prescription' or NA.")
                return
            update_queries.append("medType = %s")
            update_values.append(new_med_type)
        if new_price and new_price != "NA":
            try:
                new_price = float(new_price)
                if new_price <= 0:
                    msg.showerror("Error", "Price must be greater than 0.")
                    return
                update_queries.append("price = %s")
                update_values.append(new_price)
            except ValueError:
                msg.showerror("Error", "Price must be a valid decimal number.")
                return

        if update_queries:
            update_query = f"UPDATE medicines SET {', '.join(update_queries)} WHERE medID = %s;"
            update_values.append(medID)
            cursor.execute(update_query, tuple(update_values))

        # Prepare updates for the medSup table
        medsup_updates = []
        medsup_values = []

        if new_dosage and new_dosage != "NA":
            try:
                new_dosage = float(new_dosage)
                if new_dosage <= 0:
                    msg.showerror("Error", "Dosage must be a positive float.")
                    return
                new_dosage = f"{new_dosage}mg"
                medsup_updates.append("dosage = %s")
                medsup_values.append(new_dosage)
            except ValueError:
                msg.showerror("Error", "Dosage must be a valid float.")
                return
        if new_stock and new_stock != "NA":
            try:
                new_stock = int(new_stock)
                if new_stock < 0:
                    msg.showerror("Error", "Stock quantity must be a non-negative integer.")
                    return
                medsup_updates.append("stockBought = %s")
                medsup_values.append(new_stock)
            except ValueError:
                msg.showerror("Error", "Stock quantity must be a valid integer.")
                return

        if medsup_updates:
            medsup_query = f"UPDATE medSup SET {', '.join(medsup_updates)} WHERE medID = %s AND supID = %s;"
            medsup_values.extend([medID, supID])
            cursor.execute(medsup_query, tuple(medsup_values))

        # Commit the transaction
        connection.commit()
        msg.showinfo("Success", f"Medicine '{medID} - {medName} - {dosage} - {supID} - {supName}' updated successfully.")

    except sql.Error as e:
        msg.showerror("Error", f"Failed to update medicine: {e}")
    except Exception as e:
        msg.showerror("Error", f"Unexpected error occurred: {e}")

def deleteMedicine():
    selected_medicine = deletableMedicineVar.get()
    if not selected_medicine:
        msg.showerror("Error", "Please select a medicine to delete.")
        return

    medName = selected_medicine.split(" - ")[0]

    try:
        cursor = connection.cursor()
        get_medID_query = "SELECT medID FROM medicines WHERE medName = %s;"
        cursor.execute(get_medID_query, (medName,))
        medID_result = cursor.fetchone()

        if not medID_result:
            msg.showerror("Error", f"No medicine found with the name '{medName}'.")
            return

        medID = medID_result[0]

        # Check if the medID exists in related tables
        if checkIDExists(medID):
            msg.showerror(
                "Error",
                f"Medicine ID '{medID}' exists in related tables (prescriptions or sales). Deletion not allowed."
            )
            return

        # Proceed with deletion
        delete_query = "DELETE FROM medicines WHERE medID = %s;"
        cursor.execute(delete_query, (medID,))
        connection.commit()

        msg.showinfo("Success", f"Medicine ID '{medID}' deleted successfully.")
        getDeletableMed()  # Refresh the dropdown list of deletable medicines

    except sql.Error as e:
        msg.showerror("Error", f"Failed to delete medicine: {e}")
    except Exception as e:
        msg.showerror("Error", f"Unexpected error: {e}")

def displayLowStock():
    try:
        cursor = connection.cursor()
        query = """
            WITH low_stock AS (
                SELECT ms.dosage, m.medName, SUM(ms.stockBought) AS total_stock
                FROM medicines m
                JOIN medSup ms ON m.medID = ms.medID
                GROUP BY m.medName, ms.dosage
                HAVING total_stock < 10
            )
            SELECT m.medName, ms.dosage, ms.stockBought, s.supName
            FROM medicines m
            JOIN medSup ms ON m.medID = ms.medID
            JOIN suppliers s ON ms.supID = s.supID
            WHERE EXISTS (
                SELECT 1
                FROM low_stock ls
                WHERE ls.medName = m.medName AND ls.dosage = ms.dosage
            )
            ORDER BY m.medName, ms.dosage, ms.stockBought;
        """
        cursor.execute(query)
        low_stock_medicines = cursor.fetchall()

        lowStockTree.delete(*lowStockTree.get_children())

        for medName, dosage, stock, supName in low_stock_medicines:
            lowStockTree.insert("", tk.END, values=(medName, dosage, stock, supName))

        if not low_stock_medicines:
            msg.showinfo("Info", "No low-stock medicines found.")

    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch and display low-stock medicines: {e}")

def displayExpirationDates():
    try:
        cursor = connection.cursor()
        query = """
            SELECT m.medName, ms.dosage, s.supName, ms.expiry_date
            FROM medicines m
            JOIN medSup ms ON m.medID = ms.medID
            JOIN suppliers s ON ms.supID = s.supID
            ORDER BY ms.expiry_date;
        """
        cursor.execute(query)
        data = cursor.fetchall()

        expirationTree.delete(*expirationTree.get_children())

        for medName, dosage, supName, expiry_date in data:
            expirationTree.insert("", tk.END, values=(medName, dosage, supName, expiry_date))

        if not data:
            msg.showinfo("Info", "No medicines found.")

    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch expiration dates: {e}")

def displayInventoryReport():
    """
    Generate and display an inventory report showing the stock remaining at the end of a given year and month.
    """
    # Get year and month from input fields
    year = yearInput.get().strip()
    month = monthInput.get().strip()

    # Validate inputs
    if not year.isdigit() or not month.isdigit():
        msg.showerror("Error", "Please enter valid numeric values for Year and Month.")
        return

    year = int(year)
    month = int(month)

    if month < 1 or month > 12:
        msg.showerror("Error", "Month must be between 1 and 12.")
        return

    try:
        # Fetch data from the database
        cursor = connection.cursor()
        query = """
            WITH inventory_summary AS (
                SELECT 
                    m.medID, 
                    m.medName, 
                    ms.dosage, 
                    s.supName, 
                    SUM(ms.stockBought) AS total_stock,
                    COALESCE(SUM(sales.quantitySold), 0) AS total_sold
                FROM medicines m
                JOIN medSup ms ON m.medID = ms.medID
                LEFT JOIN suppliers s ON ms.supID = s.supID
                LEFT JOIN sales sales ON m.medID = sales.medID
                    AND YEAR(sales.salesDate) <= %s
                    AND MONTH(sales.salesDate) <= %s
                WHERE YEAR(ms.dateBought) <= %s
                  AND MONTH(ms.dateBought) <= %s
                GROUP BY m.medID, m.medName, ms.dosage, s.supName
            )
            SELECT 
                medID, 
                medName, 
                dosage, 
                supName, 
                (total_stock - total_sold) AS remaining_stock
            FROM inventory_summary
            WHERE (total_stock - total_sold) > 0;
        """
        cursor.execute(query, (year, month, year, month))
        data = cursor.fetchall()

        # Clear existing rows in Treeview
        reportTree.delete(*reportTree.get_children())

        # Populate Treeview with results
        for medID, medName, dosage, supName, remaining_stock in data:
            reportTree.insert("", tk.END, values=(medID, medName, dosage, remaining_stock, supName))

        # Show info message if no data found
        if not data:
            msg.showinfo("Info", "No inventory data found for the given year and month.")

    except sql.Error as e:
        msg.showerror("Error", f"Failed to generate inventory report: {e}")


#----------------------------------------- CUSTOMER FUNCTIONS -----------------------------------------#

def showTableCus(sort_by="ID"):
    sort_column_map = {
        "ID": "customerId",
        "Last Name": "customerLastName",
        "First Name": "customerFirstName",
        "Discount Card": "HasDisCard",
    }
    sort_column = sort_column_map.get(sort_by, "customerId")  
    
    try:
        cursor = connection.cursor()
        query = f"""
            SELECT *
            FROM {onTable}
            ORDER BY {sort_column};
        """
        cursor.execute(query)
        data = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]
        cusTree.delete(*cusTree.get_children()) 
        cusTree["columns"] = columns
        cusTree["show"] = "headings"

        for col in columns:
            cusTree.heading(col, text=col)
            cusTree.column(col, width=200, anchor="center")

        for row in data:
            cusTree.insert("", tk.END, values=row)
        
        showFrame(cusTableF)

    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch data: {e}")

def getCustomersNON():
    try:
        cursor = connection.cursor()
        query = "SELECT customerID, CONCAT(customerFirstName, ' ', customerLastName) AS fullName FROM customers;"
        cursor.execute(query)
        customers = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
        updateCustomerVar.set("")  # Reset selection
        customerDropdownNON["values"] = customers
    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch customers: {e}")

def getCustomers(dropdown_var):
    try:
        cursor = connection.cursor()
        query = "SELECT customerID, CONCAT(customerFirstName, ' ', customerLastName) AS fullName FROM customers;"
        cursor.execute(query)
        customers = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
        dropdown_var.set("")  # Reset selection
        return customers
    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch customers: {e}")
        return []

def getDeletableCustomers():
    deletable_customers = getDeletableIDs("customers", "customerID")
    deleteCustomerVar.set("")  # Reset selection
    customerDeleteDropdown["values"] = deletable_customers

def navDeleteCustomer():
    getDeletableCustomers()
    showFrame(deleteCustomerF)

def navupdateCustomer():
    if connection is None:  
        msg.showerror("Error", "Please connect to the database first.")
        return
    getCustomersNON()  
    showFrame(updateCustomerF)

def navCreateCustomer():
    showFrame(createCustomerF)

def navViewCustomers():
    viewTable("customers")

def createCustomer():
    try:
        last_name = customerLastNameInput.get().strip()
        first_name = customerFirstNameInput.get().strip()
        discount_card = hasDiscountCardVar.get()

        if not last_name or not first_name:
            msg.showerror("Error", "Both First Name and Last Name are required.")
            return

        if len(last_name) > 50 or len(first_name) > 50:
            msg.showerror("Error", "First Name and Last Name must not exceed 50 characters.")
            return

        if discount_card not in [0, 1]:
            msg.showerror("Error", "Discount Card status must be either 0 (No) or 1 (Yes).")
            return

        cursor = connection.cursor()
        check_query = """
            SELECT COUNT(*) 
            FROM customers 
            WHERE customerLastName = %s AND customerFirstName = %s;
        """
        cursor.execute(check_query, (last_name, first_name))
        exists = cursor.fetchone()[0]

        if exists > 0:
            msg.showerror("Error", f"Customer '{first_name} {last_name}' already exists.")
            return

        cursor.execute("SELECT MAX(customerID) FROM customers;")
        result = cursor.fetchone()
        numCustomerID = letterKeyRemover(result[0]) + 1 if result[0] else 1
        new_customerID = f"C{numCustomerID:04d}"

        query = """
            INSERT INTO customers (customerID, customerLastName, customerFirstName, HasDisCard)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(query, (new_customerID, last_name, first_name, discount_card))
        connection.commit()

        msg.showinfo("Success", f"Customer '{first_name} {last_name}' created with ID: {new_customerID}")

        customerLastNameInput.delete(0, tk.END)
        customerFirstNameInput.delete(0, tk.END)
        hasDiscountCardVar.set(0)

    except sql.Error as e:
        msg.showerror("Error", f"Failed to create customer: {e}")
    except Exception as e:
        msg.showerror("Error", f"Unexpected error: {e}")

def updateCustomer():
    selected_customer = updateCustomerVar.get()
    if not selected_customer:
        msg.showerror("Error", "Please select a customer to update.")
        return

    customerID = selected_customer.split(" - ")[0]
    last_name = updateCustomerLastNameInput.get().strip()
    first_name = updateCustomerFirstNameInput.get().strip()
    discount_card = updateCustomerDiscountInput.get().strip()

    updates = []
    params = []

    if last_name != "NA":
        if len(last_name) > 50:
            msg.showerror("Error", "Last Name must not exceed 50 characters.")
            return
        updates.append("customerLastName = %s")
        params.append(last_name)

    if first_name != "NA":
        if len(first_name) > 50:
            msg.showerror("Error", "First Name must not exceed 50 characters.")
            return
        updates.append("customerFirstName = %s")
        params.append(first_name)

    if discount_card != "NA":
        if discount_card not in ["0", "1"]:
            msg.showerror("Error", "Discount Card must be 0 (No) or 1 (Yes).")
            return
        updates.append("HasDisCard = %s")
        params.append(int(discount_card))

    if not updates:
        msg.showerror("Error", "No valid fields to update.")
        return

    try:
        if "customerLastName = %s" in updates and "customerFirstName = %s" in updates:
            cursor = connection.cursor()
            check_query = """
                SELECT COUNT(*) 
                FROM customers 
                WHERE customerLastName = %s AND customerFirstName = %s AND customerID != %s;
            """
            cursor.execute(check_query, (last_name, first_name, customerID))
            if cursor.fetchone()[0] > 0:
                msg.showerror("Error", "A customer with the same name already exists.")
                return

        params.append(customerID)
        cursor = connection.cursor()
        query = f"UPDATE customers SET {', '.join(updates)} WHERE customerID = %s;"
        cursor.execute(query, tuple(params))
        connection.commit()
        msg.showinfo("Success", "Customer updated successfully.")
        getCustomersNON()  # Refresh dropdown
    except sql.Error as e:
        msg.showerror("Error", f"Failed to update customer: {e}")

def deleteCustomer():
    selected_customer = deleteCustomerVar.get()
    if not selected_customer:
        msg.showerror("Error", "Please select a customer to delete.")
        return

    customerID = selected_customer.split(" - ")[0]

    if checkIDExists(customerID):
        msg.showerror(
            "Error",
            f"Customer ID '{customerID}' exists in related tables (e.g., prescriptions or sales). Deletion not allowed."
        )
        return

    try:
        cursor = connection.cursor()
        delete_query = "DELETE FROM customers WHERE customerID = %s;"
        cursor.execute(delete_query, (customerID,))
        connection.commit()

        msg.showinfo("Success", f"Customer ID '{customerID}' deleted successfully.")
        getDeletableCustomers()  # Refresh dropdown
    except sql.Error as e:
        msg.showerror("Error", f"Failed to delete customer: {e}")

#----------------------------------------- DOCTOR FUNCTIONS -----------------------------------------#
def navCreateDoctor():
    showFrame(createDoctorF)

def navUpdateDoctor():
    if connection is None:  
        msg.showerror("Error", "Please connect to the database first.")
        return
    getDoctorsNON()  
    showFrame(updateDoctorF)

def navDeleteDoctor():
    getDeletableDoctors()
    showFrame(deleteDoctorF)

def navViewDoctors():
    viewTable("doctors")

def getDoctorsNON():
    try:
        cursor = connection.cursor()
        query = "SELECT docID, CONCAT(doctorFirstName, ' ', doctorLastName) AS fullName FROM doctors;"
        cursor.execute(query)
        doctors = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
        updateDoctorVar.set("")  # Reset selection
        doctorDropdownNON["values"] = doctors
    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch doctors: {e}")

def getDoctors(dropdown_var):
    try:
        cursor = connection.cursor()
        query = "SELECT docID, CONCAT(doctorFirstName, ' ', doctorLastName) AS fullName FROM doctors;"
        cursor.execute(query)
        doctors = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
        dropdown_var.set("")  # Reset selection
        return doctors
    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch doctors: {e}")
        return []

def getDeletableDoctors():
    deletable_doctors = getDeletableIDs("doctors", "docID")
    deleteDoctorVar.set("")  # Reset selection
    doctorDeleteDropdown["values"] = deletable_doctors

def createDoctor():
    try:
        last_name = doctorLastNameInput.get().strip()
        first_name = doctorFirstNameInput.get().strip()

        if not last_name or not first_name:
            msg.showerror("Error", "Both First Name and Last Name are required.")
            return

        if len(last_name) > 50 or len(first_name) > 50:
            msg.showerror("Error", "First Name and Last Name must not exceed 50 characters.")
            return

        cursor = connection.cursor()
        check_query = """
            SELECT COUNT(*) 
            FROM doctors 
            WHERE doctorLastName = %s AND doctorFirstName = %s;
        """
        cursor.execute(check_query, (last_name, first_name))
        exists = cursor.fetchone()[0]

        if exists > 0:
            msg.showerror("Error", f"Doctor '{first_name} {last_name}' already exists.")
            return

        cursor.execute("SELECT MAX(docID) FROM doctors;")
        result = cursor.fetchone()
        numDocID = letterKeyRemover(result[0]) + 1 if result[0] else 1
        new_docID = f"D{numDocID:04d}"

        query = """
            INSERT INTO doctors (docID, doctorLastName, doctorFirstName)
            VALUES (%s, %s, %s);
        """
        cursor.execute(query, (new_docID, last_name, first_name))
        connection.commit()

        msg.showinfo("Success", f"Doctor '{first_name} {last_name}' created with ID: {new_docID}")

        doctorLastNameInput.delete(0, tk.END)
        doctorFirstNameInput.delete(0, tk.END)

    except sql.Error as e:
        msg.showerror("Error", f"Failed to create doctor: {e}")
    except Exception as e:
        msg.showerror("Error", f"Unexpected error: {e}")

def updateDoctor():
    selected_doctor = updateDoctorVar.get()
    if not selected_doctor:
        msg.showerror("Error", "Please select a doctor to update.")
        return

    docID = selected_doctor.split(" - ")[0]
    last_name = updateDoctorLastNameInput.get().strip()
    first_name = updateDoctorFirstNameInput.get().strip()

    updates = []
    params = []

    if last_name != "NA":
        if len(last_name) > 50:
            msg.showerror("Error", "Last Name must not exceed 50 characters.")
            return
        updates.append("doctorLastName = %s")
        params.append(last_name)

    if first_name != "NA":
        if len(first_name) > 50:
            msg.showerror("Error", "First Name must not exceed 50 characters.")
            return
        updates.append("doctorFirstName = %s")
        params.append(first_name)

    if not updates:
        msg.showerror("Error", "No valid fields to update.")
        return

    try:
        if "doctorLastName = %s" in updates and "doctorFirstName = %s" in updates:
            cursor = connection.cursor()
            check_query = """
                SELECT COUNT(*) 
                FROM doctors 
                WHERE doctorLastName = %s AND doctorFirstName = %s AND docID != %s;
            """
            cursor.execute(check_query, (last_name, first_name, docID))
            if cursor.fetchone()[0] > 0:
                msg.showerror("Error", "A doctor with the same name already exists.")
                return

        params.append(docID)
        cursor = connection.cursor()
        query = f"UPDATE doctors SET {', '.join(updates)} WHERE docID = %s;"
        cursor.execute(query, tuple(params))
        connection.commit()
        msg.showinfo("Success", "Doctor updated successfully.")
        getDoctorsNON()  # Refresh dropdown
    except sql.Error as e:
        msg.showerror("Error", f"Failed to update doctor: {e}")

def deleteDoctor():
    selected_doctor = deleteDoctorVar.get()
    if not selected_doctor:
        msg.showerror("Error", "Please select a doctor to delete.")
        return

    docID = selected_doctor.split(" - ")[0]

    if checkIDExists(docID):
        msg.showerror(
            "Error",
            f"Doctor ID '{docID}' exists in related tables (e.g., prescriptions). Deletion not allowed."
        )
        return

    try:
        cursor = connection.cursor()
        delete_query = "DELETE FROM doctors WHERE docID = %s;"
        cursor.execute(delete_query, (docID,))
        connection.commit()

        msg.showinfo("Success", f"Doctor ID '{docID}' deleted successfully.")
        getDeletableDoctors()  # Refresh dropdown
    except sql.Error as e:
        msg.showerror("Error", f"Failed to delete doctor: {e}")

#----------------------------------------- SUPPLIER FUNCTIONS -----------------------------------------#
def navCreateSupplier():
    showFrame(createSupplierF)

def navUpdateSupplier():
    if connection is None:  
        msg.showerror("Error", "Please connect to the database first.")
        return
    getSuppliers()  
    showFrame(updateSupplierF)

def navDeleteSupplier():
    getDeletableSuppliers()
    showFrame(deleteSupplierF)

def navViewSupplier():
    viewTable("suppliers")

def getSuppliers():
    try:
        cursor = connection.cursor()
        query = "SELECT supID, supName FROM suppliers;"
        cursor.execute(query)
        suppliers = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
        updateSupplierVar.set("")  # Reset selection
        supplierDropdown["values"] = suppliers
    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch suppliers: {e}")

def getDeletableSuppliers():
    try:
        cursor = connection.cursor()
        query = "SELECT supID, supName FROM suppliers;"
        cursor.execute(query)
        all_suppliers = cursor.fetchall()

        deletable_suppliers = []
        for row in all_suppliers:
            supID = row[0]
            supName = row[1]
            if not checkIDExists(supID):  # Check if supplier ID is not referenced in medSup
                deletable_suppliers.append(f"{supID} - {supName}")

        deleteSupplierVar.set("")  # Reset selection
        supplierDeleteDropdown["values"] = deletable_suppliers
    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch deletable suppliers: {e}")

def createSupplier():
    try:
        supplier_name = supplierNameInput.get().strip()
        contact = contactInput.get().strip()

        if not supplier_name or not contact:
            msg.showerror("Error", "Both Supplier Name and Contact are required.")
            return

        if len(supplier_name) > 100:
            msg.showerror("Error", "Supplier Name must not exceed 100 characters.")
            return

        if len(contact) > 50:
            msg.showerror("Error", "Contact must not exceed 50 characters.")
            return

        cursor = connection.cursor()
        check_query = """
            SELECT COUNT(*) 
            FROM suppliers 
            WHERE supName = %s;
        """
        cursor.execute(check_query, (supplier_name,))
        exists = cursor.fetchone()[0]

        if exists > 0:
            msg.showerror("Error", f"Supplier '{supplier_name}' already exists.")
            return

        cursor.execute("SELECT MAX(supID) FROM suppliers;")
        result = cursor.fetchone()
        numSupID = letterKeyRemover(result[0]) + 1 if result[0] else 1
        new_supID = f"B{numSupID:04d}"

        query = """
            INSERT INTO suppliers (supID, supName, contact)
            VALUES (%s, %s, %s);
        """
        cursor.execute(query, (new_supID, supplier_name, contact))
        connection.commit()

        msg.showinfo("Success", f"Supplier '{supplier_name}' created with ID: {new_supID}")

        supplierNameInput.delete(0, tk.END)
        contactInput.delete(0, tk.END)

    except sql.Error as e:
        msg.showerror("Error", f"Failed to create supplier: {e}")
    except Exception as e:
        msg.showerror("Error", f"Unexpected error: {e}")

def updateSupplier():
    selected_supplier = updateSupplierVar.get()
    if not selected_supplier:
        msg.showerror("Error", "Please select a supplier to update.")
        return

    supID = selected_supplier.split(" - ")[0]
    supplier_name = updateSupplierNameInput.get().strip()
    contact = updateSupplierContactInput.get().strip()

    updates = []
    params = []

    if supplier_name != "NA":
        if len(supplier_name) > 100:
            msg.showerror("Error", "Supplier Name must not exceed 100 characters.")
            return
        updates.append("supName = %s")
        params.append(supplier_name)

    if contact != "NA":
        if len(contact) > 50:
            msg.showerror("Error", "Contact must not exceed 50 characters.")
            return
        updates.append("contact = %s")
        params.append(contact)

    if not updates:
        msg.showerror("Error", "No valid fields to update.")
        return

    try:
        if "supName = %s" in updates:
            cursor = connection.cursor()
            check_query = """
                SELECT COUNT(*) 
                FROM suppliers 
                WHERE supName = %s AND supID != %s;
            """
            cursor.execute(check_query, (supplier_name, supID))
            if cursor.fetchone()[0] > 0:
                msg.showerror("Error", "A supplier with the same name already exists.")
                return

        params.append(supID)
        cursor = connection.cursor()
        query = f"UPDATE suppliers SET {', '.join(updates)} WHERE supID = %s;"
        cursor.execute(query, tuple(params))
        connection.commit()
        msg.showinfo("Success", "Supplier updated successfully.")
        getSuppliers() 
    except sql.Error as e:
        msg.showerror("Error", f"Failed to update supplier: {e}")

def deleteSupplier():
    selected_supplier = deleteSupplierVar.get()
    if not selected_supplier:
        msg.showerror("Error", "Please select a supplier to delete.")
        return

    supID = selected_supplier.split(" - ")[0]

    if checkIDExists(supID):
        msg.showerror(
            "Error",
            f"Supplier ID '{supID}' exists in related tables (e.g., medSup). Deletion not allowed."
        )
        return

    try:
        cursor = connection.cursor()
        delete_query = "DELETE FROM suppliers WHERE supID = %s;"
        cursor.execute(delete_query, (supID,))
        connection.commit()

        msg.showinfo("Success", f"Supplier ID '{supID}' deleted successfully.")
        getDeletableSuppliers()  # Refresh dropdown
    except sql.Error as e:
        msg.showerror("Error", f"Failed to delete supplier: {e}")

#----------------------------------------- PRESCRIPTION FUNCTIONS -----------------------------------------#
def navAddPrescription():
    customerDropdown["values"] = getCustomers(customerVar)
    doctorDropdown["values"] = getDoctors(doctorVar)
    prescriptionMedDropdown["values"] = getPrescMeds(prescriptionMedVar)

    # Show the Add Prescription frame
    showFrame(addPrescriptionF)

def navUpdatePrescription():
    if connection is None:
        msg.showerror("Error", "Please connect to the database first.")
        return

    prescSelectionDropdown["values"] = getPrescriptionsForUpdate(prescSelectionVar)
    newPrescMedDropdown["values"] = getPrescMeds(newPrescMedVar)
    newDoctorDropdown["values"] = getDoctors(newDoctorVar)

    showFrame(updatePrescriptionF)

def navDeletePresc():
    if connection is None:
        msg.showerror("Error", "Please connect to the database first.")
        return
    getDeletablePrescriptions()  # Populate the dropdown with deletable prescriptions
    showFrame(deletePrescriptionF)  # Navigate to the Delete Prescription frame

def navViewPrescriptions():
    viewTable("prescriptions")

def getPrescriptionsForUpdate(var):
    try:
        cursor = connection.cursor()
        query = """
            SELECT p.presID, c.customerID, c.customerLastName, c.customerFirstName 
            FROM prescriptions p
            JOIN customers c ON p.customerID = c.customerID;
        """
        cursor.execute(query)
        prescriptions = [
            f"{row[0]} - {row[2]} {row[3]} ({row[1]})" for row in cursor.fetchall()
        ]
        var.set("")  # Reset dropdown selection
        return prescriptions
    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch prescriptions: {e}")
        return []

def getDeletablePrescriptions():
    try:
        cursor = connection.cursor()
        query = """
            SELECT p.presID, CONCAT(c.customerLastName, ', ', c.customerFirstName) AS customerName
            FROM prescriptions p
            JOIN customers c ON p.customerID = c.customerID;
        """
        cursor.execute(query)
        prescriptions = cursor.fetchall()

        deletable_prescriptions = []
        for presID, customerName in prescriptions:
            if not checkIDExists(presID):  # Only include prescriptions not referenced elsewhere
                deletable_prescriptions.append(f"{presID} - {customerName}")

        deletablePrescriptionVar.set("")  # Reset dropdown
        deletablePrescriptionDropdown["values"] = deletable_prescriptions  # Populate dropdown

    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch deletable prescriptions: {e}")

def addNewPrescription():
    customer_selection = customerVar.get()
    medicine_selection = prescriptionMedVar.get()
    doctor_selection = doctorVar.get()

    if not all([customer_selection, medicine_selection, doctor_selection]):
        msg.showerror("Error", "All fields must be selected.")
        return

    customerID = customer_selection.split(" - ")[0]
    medID = medicine_selection.split(" - ")[0]
    docID = doctor_selection.split(" - ")[0]

    try:
        cursor = connection.cursor()

        check_query = """
            SELECT COUNT(*) 
            FROM prescriptions 
            WHERE customerID = %s AND medID = %s AND docID = %s;
        """
        cursor.execute(check_query, (customerID, medID, docID))
        exists = cursor.fetchone()[0]

        if exists:
            msg.showerror("Error", "A prescription with the same details already exists.")
            return

        cursor.execute("SELECT MAX(presID) FROM prescriptions;")
        result = cursor.fetchone()
        numPresID = letterKeyRemover(result[0]) + 1 if result[0] else 1
        new_presID = f"E{numPresID:04d}"

        query_insert = """
            INSERT INTO prescriptions (presID, customerID, medID, docID)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(query_insert, (new_presID, customerID, medID, docID))
        connection.commit()

        msg.showinfo("Success", f"Prescription added successfully with ID: {new_presID}")
    except sql.Error as e:
        msg.showerror("Error", f"Failed to add prescription: {e}")

def updatePrescription():
    try:
        selected_prescription = prescSelectionVar.get()
        new_medicine = newPrescMedVar.get()
        new_doctor = newDoctorVar.get()

        if not selected_prescription or " - " not in selected_prescription:
            msg.showerror("Error", "Please select a valid prescription.")
            return

        presID, customer_details = selected_prescription.split(" - ", 1)
        customer_name, customer_id = customer_details.rsplit("(", 1)
        customer_id = customer_id.strip(")")

        if not new_medicine or " - " not in new_medicine:
            msg.showerror("Error", "Please select a valid medicine.")
            return

        if not new_doctor or " - " not in new_doctor:
            msg.showerror("Error", "Please select a valid doctor.")
            return

        medID = new_medicine.split(" - ")[0]  # Get the first part (medID)

        docID = new_doctor.split(" - ")[0]  # Get the first part (docID)

        print(f"Customer ID: {customer_id}, Med ID: {medID}, Doc ID: {docID}, Pres ID: {presID}")

        cursor = connection.cursor()
        query = """
            SELECT COUNT(*) 
            FROM prescriptions 
            WHERE customerID = %s AND medID = %s AND docID = %s AND presID != %s;
        """
        cursor.execute(query, (customer_id, medID, docID, presID))
        exists = cursor.fetchone()[0]

        if exists:
            msg.showerror("Error", "A prescription with the same details already exists.")
            return

        update_query = """
            UPDATE prescriptions 
            SET medID = %s, docID = %s 
            WHERE presID = %s;
        """
        cursor.execute(update_query, (medID, docID, presID))
        connection.commit()

        msg.showinfo("Success", "Prescription updated successfully.")

        navUpdatePrescription()

    except sql.Error as e:
        msg.showerror("Error", f"Failed to update prescription: {e}")
    except Exception as e:
        msg.showerror("Error", f"Unexpected error: {e}")

def deletePrescription():
    try:
        selected_prescription = deletablePrescriptionVar.get()
        if not selected_prescription or " - " not in selected_prescription:
            msg.showerror("Error", "Please select a valid prescription to delete.")
            return

        presID, customerName = selected_prescription.split(" - ")

        # Check if the prescription exists in any other tables
        if checkIDExists(presID):
            msg.showerror(
                "Error",
                f"Prescription ID '{presID}' exists in related tables. Deletion not allowed."
            )
            return

        cursor = connection.cursor()
        delete_query = "DELETE FROM prescriptions WHERE presID = %s;"
        cursor.execute(delete_query, (presID,))
        connection.commit()

        msg.showinfo("Success", f"Prescription ID '{presID}' deleted successfully.")

        # Refresh the deletable prescription dropdown
        getDeletablePrescriptions()

    except sql.Error as e:
        msg.showerror("Error", f"Failed to delete prescription: {e}")
    except Exception as e:
        msg.showerror("Error", f"Unexpected error: {e}")

def getCustomersForSales(variable):
    try:
        cursor = connection.cursor()
        query = "SELECT customerID, customerLastName, customerFirstName FROM customers;"
        cursor.execute(query)
        customers = [f"{row[0]} - {row[1]}, {row[2]}" for row in cursor.fetchall()]
        variable.set("")  # Reset dropdown
        return customers
    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch customers: {e}")
        return []

def getOTCMeds(variable):
    try:
        cursor = connection.cursor()
        query = """
            SELECT m.medID, m.medName, ms.dosage, ms.supID, m.price, ms.stockBought
            FROM medicines m
            JOIN medSup ms ON m.medID = ms.medID
            WHERE m.medType = 'OTC' AND ms.stockBought > 0;
        """
        cursor.execute(query)
        otc_meds = [f"{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]} - {row[5]} pcs" for row in cursor.fetchall()]
        variable.set("")  # Reset dropdown
        return otc_meds
    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch OTC medicines: {e}")
        return []

def getPrescMedsForCustomer(customerID, variable):
    try:
        cursor = connection.cursor()
        query = """
            SELECT m.medID, m.medName, ms.dosage, ms.supID, m.price, ms.stockBought
            FROM prescriptions p
            JOIN medicines m ON p.medID = m.medID
            JOIN medSup ms ON m.medID = ms.medID
            WHERE p.customerID = %s AND ms.stockBought > 0;
        """
        cursor.execute(query, (customerID,))
        presc_meds = [f"{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]} - {row[5]} pcs" for row in cursor.fetchall()]
        variable.set("")  # Reset dropdown
        return presc_meds
    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch prescription medicines: {e}")
        return []

#----------------------------------------- SALE FUNCTIONS -----------------------------------------#
def navAddNewSale():
    """
    Navigate to the frame to select an existing customer for a new sale.
    """
    if connection is None:
        msg.showerror("Error", "Please connect to the database first.")
        return

    # Populate customer dropdown
    customerDropdownSale["values"] = getCustomersForSales(customerVar)
    showFrame(selectCustomerF)

def navAddSalesOTC():
    """
    Navigate to the frame to select OTC medicines for a new sale.
    """
    if not customerVar.get():
        msg.showerror("Error", "Please select a customer before proceeding.")
        return

    otcMedDropdown["values"] = getOTCMeds(selectedMedVar)
    showFrame(selectOTCMedicineF)

def navAddSalesPrescription():
    """
    Navigate to the frame to select prescription medicines for a new sale.
    """
    if not customerVar.get():
        msg.showerror("Error", "Please select a customer before proceeding.")
        return

    customerID = customerVar.get().split(" - ")[0]
    prescriptionMedDropdown["values"] = getPrescMedsForCustomer(customerID, selectedMedVar)
    if not prescriptionMedDropdown["values"]:
        msg.showerror("Error", "No prescription medicines available for the selected customer.")
        return

    showFrame(selectPrescriptionMedicineF)

def navConfirmQuantity():
    """
    Navigate to the frame to confirm the quantity of the selected medicine.
    """
    selected_medicine = selectedMedVar.get()
    print(selected_medicine)
    quantity = quantityVar.get()

    if not selected_medicine or not quantity:
        msg.showerror("Error", "Please select a medicine and enter a valid quantity.")
        return

    try:
        medID = selected_medicine.split(" - ")[0]
        stock = int(selected_medicine.split(" - ")[-1].split(" pcs")[0])
        price = float(selected_medicine.split(" - ")[-2])  # Assuming price is included in the dropdown

        quantity = int(quantity)
        if quantity <= 0:
            msg.showerror("Error", "Quantity must be a positive integer.")
            return
        if quantity > stock:
            msg.showerror("Error", "Requested quantity exceeds stock availability.")
            return

        # Save details for confirmation
        selectedMedVar.set(f"{medID} - {quantity} pcs - {price}")
        totalPriceLabel.config(text=f"Total Price: {price * quantity:.2f}")

        showFrame(confirmSaleF)
    except Exception as e:
        msg.showerror("Error", f"Invalid input: {e}")

def navCompleteSale():
    """
    Complete the sale and update the database.
    """
    try:
        selected_medicine = selectedMedVar.get()
        quantity = int(quantityVar.get())
        customerID = customerVar.get().split(" - ")[0]
        medID = selected_medicine.split(" - ")[0]
        mOP = mOPVar.get()

        if not mOP:
            msg.showerror("Error", "Please select a Mode of Payment.")
            return

        cursor = connection.cursor()
        cursor.execute("SELECT HasDisCard FROM customers WHERE customerID = %s", (customerID,))
        has_discount = cursor.fetchone()[0]
        discount = 0.2 if has_discount else 0

        cursor.execute(
            "SELECT presID FROM prescriptions WHERE customerID = %s AND medID = %s",
            (customerID, medID)
        )
        pres_result = cursor.fetchone()
        presID = pres_result[0] if pres_result else None

        cursor.execute("SELECT price FROM medicines WHERE medID = %s", (medID,))
        price_result = cursor.fetchone()
        if not price_result:
            msg.showerror("Error", "Medicine price not found in the database.")
            return

        price_per_unit = float(price_result[0])
        total_price = price_per_unit * quantity
        discounted_price = round(total_price * (1 - discount), 2)  # Ensure it's rounded to 2 decimal places

        cursor.execute("SELECT MAX(salesID) FROM sales;")
        result = cursor.fetchone()
        new_salesID = f"S{(int(result[0][1:]) + 1) if result[0] else 1:04d}"

        sale_query = """
            INSERT INTO sales (salesID, salesDate, quantitySold, totalPrice, medID, customerID, presID, mOP, discount)
            VALUES (%s, CURDATE(), %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(sale_query, (new_salesID, quantity, discounted_price, medID, customerID, presID, mOP, discount))

        stock_update_query = """
            UPDATE medSup SET stockBought = stockBought - %s
            WHERE medID = %s AND stockBought >= %s LIMIT 1;
        """
        cursor.execute(stock_update_query, (quantity, medID, quantity))

        connection.commit()
        msg.showinfo("Success", f"Sale completed successfully with ID: {new_salesID}")
        
        global arrF
        sales_frames = [selectCustomerF, selectOTCMedicineF, selectPrescriptionMedicineF, confirmSaleF]
        arrF = [frame for frame in arrF if frame not in sales_frames]
        
        showFrame(selectCustomerF)  # Navigate back to the customer selection frame
    except sql.Error as e:
        msg.showerror("Error", f"Failed to complete the sale: {e}")
    except Exception as e:
        msg.showerror("Error", f"Unexpected error occurred: {e}")

def navDeleteSales():
    """
    Navigate to the Delete Sales frame and populate the dropdown menu with deletable sales.
    """
    if connection is None:
        msg.showerror("Error", "Please connect to the database first.")
        return

    deletable_sales = getDeletableSales(deletableSalesVar)
    salesDropdown["values"] = deletable_sales

    showFrame(deleteSalesF)

def navViewAllSales():
    if connection is None:
        msg.showerror("Error", "Please connect to the database first.")
        return

    viewTable("sales")  # Use the universal viewTable function


def getDeletableSales(variable):
    """
    Fetch all sales IDs and populate the variable for dropdown.

    Args:
        variable (tk.StringVar): The variable for the dropdown menu.
    """
    try:
        cursor = connection.cursor()
        query = """
            SELECT salesID, salesDate, totalPrice
            FROM sales;
        """
        cursor.execute(query)
        sales = [f"{row[0]} - {row[1]} - PHP {row[2]:.2f}" for row in cursor.fetchall()]
        variable.set("")  # Reset dropdown
        return sales
    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch sales: {e}")
        return []

def deleteSales():
    """
    Delete a sale record from the sales table based on the selected salesID.
    """
    selected_sale = deletableSalesVar.get()

    if not selected_sale:
        msg.showerror("Error", "Please select a sale to delete.")
        return

    salesID = selected_sale.split(" - ")[0]  # Extract the salesID

    try:
        cursor = connection.cursor()

        # Confirm deletion
        confirmation = msg.askyesno("Confirm Deletion", f"Are you sure you want to delete Sale ID '{salesID}'?")
        if not confirmation:
            return

        # Delete the sale record
        delete_query = "DELETE FROM sales WHERE salesID = %s;"
        cursor.execute(delete_query, (salesID,))
        connection.commit()

        msg.showinfo("Success", f"Sale ID '{salesID}' deleted successfully.")

        # Refresh dropdown for deletable sales
        navDeleteSales()
    except sql.Error as e:
        msg.showerror("Error", f"Failed to delete sale: {e}")
    except Exception as e:
        msg.showerror("Error", f"Unexpected error occurred: {e}")


#---------------------------GUI-------------------------------------------#
# Main Application
root = tk.Tk()
root.title("Pharmacy DBMS")
root.geometry("1280x720")
root.resizable(False, False)

# Frames for GUI
loginF = tk.Frame(root, width=1280, height=720)
mainMenuF = tk.Frame(root, width=1280, height=720)

medMenuF = tk.Frame(root, width=1280, height=720)
medTableF = tk.Frame(root, width=1280, height=720)

cusMenuF = tk.Frame(root, width=1280, height=720)
cusTableF = tk.Frame(root, width=1280, height=720)

docMenuF = tk.Frame(root, width=1280, height=720)
docTableF = tk.Frame(root, width=1280, height=720)

presMenuF = tk.Frame(root, width=1280, height=720)
presTableF = tk.Frame(root, width=1280, height=720)

saleMenuF = tk.Frame(root, width=1280, height=720)
saleTableF = tk.Frame(root, width=1280, height=720)

supMenuF = tk.Frame(root, width=1280, height=720)
supTableF = tk.Frame(root, width=1280, height=720)

# ================= Login Frame =================
tk.Label(loginF, text="Login to MySQL Server", font=("Arial", 24)).pack(pady=20)
tk.Label(loginF, text="Host:", font=("Arial", 14)).pack(pady=10)
hostInput = tk.Entry(loginF, font=("Arial", 14), width=40)
hostInput.pack(pady=5)

tk.Label(loginF, text="User:", font=("Arial", 14)).pack(pady=10)
userInput = tk.Entry(loginF, font=("Arial", 14), width=40)
userInput.pack(pady=5)

tk.Label(loginF, text="Password:", font=("Arial", 14)).pack(pady=10)
passInput = tk.Entry(loginF, font=("Arial", 14), show="*", width=40)
passInput.pack(pady=5)

tk.Button(loginF, text="Connect", font=("Arial", 14), command=connectServer).pack(pady=20)

# ================= Main Menu Frame =================
tk.Label(mainMenuF, text="Main Menu - Select a Table", font=("Arial", 24)).pack(pady=20)

tableDisplay = tk.Listbox(mainMenuF, font=("Arial", 14), width=50, height=15)
tableDisplay.pack(pady=20)

tk.Button(mainMenuF, text="Select Table", font=("Arial", 14), command=selectTable).pack(pady=10)
tk.Button(mainMenuF, text="Monthly Report", font=("Arial", 14), command=navGenerateMonthlyReport).pack(pady=10)

tk.Button(mainMenuF, text="Back", font=("Arial", 14), command=goBack).pack(pady=20)

#==================View Table====================#
viewTableF = tk.Frame(root, width=1280, height=720)

# Title Label
viewTitleLabel = tk.Label(viewTableF, text="View Table", font=("Arial", 24))
viewTitleLabel.pack(pady=20)

# Treeview
viewTree = ttk.Treeview(viewTableF, height=25)
viewTree.pack(padx=20, pady=20, fill="both", expand=True)

# Back Button
tk.Button(viewTableF, text="Back", font=("Arial", 14), command=goBack).pack(pady=10)

# ================= Med Menu Frame =================
medTitleLabel = tk.Label(medMenuF, text="", font=("Arial", 24))
medTitleLabel.config(text=f"Table: Medicines")
medTitleLabel.pack(pady=20)

tk.Button(medMenuF, text="Add New Medicine", font=("Arial", 14), command=navAddMed).pack(pady=10)
tk.Button(medMenuF, text="Update Medicine", font=("Arial", 14), command=navUpdateMed).pack(pady=10)
tk.Button(medMenuF, text="Delete Medicine", font=("Arial", 14), command=navDeleteMedicine).pack(pady=10)
tk.Button(medMenuF, text="View All Medicines", font=("Arial", 14), command=showTableMed).pack(pady=10)
tk.Button(medMenuF, text="Low Stock Medicines", font=("Arial", 14), command=navLowStock).pack(pady=10)
tk.Button(medMenuF, text="Expiry Dates", font=("Arial", 14), command=navExpirationDates).pack(pady=10)

tk.Button(medMenuF, text="Back", font=("Arial", 14), command=goBack).pack(pady=20)

# =============== Med Table Frame ===================#
tk.Label(medTableF, text="Table Contents", font=("Arial", 24)).pack(pady=20)

medTree = ttk.Treeview(medTableF, height=20)
medTree.pack(padx=20, pady=20, fill="both", expand=True)

medSortLabel = tk.Label(medTableF, text="Sort by:", font=("Arial", 14))
medSortLabel.place(x=980, y=20, anchor="ne")  

medSort = ["ID","Name", "Dosage", "Expiry Date", "MedType", "Quantity In Stock"]
medSortVar = tk.StringVar(value=medSort[0])
medSortDrop = ttk.Combobox(medTableF, textvariable=medSortVar, values=medSort, state="readonly", font=("Arial", 14))
medSortDrop.place(x=1080, y=20, anchor="ne")  

sortButton = tk.Button(medTableF, text="Apply Sort", font=("Arial", 14), command=lambda: showTableMed(medSortVar.get()))
sortButton.place(x=1200, y=20, anchor="ne")  # Top-right button placement

tk.Button(medTableF, text="Back to Table Menu", font=("Arial", 9), command=goBack).pack(pady=20)

# ============ Add Medicine ======================#
# Frame for Adding New Medicine
addMedicineF = tk.Frame(root, width=1280, height=720)

# Title
tk.Label(addMedicineF, text="Add New Medicine", font=("Arial", 24)).grid(row=0, column=0, columnspan=2, pady=20)

# Medicine Name
tk.Label(addMedicineF, text="Medicine Name:", font=("Arial", 14)).grid(row=1, column=0, sticky="e", padx=10, pady=5)
nameInput = tk.Entry(addMedicineF, font=("Arial", 14), width=40)
nameInput.grid(row=1, column=1, sticky="w", padx=10, pady=5)

# Medicine Type
tk.Label(addMedicineF, text="Type (OTC/Prescription):", font=("Arial", 14)).grid(row=2, column=0, sticky="e", padx=10, pady=5)
medTypeVar = tk.StringVar(value="OTC")
medTypeDropdown = ttk.Combobox(addMedicineF, textvariable=medTypeVar, values=["OTC", "Prescription"], state="readonly", font=("Arial", 14), width=37)
medTypeDropdown.grid(row=2, column=1, sticky="w", padx=10, pady=5)

# Selling Price
tk.Label(addMedicineF, text="Selling Price (2 decimals):", font=("Arial", 14)).grid(row=3, column=0, sticky="e", padx=10, pady=5)
priceInput = tk.Entry(addMedicineF, font=("Arial", 14), width=40)
priceInput.grid(row=3, column=1, sticky="w", padx=10, pady=5)

# Supplier Selection
tk.Label(addMedicineF, text="Supplier:", font=("Arial", 14)).grid(row=4, column=0, sticky="e", padx=10, pady=5)
supplierVarMed = tk.StringVar()  # Variable to hold selected supplier
supplierDropdownMed = ttk.Combobox(addMedicineF, textvariable=supplierVarMed, state="readonly", font=("Arial", 14), width=37)
supplierDropdownMed.grid(row=4, column=1, sticky="w", padx=10, pady=5)

# Dosage
tk.Label(addMedicineF, text="Dosage (number only):", font=("Arial", 14)).grid(row=5, column=0, sticky="e", padx=10, pady=5)
dosageInput = tk.Entry(addMedicineF, font=("Arial", 14), width=40)
dosageInput.grid(row=5, column=1, sticky="w", padx=10, pady=5)

# Expiry Date
tk.Label(addMedicineF, text="Expiry Date (YYYY-MM-DD):", font=("Arial", 14)).grid(row=6, column=0, sticky="e", padx=10, pady=5)
expiryInput = tk.Entry(addMedicineF, font=("Arial", 14), width=40)
expiryInput.grid(row=6, column=1, sticky="w", padx=10, pady=5)

# Stock Bought
tk.Label(addMedicineF, text="Stock Bought:", font=("Arial", 14)).grid(row=7, column=0, sticky="e", padx=10, pady=5)
inStockInput = tk.Entry(addMedicineF, font=("Arial", 14), width=40)
inStockInput.grid(row=7, column=1, sticky="w", padx=10, pady=5)

# Price Bought
tk.Label(addMedicineF, text="Price Bought (2 decimals):", font=("Arial", 14)).grid(row=8, column=0, sticky="e", padx=10, pady=5)
priceBoughtInput = tk.Entry(addMedicineF, font=("Arial", 14), width=40)
priceBoughtInput.grid(row=8, column=1, sticky="w", padx=10, pady=5)

# Buttons
tk.Button(addMedicineF, text="Add Medicine", font=("Arial", 14), command=lambda: addNewMedicine()).grid(row=9, column=0, pady=20, sticky="e", padx=10)
tk.Button(addMedicineF, text="Back", font=("Arial", 14), command=goBack).grid(row=9, column=1, pady=20, sticky="w", padx=10)

# Configure the grid to adjust properly
addMedicineF.columnconfigure(0, weight=1)
addMedicineF.columnconfigure(1, weight=1)

#----------------------UpdateMedicine----------------------------------#
# Frame for Updating Medicine
updateMedicineF = tk.Frame(root, width=1280, height=720)

# Title
tk.Label(updateMedicineF, text="Update Medicine", font=("Arial", 24)).grid(row=0, column=0, columnspan=2, pady=20)

# Medicine ID Selection
tk.Label(updateMedicineF, text="Medicine ID:", font=("Arial", 14)).grid(row=1, column=0, sticky="e", padx=10, pady=5)
medicineIDVar = tk.StringVar()
medicineIDDropdown = ttk.Combobox(updateMedicineF, textvariable=medicineIDVar, state="readonly", font=("Arial", 14), width=40)
medicineIDDropdown.grid(row=1, column=1, sticky="w", padx=10, pady=5)

# Medicine Name
tk.Label(updateMedicineF, text="New Name (or NA):", font=("Arial", 14)).grid(row=2, column=0, sticky="e", padx=10, pady=5)
newNameInput = tk.Entry(updateMedicineF, font=("Arial", 14), width=40)
newNameInput.grid(row=2, column=1, sticky="w", padx=10, pady=5)

# Medicine Type
tk.Label(updateMedicineF, text="New Type (OTC/Prescription):", font=("Arial", 14)).grid(row=3, column=0, sticky="e", padx=10, pady=5)
newMedTypeVar = tk.StringVar(value="OTC")
newMedTypeDropdown = ttk.Combobox(updateMedicineF, textvariable=newMedTypeVar, values=["OTC", "Prescription"], state="readonly", font=("Arial", 14), width=37)
newMedTypeDropdown.grid(row=3, column=1, sticky="w", padx=10, pady=5)

# Price
tk.Label(updateMedicineF, text="New Price (2 decimals) (or NA):", font=("Arial", 14)).grid(row=4, column=0, sticky="e", padx=10, pady=5)
newPriceInput = tk.Entry(updateMedicineF, font=("Arial", 14), width=40)
newPriceInput.grid(row=4, column=1, sticky="w", padx=10, pady=5)

# Dosage
tk.Label(updateMedicineF, text="New Dosage (number only) (or NA):", font=("Arial", 14)).grid(row=5, column=0, sticky="e", padx=10, pady=5)
newDosageInput = tk.Entry(updateMedicineF, font=("Arial", 14), width=40)
newDosageInput.grid(row=5, column=1, sticky="w", padx=10, pady=5)

# Stock
tk.Label(updateMedicineF, text="New Stock Quantity (or NA):", font=("Arial", 14)).grid(row=6, column=0, sticky="e", padx=10, pady=5)
newStockInput = tk.Entry(updateMedicineF, font=("Arial", 14), width=40)
newStockInput.grid(row=6, column=1, sticky="w", padx=10, pady=5) 

# Buttons
tk.Button(updateMedicineF, text="Update Medicine", font=("Arial", 14), command=updateMedicine).grid(row=7, column=0, pady=20, sticky="e", padx=10)
tk.Button(updateMedicineF, text="Back", font=("Arial", 14), command=goBack).grid(row=7, column=1, pady=20, sticky="w", padx=10)

# ----------------------DeleteMedicine----------------------------------#
deleteMedicineF = tk.Frame(root, width=1280, height=720)

tk.Label(deleteMedicineF, text="Delete Medicine", font=("Arial", 24)).pack(pady=20)

tk.Label(deleteMedicineF, text="Select Medicine:", font=("Arial", 14)).pack(pady=10)
deletableMedicineVar = tk.StringVar()
deletableMedicineDropdown = ttk.Combobox(deleteMedicineF, textvariable=deletableMedicineVar, state="readonly", font=("Arial", 14), width=40)
deletableMedicineDropdown.pack(pady=5)

tk.Button(deleteMedicineF, text="Delete Medicine", font=("Arial", 14), command=deleteMedicine).pack(pady=20)
tk.Button(deleteMedicineF, text="Back", font=("Arial", 14), command=goBack).pack(pady=10)

#----------------------LowStock----------------------------------#
# Low Stock Frame
lowStockF = tk.Frame(root, width=1280, height=720)

tk.Label(lowStockF, text="Low Stock Medicines", font=("Arial", 24)).pack(pady=20)

# Treeview for displaying low-stock medicines
lowStockTree = ttk.Treeview(lowStockF, columns=("Name", "Dosage", "Stock", "Supplier"), show="headings", height=20)
lowStockTree.pack(fill="both", expand=True)

lowStockTree.heading("Name", text="Medicine Name")
lowStockTree.heading("Dosage", text="Dosage")
lowStockTree.heading("Stock", text="Stock")
lowStockTree.heading("Supplier", text="Supplier")

# Add Refresh and Back Buttons
tk.Button(lowStockF, text="Refresh", font=("Arial", 14), command=displayLowStock).pack(pady=10)
tk.Button(lowStockF, text="Back", font=("Arial", 14), command=goBack).pack(pady=10)

#----------------------ExpirationDates----------------------------------#
# Frame for Viewing Expiration Dates
expirationDatesF = tk.Frame(root, width=1280, height=720)

# Title
tk.Label(expirationDatesF, text="Medicine Expiration Dates", font=("Arial", 24)).pack(pady=20)

# Treeview for displaying expiration data
expirationTree = ttk.Treeview(expirationDatesF, columns=("Name", "Dosage", "Supplier", "Expiry Date"), show="headings", height=20)
expirationTree.pack(fill="both", expand=True)

expirationTree.heading("Name", text="Medicine Name")
expirationTree.heading("Dosage", text="Dosage")
expirationTree.heading("Supplier", text="Supplier")
expirationTree.heading("Expiry Date", text="Expiry Date")

# Buttons
tk.Button(expirationDatesF, text="Refresh", font=("Arial", 14), command=displayExpirationDates).pack(pady=10)
tk.Button(expirationDatesF, text="Back", font=("Arial", 14), command=goBack).pack(pady=10)

#----------------------InventoryReport----------------------------------#
# Frame for Inventory Report
inventoryReportF = tk.Frame(root, width=1280, height=720)

# Title
tk.Label(inventoryReportF, text="Inventory Report", font=("Arial", 24)).pack(pady=20)

# Input Fields for Year and Month
tk.Label(inventoryReportF, text="Enter Year:", font=("Arial", 14)).pack(pady=5)
yearInput = tk.Entry(inventoryReportF, font=("Arial", 14), width=10)
yearInput.pack(pady=5)

tk.Label(inventoryReportF, text="Enter Month (1-12):", font=("Arial", 14)).pack(pady=5)
monthInput = tk.Entry(inventoryReportF, font=("Arial", 14), width=10)
monthInput.pack(pady=5)

# Treeview for displaying the report
reportTree = ttk.Treeview(inventoryReportF, columns=("ID", "Name", "Dosage", "Quantity", "Supplier"), show="headings", height=20)
reportTree.pack(fill="both", expand=True)

reportTree.heading("ID", text="Medicine ID")
reportTree.heading("Name", text="Medicine Name")
reportTree.heading("Dosage", text="Dosage Form")
reportTree.heading("Quantity", text="Quantity in Stock")
reportTree.heading("Supplier", text="Supplier Name")

# Buttons
tk.Button(inventoryReportF, text="Generate Report", font=("Arial", 14), command=displayInventoryReport).pack(pady=10)
tk.Button(inventoryReportF, text="Back", font=("Arial", 14), command=goBack).pack(pady=10)

#----------------------CusMenu----------------------------------#

cusMenuTitle = tk.Label(cusMenuF, text="", font=("Arial", 24))
cusMenuTitle.config(text=f"Table: Customers")
cusMenuTitle.pack(pady=20)

tk.Button(cusMenuF, text="Add New Customer", font=("Arial", 14), command=navCreateCustomer).pack(pady=10)
tk.Button(cusMenuF, text="Update Customer", font=("Arial", 14), command=navupdateCustomer).pack(pady=10)
tk.Button(cusMenuF, text="Delete Customer", font=("Arial", 14), command=navDeleteCustomer).pack(pady=10)
tk.Button(cusMenuF, text="View All Customers", font=("Arial", 14), command=showTableCus).pack(pady=10)

tk.Button(cusMenuF, text="Back", font=("Arial", 14), command=goBack).pack(pady=20)

#-----------------------CusTable---------------------------------#

tk.Label(cusTableF, text="Table Contents", font=("Arial", 24)).pack(pady=20)

cusTree = ttk.Treeview(cusTableF, height=20)
cusTree.pack(padx=20, pady=20, fill="both", expand=True)

cusSortLabel = tk.Label(cusTableF, text="Sort by:", font=("Arial", 14))
cusSortLabel.place(x=980, y=20, anchor="ne")  

cusSort = ["ID","Last Name", "First Name", "Discount Card"]
cusSortVar = tk.StringVar(value=cusSort[0])
cusSortDrop = ttk.Combobox(cusTableF, textvariable=cusSortVar, values=cusSort, state="readonly", font=("Arial", 14))
cusSortDrop.place(x=1080, y=20, anchor="ne")  

sortButton = tk.Button(cusTableF, text="Apply Sort", font=("Arial", 14), command=lambda: showTableCus(cusSortVar.get()))
sortButton.place(x=1200, y=20, anchor="ne")  # Top-right button placement

tk.Button(cusTableF, text="Back to Table Menu", font=("Arial", 9), command=goBack).pack(pady=20)

#----------------------CreateCustomer----------------------------------#
# Frame for Create Customer
createCustomerF = tk.Frame(root, width=1280, height=720)

# Title
tk.Label(createCustomerF, text="Create New Customer", font=("Arial", 24)).pack(pady=20)

# Last Name Input
tk.Label(createCustomerF, text="Last Name:", font=("Arial", 14)).pack(pady=5)
customerLastNameInput = tk.Entry(createCustomerF, font=("Arial", 14), width=40)
customerLastNameInput.pack(pady=5)

# First Name Input
tk.Label(createCustomerF, text="First Name:", font=("Arial", 14)).pack(pady=5)
customerFirstNameInput = tk.Entry(createCustomerF, font=("Arial", 14), width=40)
customerFirstNameInput.pack(pady=5)

# Discount Card Status
tk.Label(createCustomerF, text="Has Discount Card (0 = No, 1 = Yes):", font=("Arial", 14)).pack(pady=5)
hasDiscountCardVar = tk.IntVar(value=0)
tk.Radiobutton(createCustomerF, text="No", variable=hasDiscountCardVar, value=0, font=("Arial", 12)).pack()
tk.Radiobutton(createCustomerF, text="Yes", variable=hasDiscountCardVar, value=1, font=("Arial", 12)).pack()

# Buttons
tk.Button(createCustomerF, text="Create Customer", font=("Arial", 14), command=createCustomer).pack(pady=20)
tk.Button(createCustomerF, text="Back", font=("Arial", 14), command=goBack).pack(pady=10)

#----------------------UpdateCus----------------------------------#
# Frame for Update Customer
updateCustomerF = tk.Frame(root, width=1280, height=720)

# Title
tk.Label(updateCustomerF, text="Update Customer", font=("Arial", 24)).pack(pady=20)

# Dropdown for Customer Selection
tk.Label(updateCustomerF, text="Select Customer:", font=("Arial", 14)).pack(pady=5)
updateCustomerVar = tk.StringVar()
customerDropdownNON = ttk.Combobox(updateCustomerF, textvariable=updateCustomerVar, state="readonly", font=("Arial", 14), width=50)
customerDropdownNON.pack(pady=5)

# Input Fields for Updating
tk.Label(updateCustomerF, text="Last Name (or NA):", font=("Arial", 14)).pack(pady=5)
updateCustomerLastNameInput = tk.Entry(updateCustomerF, font=("Arial", 14), width=40)
updateCustomerLastNameInput.pack(pady=5)

tk.Label(updateCustomerF, text="First Name (or NA):", font=("Arial", 14)).pack(pady=5)
updateCustomerFirstNameInput = tk.Entry(updateCustomerF, font=("Arial", 14), width=40)
updateCustomerFirstNameInput.pack(pady=5)

tk.Label(updateCustomerF, text="Has Discount Card (0 = No, 1 = Yes, or NA):", font=("Arial", 14)).pack(pady=5)
updateCustomerDiscountInput = tk.Entry(updateCustomerF, font=("Arial", 14), width=40)
updateCustomerDiscountInput.pack(pady=5)

# Buttons
tk.Button(updateCustomerF, text="Update Customer", font=("Arial", 14), command=lambda: updateCustomer()).pack(pady=20)
tk.Button(updateCustomerF, text="Back", font=("Arial", 14), command=goBack).pack(pady=10)

#----------------------DeleteCustomer----------------------------------#
# Frame for Delete Customer
deleteCustomerF = tk.Frame(root, width=1280, height=720)

# Title
tk.Label(deleteCustomerF, text="Delete Customer", font=("Arial", 24)).pack(pady=20)

# Dropdown for Customer Selection
tk.Label(deleteCustomerF, text="Select Customer to Delete:", font=("Arial", 14)).pack(pady=5)
deleteCustomerVar = tk.StringVar()
customerDeleteDropdown = ttk.Combobox(deleteCustomerF, textvariable=deleteCustomerVar, state="readonly", font=("Arial", 14), width=50)
customerDeleteDropdown.pack(pady=5)

# Buttons
tk.Button(deleteCustomerF, text="Delete Customer", font=("Arial", 14), command=lambda: deleteCustomer()).pack(pady=20)
tk.Button(deleteCustomerF, text="Back", font=("Arial", 14), command=goBack).pack(pady=10)

#----------------------DocMenu----------------------------------#

docMenuTitle = tk.Label(docMenuF, text="", font=("Arial", 24))
docMenuTitle.config(text=f"Table: Doctors")
docMenuTitle.pack(pady=20)

#tk.Button(medMenuF, text="Show Table", font=("Arial", 14), command=[EDIT]).pack(pady=10)
tk.Button(docMenuF, text="Add New Doctor", font=("Arial", 14), command=navCreateDoctor).pack(pady=10)
tk.Button(docMenuF, text="Update Doctor", font=("Arial", 14), command=navUpdateDoctor).pack(pady=10)
tk.Button(docMenuF, text="Delete Doctor", font=("Arial", 14), command=navDeleteDoctor).pack(pady=10)
tk.Button(docMenuF, text="View All Doctors", font=("Arial", 14), command=navViewDoctors).pack(pady=10)

tk.Button(docMenuF, text="Back", font=("Arial", 14), command=goBack).pack(pady=20)

#----------------------CreateDoc----------------------------------#
# Frame for Create Doctor
createDoctorF = tk.Frame(root, width=1280, height=720)

# Title
tk.Label(createDoctorF, text="Create New Doctor", font=("Arial", 24)).pack(pady=20)

# Last Name Input
tk.Label(createDoctorF, text="Last Name:", font=("Arial", 14)).pack(pady=5)
doctorLastNameInput = tk.Entry(createDoctorF, font=("Arial", 14), width=40)
doctorLastNameInput.pack(pady=5)

# First Name Input
tk.Label(createDoctorF, text="First Name:", font=("Arial", 14)).pack(pady=5)
doctorFirstNameInput = tk.Entry(createDoctorF, font=("Arial", 14), width=40)
doctorFirstNameInput.pack(pady=5)

# Buttons
tk.Button(createDoctorF, text="Create Doctor", font=("Arial", 14), command=createDoctor).pack(pady=20)
tk.Button(createDoctorF, text="Back", font=("Arial", 14), command=goBack).pack(pady=10)

#----------------------UpdateDoc----------------------------------#
# Frame for Update Doctor
updateDoctorF = tk.Frame(root, width=1280, height=720)

# Title
tk.Label(updateDoctorF, text="Update Doctor", font=("Arial", 24)).pack(pady=20)

# Dropdown for Doctor Selection
tk.Label(updateDoctorF, text="Select Doctor:", font=("Arial", 14)).pack(pady=5)
updateDoctorVar = tk.StringVar()
doctorDropdownNON = ttk.Combobox(updateDoctorF, textvariable=updateDoctorVar, state="readonly", font=("Arial", 14), width=50)
doctorDropdownNON.pack(pady=5)

# Input Fields for Updating
tk.Label(updateDoctorF, text="Last Name (or NA):", font=("Arial", 14)).pack(pady=5)
updateDoctorLastNameInput = tk.Entry(updateDoctorF, font=("Arial", 14), width=40)
updateDoctorLastNameInput.pack(pady=5)

tk.Label(updateDoctorF, text="First Name (or NA):", font=("Arial", 14)).pack(pady=5)
updateDoctorFirstNameInput = tk.Entry(updateDoctorF, font=("Arial", 14), width=40)
updateDoctorFirstNameInput.pack(pady=5)

# Buttons
tk.Button(updateDoctorF, text="Update Doctor", font=("Arial", 14), command=lambda: updateDoctor()).pack(pady=20)
tk.Button(updateDoctorF, text="Back", font=("Arial", 14), command=goBack).pack(pady=10)

#----------------------DeleteDoc----------------------------------#
# Frame for Delete Doctor
deleteDoctorF = tk.Frame(root, width=1280, height=720)

# Title
tk.Label(deleteDoctorF, text="Delete Doctor", font=("Arial", 24)).pack(pady=20)

# Dropdown for Doctor Selection
tk.Label(deleteDoctorF, text="Select Doctor to Delete:", font=("Arial", 14)).pack(pady=5)
deleteDoctorVar = tk.StringVar()
doctorDeleteDropdown = ttk.Combobox(deleteDoctorF, textvariable=deleteDoctorVar, state="readonly", font=("Arial", 14), width=50)
doctorDeleteDropdown.pack(pady=5)

# Buttons
tk.Button(deleteDoctorF, text="Delete Doctor", font=("Arial", 14), command=lambda: deleteDoctor()).pack(pady=20)
tk.Button(deleteDoctorF, text="Back", font=("Arial", 14), command=goBack).pack(pady=10)













#----------------------PresMenu----------------------------------#

presMenuTitle = tk.Label(presMenuF, text="", font=("Arial", 24))
presMenuTitle.config(text=f"Table: Prescriptions")
presMenuTitle.pack(pady=20)

#tk.Button(medMenuF, text="Show Table", font=("Arial", 14), command=[EDIT]).pack(pady=10)
tk.Button(presMenuF, text="Add New Prescription", font=("Arial", 14), command=navAddPrescription).pack(pady=10)
tk.Button(presMenuF, text="Update Prescription", font=("Arial", 14), command=navUpdatePrescription).pack(pady=10)
tk.Button(presMenuF, text="Delete Prescription", font=("Arial", 14), command=navDeletePresc).pack(pady=10)
tk.Button(presMenuF, text="View All Prescriptions", font=("Arial", 14), command=navViewPrescriptions).pack(pady=10)

tk.Button(presMenuF, text="Back", font=("Arial", 14), command=goBack).pack(pady=20)



#----------------------addPres----------------------------------#
# Frame for Adding New Prescription
addPrescriptionF = tk.Frame(root, width=1280, height=720)

# Title
tk.Label(addPrescriptionF, text="Add New Prescription", font=("Arial", 24)).pack(pady=20)

# Dropdown for Customer Selection
tk.Label(addPrescriptionF, text="Select Customer:", font=("Arial", 14)).pack(pady=5)
customerVar = tk.StringVar()
customerDropdown = ttk.Combobox(addPrescriptionF, textvariable=customerVar, state="readonly", font=("Arial", 14), width=50)
customerDropdown.pack(pady=5)

# Dropdown for Prescription Medicine
tk.Label(addPrescriptionF, text="Select Medicine:", font=("Arial", 14)).pack(pady=5)
prescriptionMedVar = tk.StringVar()
prescriptionMedDropdown = ttk.Combobox(addPrescriptionF, textvariable=prescriptionMedVar, state="readonly", font=("Arial", 14), width=50)
prescriptionMedDropdown.pack(pady=5)

# Dropdown for Doctor Selection
tk.Label(addPrescriptionF, text="Select Doctor:", font=("Arial", 14)).pack(pady=5)
doctorVar = tk.StringVar()
doctorDropdown = ttk.Combobox(addPrescriptionF, textvariable=doctorVar, state="readonly", font=("Arial", 14), width=50)
doctorDropdown.pack(pady=5)

# Buttons
tk.Button(addPrescriptionF, text="Add Prescription", font=("Arial", 14), command=lambda: addNewPrescription()).pack(pady=20)
tk.Button(addPrescriptionF, text="Back", font=("Arial", 14), command=goBack).pack(pady=10)

#----------------------UpdatePres----------------------------------#
# Frame for Updating Prescription
updatePrescriptionF = tk.Frame(root, width=1280, height=720)

# Title
tk.Label(updatePrescriptionF, text="Update Prescription", font=("Arial", 24)).grid(row=0, column=0, columnspan=2, pady=20)

# Dropdown for Selecting Customer and Prescription ID
tk.Label(updatePrescriptionF, text="Select Customer and Prescription ID:", font=("Arial", 14)).grid(row=1, column=0, sticky="e", padx=10, pady=5)
prescSelectionVar = tk.StringVar()
prescSelectionDropdown = ttk.Combobox(updatePrescriptionF, textvariable=prescSelectionVar, state="readonly", font=("Arial", 14), width=50)
prescSelectionDropdown.grid(row=1, column=1, sticky="w", padx=10, pady=5)

# Dropdown for Prescription Medicine
tk.Label(updatePrescriptionF, text="New Prescription Medicine:", font=("Arial", 14)).grid(row=2, column=0, sticky="e", padx=10, pady=5)
newPrescMedVar = tk.StringVar()
newPrescMedDropdown = ttk.Combobox(updatePrescriptionF, textvariable=newPrescMedVar, state="readonly", font=("Arial", 14), width=50)
newPrescMedDropdown.grid(row=2, column=1, sticky="w", padx=10, pady=5)

# Dropdown for Doctor
tk.Label(updatePrescriptionF, text="New Doctor:", font=("Arial", 14)).grid(row=3, column=0, sticky="e", padx=10, pady=5)
newDoctorVar = tk.StringVar()
newDoctorDropdown = ttk.Combobox(updatePrescriptionF, textvariable=newDoctorVar, state="readonly", font=("Arial", 14), width=50)
newDoctorDropdown.grid(row=3, column=1, sticky="w", padx=10, pady=5)

# Buttons
tk.Button(updatePrescriptionF, text="Update Prescription", font=("Arial", 14), command=lambda: updatePrescription()).grid(row=4, column=0, pady=20, sticky="e", padx=10)
tk.Button(updatePrescriptionF, text="Back", font=("Arial", 14), command=goBack).grid(row=4, column=1, pady=20, sticky="w", padx=10)

# Configure the grid to adjust properly
updatePrescriptionF.columnconfigure(0, weight=1)
updatePrescriptionF.columnconfigure(1, weight=1)

#----------------------DeletePres----------------------------------#
# Frame for Delete Prescription
deletePrescriptionF = tk.Frame(root, width=1280, height=720)

# Title
tk.Label(deletePrescriptionF, text="Delete Prescription", font=("Arial", 24)).pack(pady=20)

# Dropdown for selecting deletable prescriptions
tk.Label(deletePrescriptionF, text="Select Prescription (ID - Customer Name):", font=("Arial", 14)).pack(pady=10)
deletablePrescriptionVar = tk.StringVar()
deletablePrescriptionDropdown = ttk.Combobox(
    deletePrescriptionF,
    textvariable=deletablePrescriptionVar,
    state="readonly",
    font=("Arial", 14),
    width=50
)
deletablePrescriptionDropdown.pack(pady=5)

# Buttons
tk.Button(deletePrescriptionF, text="Delete Prescription", font=("Arial", 14), command=deletePrescription).pack(pady=20)
tk.Button(deletePrescriptionF, text="Back", font=("Arial", 14), command=goBack).pack(pady=10)

# Configure the grid layout to adjust properly
deletePrescriptionF.columnconfigure(0, weight=1)
deletePrescriptionF.columnconfigure(1, weight=1)


#----------------------SaleMenu----------------------------------#
saleMenuTitle = tk.Label(saleMenuF, text="", font=("Arial", 24))
saleMenuTitle.config(text=f"Table: Sales")
saleMenuTitle.pack(pady=20)

#tk.Button(medMenuF, text="Show Table", font=("Arial", 14), command=[EDIT]).pack(pady=10)
tk.Button(saleMenuF, text="Add New Sale", font=("Arial", 14), command=navAddNewSale).pack(pady=10)
tk.Button(saleMenuF, text="Delete Sales", font=("Arial", 14), command=navDeleteSales).pack(pady=10)
tk.Button(saleMenuF, text="View All Sales", font=("Arial", 14), command=navViewAllSales).pack(pady=10)


tk.Button(saleMenuF, text="Back", font=("Arial", 14), command=goBack).pack(pady=20)


selectedMedVar = tk.StringVar()
quantityVar = tk.StringVar()
customerVar = tk.StringVar()
mOPVar = tk.StringVar()



#----------------------GUI Frames----------------------------------#
# Frame for selecting a customer
selectCustomerF = tk.Frame(root, width=1280, height=720)
tk.Label(selectCustomerF, text="Select Customer", font=("Arial", 24)).pack(pady=20)
tk.Label(selectCustomerF, text="Customer:", font=("Arial", 14)).pack(pady=10)
customerDropdownSale = ttk.Combobox(selectCustomerF, textvariable=customerVar, font=("Arial", 14), width=50, state="readonly")
customerDropdownSale.pack(pady=10)
tk.Button(selectCustomerF, text="OTC Medicines", font=("Arial", 14), command=navAddSalesOTC).pack(pady=10)
tk.Button(selectCustomerF, text="Prescription Medicines", font=("Arial", 14), command=navAddSalesPrescription).pack(pady=10)
tk.Button(selectCustomerF, text="Back", font=("Arial", 14), command=goBack).pack(pady=20)

# Frame for selecting OTC medicines
selectOTCMedicineF = tk.Frame(root, width=1280, height=720)
tk.Label(selectOTCMedicineF, text="Select OTC Medicine", font=("Arial", 24)).pack(pady=20)
tk.Label(selectOTCMedicineF, text="OTC Medicine:", font=("Arial", 14)).pack(pady=10)
otcMedDropdown = ttk.Combobox(selectOTCMedicineF, textvariable=selectedMedVar, font=("Arial", 14), width=50, state="readonly")
otcMedDropdown.pack(pady=10)
tk.Label(selectOTCMedicineF, text="Quantity:", font=("Arial", 14)).pack(pady=10)
tk.Entry(selectOTCMedicineF, textvariable=quantityVar, font=("Arial", 14), width=10).pack(pady=10)
tk.Button(selectOTCMedicineF, text="Next", font=("Arial", 14), command=navConfirmQuantity).pack(pady=10)
tk.Button(selectOTCMedicineF, text="Back", font=("Arial", 14), command=goBack).pack(pady=20)

# Frame for selecting prescription medicines
selectPrescriptionMedicineF = tk.Frame(root, width=1280, height=720)
tk.Label(selectPrescriptionMedicineF, text="Select Prescription Medicine", font=("Arial", 24)).pack(pady=20)
tk.Label(selectPrescriptionMedicineF, text="Prescription Medicine:", font=("Arial", 14)).pack(pady=10)
prescriptionMedDropdown = ttk.Combobox(selectPrescriptionMedicineF, textvariable=selectedMedVar, font=("Arial", 14), width=50, state="readonly")
prescriptionMedDropdown.pack(pady=10)
tk.Label(selectPrescriptionMedicineF, text="Quantity:", font=("Arial", 14)).pack(pady=10)
tk.Entry(selectPrescriptionMedicineF, textvariable=quantityVar, font=("Arial", 14), width=10).pack(pady=10)
tk.Button(selectPrescriptionMedicineF, text="Next", font=("Arial", 14), command=navConfirmQuantity).pack(pady=10)
tk.Button(selectPrescriptionMedicineF, text="Back", font=("Arial", 14), command=goBack).pack(pady=20)

# Frame for confirming the sale
confirmSaleF = tk.Frame(root, width=1280, height=720)
tk.Label(confirmSaleF, text="Confirm Sale", font=("Arial", 24)).pack(pady=20)
totalPriceLabel = tk.Label(confirmSaleF, text="Total Price: 0.00", font=("Arial", 18))
totalPriceLabel.pack(pady=20)
tk.Label(confirmSaleF, text="Mode of Payment:", font=("Arial", 14)).pack(pady=10)
mOPDropdown = ttk.Combobox(confirmSaleF, textvariable=mOPVar, font=("Arial", 14), width=30, state="readonly")
mOPDropdown["values"] = ["Cash", "E-Wallet", "Card"]
mOPDropdown.pack(pady=10)
tk.Button(confirmSaleF, text="Complete Sale", font=("Arial", 14), command=navCompleteSale).pack(pady=10)
tk.Button(confirmSaleF, text="Back", font=("Arial", 14), command=goBack).pack(pady=20)

#------------------------DELETESales--------------------------#
# Frame for Deleting Sales
deleteSalesF = tk.Frame(root, width=1280, height=720)

# Title
tk.Label(deleteSalesF, text="Delete Sale", font=("Arial", 24)).pack(pady=20)

# Dropdown for Sales
tk.Label(deleteSalesF, text="Select Sale to Delete:", font=("Arial", 14)).pack(pady=10)
deletableSalesVar = tk.StringVar()
salesDropdown = ttk.Combobox(deleteSalesF, textvariable=deletableSalesVar, font=("Arial", 14), width=50, state="readonly")
salesDropdown.pack(pady=10)

# Buttons
tk.Button(deleteSalesF, text="Delete Sale", font=("Arial", 14), command=deleteSales).pack(pady=10)
tk.Button(deleteSalesF, text="Back", font=("Arial", 14), command=goBack).pack(pady=20)






#----------------------SupMenu----------------------------------#

supMenuTitle = tk.Label(supMenuF, text="", font=("Arial", 24))
supMenuTitle.config(text=f"Table: Suppliers")
supMenuTitle.pack(pady=20)

#tk.Button(medMenuF, text="Show Table", font=("Arial", 14), command=[EDIT]).pack(pady=10)
tk.Button(supMenuF, text="Add New Supplier", font=("Arial", 14), command=navCreateSupplier).pack(pady=10)
tk.Button(supMenuF, text="Update Supplier", font=("Arial", 14), command=navUpdateSupplier).pack(pady=10)
tk.Button(supMenuF, text="Delete Supplier", font=("Arial", 14), command=navDeleteSupplier).pack(pady=10)
tk.Button(supMenuF, text="View All Suppliers", font=("Arial", 14), command=navViewSupplier).pack(pady=10)

tk.Button(supMenuF, text="Back", font=("Arial", 14), command=goBack).pack(pady=20)

#----------------------CreateSup----------------------------------#
# Frame for Create Supplier
createSupplierF = tk.Frame(root, width=1280, height=720)

# Title
tk.Label(createSupplierF, text="Create New Supplier", font=("Arial", 24)).pack(pady=20)

# Supplier Name Input
tk.Label(createSupplierF, text="Supplier Name:", font=("Arial", 14)).pack(pady=5)
supplierNameInput = tk.Entry(createSupplierF, font=("Arial", 14), width=40)
supplierNameInput.pack(pady=5)

# Contact Input
tk.Label(createSupplierF, text="Contact (Required):", font=("Arial", 14)).pack(pady=5)
contactInput = tk.Entry(createSupplierF, font=("Arial", 14), width=40)
contactInput.pack(pady=5)

# Buttons
tk.Button(createSupplierF, text="Create Supplier", font=("Arial", 14), command=createSupplier).pack(pady=20)
tk.Button(createSupplierF, text="Back", font=("Arial", 14), command=goBack).pack(pady=10)

#----------------------UpdateSup----------------------------------#
# Frame for Update Supplier
updateSupplierF = tk.Frame(root, width=1280, height=720)

# Title
tk.Label(updateSupplierF, text="Update Supplier", font=("Arial", 24)).pack(pady=20)

# Dropdown for Supplier Selection
tk.Label(updateSupplierF, text="Select Supplier:", font=("Arial", 14)).pack(pady=5)
updateSupplierVar = tk.StringVar()
supplierDropdown = ttk.Combobox(updateSupplierF, textvariable=updateSupplierVar, state="readonly", font=("Arial", 14), width=50)
supplierDropdown.pack(pady=5)

# Input Fields for Updating
tk.Label(updateSupplierF, text="Supplier Name (or NA):", font=("Arial", 14)).pack(pady=5)
updateSupplierNameInput = tk.Entry(updateSupplierF, font=("Arial", 14), width=40)
updateSupplierNameInput.pack(pady=5)

tk.Label(updateSupplierF, text="Contact (or NA):", font=("Arial", 14)).pack(pady=5)
updateSupplierContactInput = tk.Entry(updateSupplierF, font=("Arial", 14), width=40)
updateSupplierContactInput.pack(pady=5)

# Buttons
tk.Button(updateSupplierF, text="Update Supplier", font=("Arial", 14), command=lambda: updateSupplier()).pack(pady=20)
tk.Button(updateSupplierF, text="Back", font=("Arial", 14), command=goBack).pack(pady=10)

#----------------------DeleteSup----------------------------------#
# Frame for Delete Supplier
deleteSupplierF = tk.Frame(root, width=1280, height=720)

# Title
tk.Label(deleteSupplierF, text="Delete Supplier", font=("Arial", 24)).pack(pady=20)

# Dropdown for Supplier Selection
tk.Label(deleteSupplierF, text="Select Supplier to Delete:", font=("Arial", 14)).pack(pady=5)
deleteSupplierVar = tk.StringVar()
supplierDeleteDropdown = ttk.Combobox(deleteSupplierF, textvariable=deleteSupplierVar, state="readonly", font=("Arial", 14), width=50)
supplierDeleteDropdown.pack(pady=5)

# Buttons
tk.Button(deleteSupplierF, text="Delete Supplier", font=("Arial", 14), command=lambda: deleteSupplier()).pack(pady=20)
tk.Button(deleteSupplierF, text="Back", font=("Arial", 14), command=goBack).pack(pady=10)

#--------------------GENERATE REPORTS--------------------------#
# Frame for generating monthly reports
generateReportF = tk.Frame(root, width=1280, height=720)

# Title
tk.Label(generateReportF, text="Generate Monthly Report", font=("Arial", 24)).pack(pady=20)

# Report Type Dropdown
tk.Label(generateReportF, text="Report Type:", font=("Arial", 14)).pack(pady=10)
reportTypeVar = tk.StringVar()
reportTypeDropdown = ttk.Combobox(generateReportF, textvariable=reportTypeVar, font=("Arial", 14), width=30, state="readonly")
reportTypeDropdown["values"] = ["sales", "suppliers", "prescriptions", "medicines"]
reportTypeDropdown.pack(pady=10)

# Year Entry
tk.Label(generateReportF, text="Year:", font=("Arial", 14)).pack(pady=10)
yearVar = tk.StringVar()
yearEntry = tk.Entry(generateReportF, textvariable=yearVar, font=("Arial", 14), width=10)
yearEntry.pack(pady=10)

# Month Entry
tk.Label(generateReportF, text="Month:", font=("Arial", 14)).pack(pady=10)
monthVar = tk.StringVar()
monthEntry = tk.Entry(generateReportF, textvariable=monthVar, font=("Arial", 14), width=10)
monthEntry.pack(pady=10)

# Generate Button
tk.Button(generateReportF, text="Generate Report", font=("Arial", 14), command=lambda: generateMonthlyReport(reportTypeVar.get(), int(yearVar.get()), int(monthVar.get()))).pack(pady=20)

# Back Button
tk.Button(generateReportF, text="Back", font=("Arial", 14), command=goBack).pack(pady=20)






#-------------------------------------------------------------#
arrF.append(loginF)
showFrame(loginF)

root.mainloop()