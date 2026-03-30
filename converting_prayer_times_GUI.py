import pandas as pd
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox

def run_conversion():
    # 1. Get values from the GUI
    excel_path = entry_excel.get()
    db_name = entry_db.get()
    table_name = entry_table.get()

    if not excel_path or not db_name or not table_name:
        messagebox.showerror("Error", "Please fill in all fields!")
        return

    # Ensure DB name ends with .db
    if not db_name.endswith('.db'):
        db_name += '.db'

    try:
        # 2. Load and Clean Excel
        df = pd.read_excel(excel_path)
        df.columns = df.columns.str.strip().str.lower()

        # 3. Bulletproof Formatting
        time_cols = ['fajr', 'sunrise', 'dhuhur', 'asr', 'maghrib', 'ishaa']
        for col in time_cols:
            if col in df.columns:
                # Force to string and grab the HH:MM part
                df[col] = df[col].astype(str).str.strip().str.split().str[-1].str.slice(0, 5)
                # Pad with leading zero (e.g., 6:35 -> 06:35)
                df[col] = df[col].apply(lambda x: f"0{x}" if len(x) == 4 and ":" in x else x)

        # 4. Add ID column if it doesn't exist
        if 'id' not in df.columns:
            df.insert(0, 'id', range(1, 1 + len(df)))

        # 5. Database Connection
        conn = sqlite3.connect(db_name)
        
        # Select only relevant columns
        final_cols = ['id', 'month', 'day', 'fajr', 'sunrise', 'dhuhur', 'asr', 'maghrib', 'ishaa']
        df_final = df[[c for c in final_cols if c in df.columns]]

        # 6. Save to SQLite
        df_final.to_sql(table_name, conn, if_exists='replace', index=False)
        
        # 7. Re-apply Unique Constraint
        conn.execute(f'CREATE UNIQUE INDEX IF NOT EXISTS idx_date_{table_name} ON {table_name} (month, day)')
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", f"Converted {len(df)} rows into {db_name}!")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    entry_excel.delete(0, tk.END)
    entry_excel.insert(0, filename)

# --- GUI Setup ---
root = tk.Tk()
root.title("Prayer Times SQLite Converter")
root.geometry("500x300")
root.padx = 20
root.pady = 20

# Excel Path
tk.Label(root, text="Excel File Path:").pack(pady=(10, 0))
frame_excel = tk.Frame(root)
frame_excel.pack()
entry_excel = tk.Entry(frame_excel, width=50)
entry_excel.pack(side=tk.LEFT, padx=5)
tk.Button(frame_excel, text="Browse", command=browse_file).pack(side=tk.LEFT)

# DB Name
tk.Label(root, text="Database Name (e.g., sweden_prayer.db):").pack(pady=(10, 0))
entry_db = tk.Entry(root, width=60)
entry_db.pack()

# Table Name
tk.Label(root, text="Table Name (e.g., göteborg_times):").pack(pady=(10, 0))
entry_table = tk.Entry(root, width=60)
entry_table.pack()

# Run Button
tk.Button(root, text="CONVERT TO SQLITE", bg="green", fg="white", font=("Arial", 10, "bold"), 
          command=run_conversion).pack(pady=25)

root.mainloop()