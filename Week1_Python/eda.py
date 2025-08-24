#%%
import csv
import pandas as pd
from IPython.display import display
import tkinter as tk
import matplotlib.pyplot as plt


def add_entry():
    with open("data.csv", mode="a", newline="") as data_csv:
        fieldnames = ["Date","Category","Description","Amount","Currency"]
        writer = csv.DictWriter(data_csv, fieldnames=fieldnames)

        while True:
            date = input("Enter date: ")
            category = input("Enter category: ")
            description = input("Enter description: ")
            amount = input("Enter amount: ")
            amount_ = ''.join(filter(lambda c: c.isdigit() or c == '.', amount))
            currency = ''.join(filter(lambda c: not c.isdigit() and c != '.', amount))
        
            if not currency:
                currency = input("Enter currency symbol: ")

            amount_ = float(amount_)
            writer.writerow({
                "Date": date,
                "Category": category,
                "Description": description,
                "Amount": amount_,
                "Currency": currency
              })
            print("Added!")
            more = input("Add another entry? (y/n): ").strip().lower()
            if more != "y":
                break

#add_entry()

def view_entries():
    df = pd.read_csv("data.csv")
    
    if df.empty:
        print("No entries to display.")
        return
    
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df = df.sort_values("Date")
    df["Date"] = df["Date"].dt.strftime("%d.%m.%Y")
   
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Amount"] = df["Amount"].apply(lambda x: f"{x:,.2f}") + " " + df["Currency"]
   
    df["Currency"] = df["Currency"].astype(str).fillna("")
     
    display_df = df[["Date", "Category", "Description", "Amount"]]
    
    display(display_df)

#view_entries()


def statistics():
    df = pd.read_csv("data.csv")

    if df.empty:
        print("No data to analyze.")
        return
    
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    grouped = df.groupby("Category", as_index=False).agg(
        Total_Amount=("Amount", "sum"),
        Average_Amount=("Amount", "mean"),
        Num_Entries=("Amount", "count")
    ).reset_index()

    grouped = grouped.round(2)
    print(grouped.to_string(index=False))

#statistics()

def edit_entry():
    df = pd.read_csv("data.csv")

    if df.empty:
        print("No data to edit.")
        return
    
    display(df)

    index = int(input("Enter the index of the entry: "))
    column = str(input("Enter the name of the column: ")) 
   
    if index not in df.index:
        print(f"No entry found at index {index}. ")
        return
    elif column not in df.columns:
        print(f"No entry found in the column {column}. ")
        return
    
    new_value = input("Edit the data: ")

    df.at[index, column] = new_value
    df.to_csv("data.csv", index=False)

    print(f"Entry {index} updated: {column} -> {new_value}")
    
    display(df)

#edit_entry()

def delete_entry():
    df = pd.read_csv("data.csv")

    if df.empty:
        print("No data to edit.")
        return
    
    display(df)

    index = int(input("Enter the index of the entry: "))
    if index not in df.index:
        print(f"No entry found at index {index}. ")
        return
    
    df = df.drop(index)

    df.to_csv("data.csv", index=False)
    print(f"Entry {index} deleted successfully.")

    display(df)

#delete_entry()

def visualize_totals():
    df = pd.read_csv("data.csv")
    if df.empty:
        print("No data to visualize.")
        return
    
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    grouped = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    plt.figure(figsize=(8,5))
    grouped.plot(kind="bar", color="skyblue", edgecolor="black")
    plt.title("Total Expenses per Category")
    plt.xlabel("Category")
    plt.ylabel("Total Amount")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("300x300")

btn_add = tk.Button(root, text="Add Entry", width=20, command=add_entry)
btn_view = tk.Button(root, text="View Entries", width=20, command=view_entries)
btn_edit = tk.Button(root, text="Edit Entries", width=20, command=edit_entry)
btn_delete = tk.Button(root, text="Delete Entry", width=20, command=delete_entry)
btn_summary = tk.Button(root, text="Summary", width=20, command=statistics)
btn_visualize = tk.Button(root, text="Visualize Totals", width=20, command=visualize_totals)

btn_add.pack(pady=5)
btn_view.pack(pady=5)
btn_edit.pack(pady=5)
btn_delete.pack(pady=5)
btn_summary.pack(pady=5)
btn_visualize.pack(pady=5)

root.mainloop()