import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import gspread
from numpy import empty
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",
        'https://www.googleapis.com/auth/spreadsheets',
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"]



#CREDENTIALS FROM GOOGLE SERVICE ACCOUNT
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1Pfn_Dx_hEWGChU74iamO3BM4giSL7MpbuepGVo6_Bpk")  
styleDtlSheet = sheet.worksheet("code")
SamplePOMSheet = sheet.worksheet("RAWDATA")

# root window
root = tk.Tk()
root.geometry("300x250")
root.resizable(False, False)
root.title('Style Details')

# store email address and password
stylenum = tk.StringVar()
sizeset = tk.StringVar()
view = tk.StringVar()

views = ('Front', 'Back', 'Other')
selected_view = tk.StringVar()

sizes = ('XS', 'S', 'M','L', 'XL', 'XXL')
selected_sizes = tk.StringVar()


def login_clicked():
    """ callback when the button clicked
    """
    msg = f'You entered stylenum: {stylenum.get()}, stylenum: {sizeset_entry.get()}, and view: {view_entry.get()}'
    styleDtlSheet.update('B2', stylenum.get())
    styleDtlSheet.update('B3', sizeset_entry.get())
    styleDtlSheet.update('B4', view_entry.get())

    showinfo(
        title='Information',
        message=msg
    )




def clear_clicked():

    """ callback when the button clicked
    """
    msg = f'You clear all data results!'
    # SamplePOMSheet.clear('R2:R', "")
    range_of_cells = SamplePOMSheet.range('R2:R1000')
    for cell in range_of_cells:
        cell.value = ''
    SamplePOMSheet.update_cells(range_of_cells) 
  

    showinfo(
        title='Information',
        message=msg
    )

# Sign in frame
proceed = ttk.Frame(root)
proceed.pack(padx=10, pady=10, fill='x', expand=True)


# stylenums
stylenum_label = ttk.Label(proceed, text="Style Number:")
stylenum_label.pack(fill='x', expand=True)

stylenum_entry = ttk.Entry(proceed, textvariable=stylenum)
stylenum_entry.pack(fill='x', expand=True)
stylenum_entry.focus()

# sizesets
sizeset_label = ttk.Label(proceed, text="Sizeset:")
sizeset_label.pack(fill='x', expand=True)

sizeset_entry = ttk.Combobox(proceed, textvariable=selected_sizes)
sizeset_entry['values'] = sizes
sizeset_entry['state'] = 'readonly'  # normal
sizeset_entry.pack(fill='x', expand=True)


# views
view_label = ttk.Label(proceed, text="View:")
view_label.pack(fill='x', expand=True)

view_entry = ttk.Combobox(proceed, textvariable=selected_view)
view_entry['values'] = views
view_entry['state'] = 'readonly'  # normal
view_entry.pack(fill='x', expand=True)

# login button
proceed_button = ttk.Button(proceed, text="Proceed", command=login_clicked)
proceed_button.pack(fill='x', expand=True, pady=10)

# login button
clear_button = ttk.Button(proceed, text="Clear", command=clear_clicked)
clear_button.pack(fill='x', expand=True, pady=10)

root.mainloop()
