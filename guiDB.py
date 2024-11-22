import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import mysql.connector as sql
from datetime import date

connection = None
onTable = None
arrF = []  

#----------------------------------------- UNIVERSAL FUNCTIONS -----------------------------------------#

def showFrame(nextF):
    # REMEMBER TO ADD NEW FRAMES TO THIS LIST
    listF = [loginF, mainMenuF, medMenuF, medTableF, cusMenuF,cusTableF, docMenuF, docTableF, presMenuF, presTableF, saleMenuF, saleTableF, supMenuF, supTableF, addMedicineF
             , updateMedicineF, deleteMedicineF, lowStockF, expirationDatesF]

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

def navAddMed():
    if connection is None:  # Ensure a connection exists before fetching suppliers
        msg.showerror("Error", "Please connect to the database first.")
        return
    getSuppliers()  # Populate the supplier dropdown
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

def getSuppliers():
    try:
        cursor = connection.cursor()
        query = "SELECT supID, supName FROM suppliers;"
        cursor.execute(query)
        suppliers = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]  # Combine ID and name for clarity
        supplierVar.set("")  # Reset the combobox selection
        supplierDropdown["values"] = suppliers  # Populate the dropdown
    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch suppliers: {e}")

def getMedName():
    try:
        cursor = connection.cursor()
        query = """
            SELECT m.medName, s.dosage
            FROM medicines m
            JOIN medSup s ON m.medID = s.medID;
        """
        cursor.execute(query)
        medData = cursor.fetchall()
        medicine_dropdown_values = [f"{row[0]} - {row[1]}" for row in medData]  
        medicineIDDropdown["values"] = medicine_dropdown_values  
    except sql.Error as e:
        msg.showerror("Error", f"Failed to fetch medicine names and dosages: {e}")

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

#----------------------------------------- MEDICINE FUNCTIONS -----------------------------------------#

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
        supplier = supplierVar.get().strip()
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
            dosage_value = int(dosage)
            if dosage_value <= 0:
                msg.showerror("Error", "Dosage must be a positive integer.")
                check = 0
                return
            dosage = f"{dosage_value}mg"
        except ValueError:
            msg.showerror("Error", "Dosage must be a valid integer.")
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

    except sql.Error as e:
        msg.showerror("Error", f"Failed to add new medicine: {e}")
    except Exception as e:
        msg.showerror("Error", f"Unexpected error: {e}")

def updateMedicine():
    try:
        selected_medicine = medicineIDVar.get()
        if not selected_medicine:
            msg.showerror("Error", "Please select a medicine.")
            return
        
        medicine_name = selected_medicine.split(" - ")[0]

        new_name = newNameInput.get().strip()
        new_med_type = newMedTypeVar.get().strip()
        new_price = newPriceInput.get().strip()
        new_dosage = newDosageInput.get().strip()
        new_stock = newStockInput.get().strip()

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
            update_query = f"UPDATE medicines SET {', '.join(update_queries)} WHERE medName = %s;"
            update_values.append(medicine_name)
            cursor = connection.cursor()
            cursor.execute(update_query, tuple(update_values))

        medsup_updates = []
        medsup_values = []

        if new_dosage and new_dosage != "NA":
            try:
                new_dosage = int(new_dosage)
                if new_dosage <= 0:
                    msg.showerror("Error", "Dosage must be a positive integer.")
                    return
                new_dosage = f"{new_dosage}mg"
                medsup_updates.append("dosage = %s")
                medsup_values.append(new_dosage)
            except ValueError:
                msg.showerror("Error", "Dosage must be a valid integer.")
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
            medsup_query = f"UPDATE medSup SET {', '.join(medsup_updates)} WHERE medID = (SELECT medID FROM medicines WHERE medName = %s);"
            medsup_values.append(medicine_name)
            cursor.execute(medsup_query, tuple(medsup_values))

        # Commit the transaction
        connection.commit()
        msg.showinfo("Success", f"Medicine '{medicine_name}' updated successfully.")

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
    
#---------------------------GUI SHIT-------------------------------------------#
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
tk.Button(mainMenuF, text="Back", font=("Arial", 14), command=goBack).pack(pady=20)

# ================= Med Menu Frame =================
medTitleLabel = tk.Label(medMenuF, text="", font=("Arial", 24))
medTitleLabel.config(text=f"Table: Medicines")
medTitleLabel.pack(pady=20)

