
import os
import pandas as pd
import hashlib
import random
import datetime

from pathlib import Path

# ----------- CONFIGURATION ------------
# Noise for numeric values (e.g., ±20%)
NUMERIC_NOISE_PCT = 0.20

# Date shift (in days)
DATE_SHIFT_DAYS = 90

# Enter the path to the original data here
INPUT_DIRECTORY = Path(__file__).parent.parent / "original"

# Will create a sibling directory called "obfuscated"
OBFUS_DIRECTORY = INPUT_DIRECTORY.parent / "obfuscated"


# --------------------------------------

def hash_string(s: str) -> str:
    """Deterministic pseudonymization for strings."""
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]

def obfuscate_value(v):
    # Preserve empty/NaN
    if pd.isna(v):
        return v

    # Convert numpy types to Python built-ins
    if hasattr(v, 'item'):
        try:
            v = v.item()
        except:
            pass


    # ---- PRESERVE logic ----
    if isinstance(v, str) and v.startswith("PRESERVE:"):
        return v[len("PRESERVE:"):]  # keep original value


    # ---- Strings ----
    if isinstance(v, str):
        # If it looks like a date, try to parse
        try:
            dt = pd.to_datetime(v)
            shifted = dt + pd.to_timedelta(DATE_SHIFT_DAYS, unit='D')
            return shifted.strftime("%Y-%m-%d")
        except:
            pass

        # Otherwise treat as text
        return hash_string(v)

    # ---- Numbers ----
    if isinstance(v, (int, float)):
        noise = 1 + random.uniform(-NUMERIC_NOISE_PCT, NUMERIC_NOISE_PCT)
        return round(v * noise, 2)

    # ---- Dates ----
    if isinstance(v, (datetime.date, datetime.datetime)):
        return v + datetime.timedelta(days=DATE_SHIFT_DAYS)

    # ---- Booleans ----
    if isinstance(v, bool):
        return random.choice([True, False])

    # Fallback (rare)
    return hash_string(str(v))


def obfuscate_excel(infile, outfile):
    # Load workbook
    xls = pd.ExcelFile(infile)

    with pd.ExcelWriter(outfile, engine="openpyxl") as writer:
        for sheet in xls.sheet_names:
            df = pd.read_excel(infile, sheet_name=sheet)

            # Modern replacement for applymap
            df_obf = df.apply(lambda col: col.map(obfuscate_value))

            # Write result
            df_obf.to_excel(writer, index=False, sheet_name=sheet)



# ------------------ RUN ------------------


if __name__ == '__main__':

    assert os.path.exists(OBFUS_DIRECTORY), f"You must create the obfuscated directory {OBFUS_DIRECTORY}"

    for f in os.listdir(INPUT_DIRECTORY):

        orgpath = INPUT_DIRECTORY / f
        obspath = OBFUS_DIRECTORY / f
        print(f"Going to obfuscate file: \n\t{orgpath}\n\t{obspath}")


        obfuscate_excel(orgpath, obspath)

