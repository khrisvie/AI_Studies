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

#view_entries()

#def summary():
    df = pd.read_csv("data.csv")

    if df.empty:
        print("No data to analyze.")
        return

    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    
    grouped = df.groupby("Category", as_index=False)["Amount"].sum()
    grouped.columns = ["Category", "Total Amount"]

    print(grouped.to_string(index=False))

#summary()

#def average():
    df = pd.read_csv("data.csv")

    if df.empty:
        print("No data to analyze.")
        return
    
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    grouped = df.groupby("Category", as_index=False)["Amount"].mean()
    grouped.columns = ["Category", "Average Amount"]

    print(grouped.to_string(index=False))

#average()

#def count():
    df = pd.read_csv("data.csv")

    if df.empty:
        print("No data to analyze.")
        return
    
    counts = df.groupby("Category", as_index=False).size()
    counts.columns = ["Category", "Number of entries"]

    print(counts.to_string(index=False))

#count()


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

statistics()