tk.Button(medMenuF, text="Records", font=("Arial", 14), command=showTableMed).pack(pady=10)
tk.Button(medMenuF, text="Add New Medicine", font=("Arial", 14), command=navAddMed).pack(pady=10)
tk.Button(medMenuF, text="Update Medicine", font=("Arial", 14), command=navUpdateMed).pack(pady=10)
tk.Button(medMenuF, text="Delete Medicine", font=("Arial", 14), command=navDeleteMedicine).pack(pady=10)
tk.Button(medMenuF, text="Low Stock Medicines", font=("Arial", 14), command=navLowStock).pack(pady=10)
tk.Button(medMenuF, text="Expiry Dates", font=("Arial", 14), command=navExpirationDates).pack(pady=10)
tk.Button(medMenuF, text="Inventory Report", font=("Arial", 14), command=navInventoryReport).pack(pady=10)

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
supplierVar = tk.StringVar()  # Variable to hold selected supplier
supplierDropdown = ttk.Combobox(addMedicineF, textvariable=supplierVar, state="readonly", font=("Arial", 14), width=37)
supplierDropdown.grid(row=4, column=1, sticky="w", padx=10, pady=5)

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
tk.Button(addMedicineF, text="Add Medicine", font=("Arial", 14), command=addNewMedicine).grid(row=9, column=0, pady=20, sticky="e", padx=10)
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
tk.Label(updateMedicineF, text="New Name:", font=("Arial", 14)).grid(row=2, column=0, sticky="e", padx=10, pady=5)
newNameInput = tk.Entry(updateMedicineF, font=("Arial", 14), width=40)
newNameInput.grid(row=2, column=1, sticky="w", padx=10, pady=5)

# Medicine Type
tk.Label(updateMedicineF, text="New Type (OTC/Prescription):", font=("Arial", 14)).grid(row=3, column=0, sticky="e", padx=10, pady=5)
newMedTypeVar = tk.StringVar(value="OTC")
newMedTypeDropdown = ttk.Combobox(updateMedicineF, textvariable=newMedTypeVar, values=["OTC", "Prescription"], state="readonly", font=("Arial", 14), width=37)
newMedTypeDropdown.grid(row=3, column=1, sticky="w", padx=10, pady=5)

# Price
tk.Label(updateMedicineF, text="New Price (2 decimals):", font=("Arial", 14)).grid(row=4, column=0, sticky="e", padx=10, pady=5)
newPriceInput = tk.Entry(updateMedicineF, font=("Arial", 14), width=40)
newPriceInput.grid(row=4, column=1, sticky="w", padx=10, pady=5)

# Dosage
tk.Label(updateMedicineF, text="New Dosage (number only):", font=("Arial", 14)).grid(row=5, column=0, sticky="e", padx=10, pady=5)
newDosageInput = tk.Entry(updateMedicineF, font=("Arial", 14), width=40)
newDosageInput.grid(row=5, column=1, sticky="w", padx=10, pady=5)

# Stock
tk.Label(updateMedicineF, text="New Stock Quantity:", font=("Arial", 14)).grid(row=6, column=0, sticky="e", padx=10, pady=5)
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

tk.Button(cusMenuF, text="Show Table", font=("Arial", 14), command=showTableCus).pack(pady=10)
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

#----------------------DocMenu----------------------------------#

docMenuTitle = tk.Label(docMenuF, text="", font=("Arial", 24))
docMenuTitle.config(text=f"Table: Doctors")
docMenuTitle.pack(pady=20)

#tk.Button(medMenuF, text="Show Table", font=("Arial", 14), command=[EDIT]).pack(pady=10)
tk.Button(docMenuF, text="Back", font=("Arial", 14), command=goBack).pack(pady=20)

#----------------------PresMenu----------------------------------#

presMenuTitle = tk.Label(presMenuF, text="", font=("Arial", 24))
presMenuTitle.config(text=f"Table: Prescriptions")
presMenuTitle.pack(pady=20)

#tk.Button(medMenuF, text="Show Table", font=("Arial", 14), command=[EDIT]).pack(pady=10)
tk.Button(presMenuF, text="Back", font=("Arial", 14), command=goBack).pack(pady=20)

#----------------------SaleMenu----------------------------------#

saleMenuTitle = tk.Label(saleMenuF, text="", font=("Arial", 24))
saleMenuTitle.config(text=f"Table: Sales")
saleMenuTitle.pack(pady=20)

#tk.Button(medMenuF, text="Show Table", font=("Arial", 14), command=[EDIT]).pack(pady=10)
tk.Button(saleMenuF, text="Back", font=("Arial", 14), command=goBack).pack(pady=20)

#----------------------SupMenu----------------------------------#

supMenuTitle = tk.Label(supMenuF, text="", font=("Arial", 24))
supMenuTitle.config(text=f"Table: Suppliers")
supMenuTitle.pack(pady=20)

#tk.Button(medMenuF, text="Show Table", font=("Arial", 14), command=[EDIT]).pack(pady=10)
tk.Button(supMenuF, text="Back", font=("Arial", 14), command=goBack).pack(pady=20)

#-------------------------------------------------------------#
arrF.append(loginF)
showFrame(loginF)

root.mainloop()