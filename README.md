# Excel Data Obfuscation Script

This script takes one or more **Excel (.xlsx) files** and produces an **obfuscated version** of the data.  
It is designed for IT/security personnel who need to share example data externally **without revealing sensitive information**, while keeping the **column names, headings, and structure** identical.

The script does **not** modify the original files.  
All obfuscated files are written into a separate folder.


---

# 📝 Instructions

Follow these steps to use the obfuscation script:

1. Make sure you have Python and the required packages installed. To test this, you can 
run the following commands:

```
WanderingThoughts:script dburfoot$ python3
Python 3.9.6 (default, Feb  3 2024, 15:58:27) 
[Clang 15.0.0 (clang-1500.3.9.4)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import pandas as pd
>>> import openpyxl
```

The exact version is not critical, but we need Pandas and openpyxl to read the Excel files.
Please do a Google/GPT conversation for help with installing Python and Python packages.


2. **Get the repository**
   Download the project using either:
   - `git clone https://github.com/comperical/excel-obfuscator.git`
   - or **Download ZIP** → extract it to a folder on your computer.


2b. Review the code to make sure you are comfortable with it. It is a single short Python script.
If you are unsure about something, I am happy to go over it with you, or you can consult
GPT to answer any questions.

3. Run the script on the test data. The repo includes some `.xlsx` files to use as test data.
Open a shell to the repo directory, and run:

```
python3 excel_obfuscator.py
```

If everything is installed correctly, you should see this kind of output:
```
WanderingThoughts:script dburfoot$ python3 excel_obfuscator.py 
Going to obfuscate file: 
    /opt/userdata/external/excel-obfuscator/original/Offenses_P.xlsx
    /opt/userdata/external/excel-obfuscator/obfuscated/Offenses_P.xlsx
Going to obfuscate file: 
    /opt/userdata/external/excel-obfuscator/original/EnergyOverview.xlsx
    /opt/userdata/external/excel-obfuscator/obfuscated/EnergyOverview.xlsx
Going to obfuscate file: 
    /opt/userdata/external/excel-obfuscator/original/historicalcpi_P.xlsx
    /opt/userdata/external/excel-obfuscator/obfuscated/historicalcpi_P.xlsx
```



4. **Create a folder for your original data**  
   Make a directory such as:  

```
C:\ClientData\original
```

and place your Excel files (`.xlsx`) inside it.

5. **Edit the Python script to point to your data**  
At the top of the script, update:  
```
INPUT_DIRECTORY = Path("C:\ClientData\original")
```

You can also update the Obfuscated directory path if desired,
    if you don't change it, the code will use a sibling directory to the original folder,
    with the name `obfuscated`.


6. Review the Obfuscated data. Open the `.xlsx` files that have been created,
    and confirm that the obfuscation code has worked.


6b. (Optional). Since the obfuscation is very strict, it may be necessary to preserve
    a few "landmark" cells in the data. To preserve a cell, edit the content
    so that it has the exact prefix `PRESERVE:`.
    The code will not obfuscate cells with this prefix.
    Rerun the obfuscator and confirm that the preserved cells are readable as expected.

7. Share the obfuscated Excel data files.




## What the Script Does

For every Excel file in the Input directory, it creates a <b>obfuscated</b> copy of the file
in the Obfuscated directory.


The header row is preserved if present, but all data values are transformed using the following rules:

### Obfuscation Rules

| Data Type | Obfuscation Method |
|----------|---------------------|
| **Strings (text)** | Hashed using SHA-256 (12-character hex). |
| **Strings that look like dates** | Converted to a real date, then shifted by +90 days. |
| **Strings beginning with `PRESERVE:`** | Not obfuscated. The prefix `PRESERVE:` is removed, keeping the original value. |
| **Numbers** | Random ±20% noise applied (configurable). |
| **Dates** | Shifted forward +90 days. |
| **Booleans** | Randomized. |
| **Blanks / NaN** | Left unchanged. |

All sheets within each workbook are processed automatically.

---

## Requirements

### 1. Install Python (Windows)

If you do not already have Python installed:

1. Download Python from:  
   **https://www.python.org/downloads/windows/**
2. During installation, **check the box** that says:  
   **“Add Python to PATH”**
3. Complete the installer.

### 2. Install the Required Python Packages

Open **Command Prompt** and run:

```cmd
pip install pandas openpyxl
```
