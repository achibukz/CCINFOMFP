import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import mysql.connector as sql

connection = None
onTable = None
arrF = []  

def showFrame(nextF):
    # REMEMBER TO ADD NEW FRAMES TO THIS LIST
    listF = [loginF, mainMenuF, medMenuF, medTableF, cusMenuF,cusTableF, docMenuF, docTableF, medSupMenuF, medSupTableF, presMenuF, presTableF, saleMenuF, saleTableF, supMenuF, supTableF, addMedicineF]

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
            database="finaldbpharma"
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
        "medsup": medSupMenuF,
        "prescriptions": presMenuF,
        "sales": saleMenuF,
        "suppliers": supMenuF,
    }

    nextFrame = tableFrame.get(onTable)
    showFrame(nextFrame) 

def letterKeyRemover(medId):
    num = ''.join(filter(str.isdigit, medId))  
    return int(num) if num else 0 

def navAddMed():
    showFrame(addMedicineF)

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
    

def addNewMedicine():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(medId) FROM medicines;")
        result = cursor.fetchone()
        if result[0]:
            highest_numeric_id = letterKeyRemover(result[0])  
            next_medId = highest_numeric_id + 1 
        else:
            next_medId = 1  

        new_medId = f"A{next_medId}"

        name = nameInput.get().strip()
        dosage = dosageInput.get().strip()  
        expiry_date = expiryInput.get().strip()
        med_type = medTypeVar.get()
        in_stock = inStockInput.get().strip()
        price = priceInput.get().strip()

        if not name or not dosage or not expiry_date or not med_type or not in_stock or not price:
            msg.showerror("Error", "All fields must be filled out.")
            return

        dosage_numeric = int(dosage)  
        dosage_with_unit = f"{dosage_numeric}mg"  

        query = """
            INSERT INTO medicines (medId, name, dosage, expiry_date, medType, inStock, price)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query, (new_medId, name, dosage_with_unit, expiry_date, med_type, in_stock, price))
        connection.commit()

        msg.showinfo("Success", f"New medicine added with medId: {next_medId}")
    except sql.Error as e:
        msg.showerror("Error", f"Failed to add new medicine: {e}")
    except ValueError:
        msg.showerror("Error", "Invalid input. Please check the entered values.")




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

medSupMenuF = tk.Frame(root, width=1280, height=720)
medSupTableF = tk.Frame(root, width=1280, height=720)

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

tk.Button(medMenuF, text="Show Table", font=("Arial", 14), command=showTableMed).pack(pady=10)
tk.Button(medMenuF, text="Add New Medicine", font=("Arial", 14), command=navAddMed).pack(pady=10)
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
addMedicineF = tk.Frame(root, width=1280, height=720)

tk.Label(addMedicineF, text="Add New Medicine", font=("Arial", 24)).pack(pady=20)

tk.Label(addMedicineF, text="Name:", font=("Arial", 14)).pack(pady=10)
nameInput = tk.Entry(addMedicineF, font=("Arial", 14), width=40)
nameInput.pack(pady=5)

tk.Label(addMedicineF, text="Dosage (number only):", font=("Arial", 14)).pack(pady=10)
dosageInput = tk.Entry(addMedicineF, font=("Arial", 14), width=40)
dosageInput.pack(pady=5)

tk.Label(addMedicineF, text="Expiry Date (YYYY-MM-DD):", font=("Arial", 14)).pack(pady=10)
expiryInput = tk.Entry(addMedicineF, font=("Arial", 14), width=40)
expiryInput.pack(pady=5)

tk.Label(addMedicineF, text="Type (OTC/Prescription):", font=("Arial", 14)).pack(pady=10)
medTypeVar = tk.StringVar(value="OTC")
medTypeDropdown = ttk.Combobox(addMedicineF, textvariable=medTypeVar, values=["OTC", "Prescription"], state="readonly", font=("Arial", 14))
medTypeDropdown.pack(pady=5)

tk.Label(addMedicineF, text="In Stock:", font=("Arial", 14)).pack(pady=10)
inStockInput = tk.Entry(addMedicineF, font=("Arial", 14), width=40)
inStockInput.pack(pady=5)

tk.Label(addMedicineF, text="Price (2 decimals):", font=("Arial", 14)).pack(pady=10)
priceInput = tk.Entry(addMedicineF, font=("Arial", 14), width=40)
priceInput.pack(pady=5)

tk.Button(addMedicineF, text="Add Medicine", font=("Arial", 14), command=addNewMedicine).pack(pady=20)
tk.Button(addMedicineF, text="Back", font=("Arial", 14), command=goBack).pack(pady=10)

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

#----------------------MedSupMenu----------------------------------#

medSupMenuTitle = tk.Label(medSupMenuF, text="", font=("Arial", 24))
medSupMenuTitle.config(text=f"Table: Medicine Suppliers")
medSupMenuTitle.pack(pady=20)

#tk.Button(medMenuF, text="Show Table", font=("Arial", 14), command=[EDIT]).pack(pady=10)
tk.Button(medSupMenuF, text="Back", font=("Arial", 14), command=goBack).pack(pady=20)

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