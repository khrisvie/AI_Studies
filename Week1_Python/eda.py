#%%
import csv
import pandas as pd
from IPython.display import display


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

view_entries()
