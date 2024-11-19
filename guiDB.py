import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import mysql.connector as sql

connection = None
onTable = None
arrF = []  

def showFrame(nextF):
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

def letterKeyRemover(medId):
    num = ''.join(filter(str.isdigit, medId))  # Keep only digits
    return int(num) if num else 0  # Return as an integer, default to 0 if no digits


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
    showFrame(medMenuF) 
    medTitleLabel.config(text=f"Table: {onTable}")

def navAddMed():
    showFrame(addMedicineF)

def showTableMed(sort_by="Name"):

    sort_column_map = {
        "ID": "medId",
        "Name": "name",
        "Dosage": "dosage",
        "Expiry Date": "expiry_date",
        "MedType": "medType",
        "Quantity In Stock": "inStock"
    }
    sort_column = sort_column_map.get(sort_by, "medId")  # Default to sorting by Name
    
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
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(medId) FROM medicines;")
        result = cursor.fetchone()
        if result[0]:
            highest_numeric_id = letterKeyRemover(result[0])  # Extract numeric part
            next_medId = highest_numeric_id + 1  # Increment by 1
        else:
            next_medId = 1  # Default to 1 if no records exist

        # Step 2: Format medId with a prefix (e.g., 'A' + next_medId)
        new_medId = f"A{next_medId}"

        # Step 2: Get user inputs
        name = nameInput.get().strip()
        dosage = dosageInput.get().strip()  # Keep it as a string
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
medTitleLabel.pack(pady=20)

tk.Button(medMenuF, text="Show Table", font=("Arial", 14), command=showTableMed).pack(pady=10)
tk.Button(medMenuF, text="Add New Medicine", font=("Arial", 14), command=navAddMed).pack(pady=10)
tk.Button(medMenuF, text="Back", font=("Arial", 14), command=goBack).pack(pady=20)

# =============== Med Table Frame ===================#
tk.Label(medTableF, text="Table Contents", font=("Arial", 24)).pack(pady=20)

medTree = ttk.Treeview(medTableF, height=20)
medTree.pack(padx=20, pady=20, fill="both", expand=True)

# Dropdown for sorting
medSortLabel = tk.Label(medTableF, text="Sort by:", font=("Arial", 14))
medSortLabel.place(x=980, y=20, anchor="ne")  

medSort = ["ID","Name", "Dosage", "Expiry Date", "MedType", "Quantity In Stock"]
medSortVar = tk.StringVar(value=medSort[0])
medSortDrop = ttk.Combobox(medTableF, textvariable=medSortVar, values=medSort, state="readonly", font=("Arial", 14))
medSortDrop.place(x=1080, y=20, anchor="ne")  

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

#----------------------------------------------------------------#

sortButton = tk.Button(medTableF, text="Apply Sort", font=("Arial", 14), command=lambda: showTableMed(medSortVar.get()))
sortButton.place(x=1200, y=20, anchor="ne")  # Top-right button placement

tk.Button(medTableF, text="Back to Table Menu", font=("Arial", 9), command=goBack).pack(pady=20)

#------------------------------------------------------------------------#
arrF.append(loginF)
showFrame(loginF)

root.mainloop()
