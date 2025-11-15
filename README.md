# Excel Data Obfuscation Script

This script takes one or more **Excel (.xlsx) files** and produces an **obfuscated version** of the data.  
It is designed for IT/security personnel who need to share example data externally **without revealing sensitive information**, while keeping the **column names, headings, and structure** identical.

The script does **not** modify the original files.  
All obfuscated files are written into a separate folder.

---



```
original/
```


---

# ❗ Before You Run the Script: Update the Input Folder Path

At the top of the Python script, you will see this section:

```python
# ----------- CONFIGURATION ------------


...

# Date shift (in days)
DATE_SHIFT_DAYS = 90

# Enter the path to the original data here
INPUT_DIRECTORY = Path("C:/PATH/TO/YOUR/ORIGINAL/FOLDER")

...
# --------------------------------------
```

You should edit the source code to point to the location of your original data.



## What the Script Does

For every Excel file in the Input directory, it creates a <b>obfuscated</b> copy of the file
in the Obfuscated directory.


The **header row is preserved exactly**, but all data values are transformed using the following rules:

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
