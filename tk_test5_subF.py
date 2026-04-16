import os 
import re
import zipfile
import threading
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

# Folders
OUT_F = "output_cleaned"
TEMP_F = "temp_extract"

WORDS = ["sum", "CAG", "Changi", "airport", "CT05", "Joestar", "Brando", "Kujo",
         "Higashikata", "Giovanna", "Jojo", "Salve", "sumus", "Oblectate",
         "salve", "parve", "Gaudeo", "Simulare", "Perdere", "Para",
         "Pilis", "Nunc", "Hic", "Petitionis", "nostrae", "quam",
         "tibi", "summae", "barbarus", "albinus", "culex", "et",
         "mea", "libido", "0", "5"]

os.makedirs(OUT_F, exist_ok=True)
os.makedirs(TEMP_F, exist_ok=True)

# ---------------- BACKEND ---------------- #

def clean_data_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        for word in WORDS:
            content = re.sub(re.escape(word), f"[KAME{'HAME' * round(int((WORDS.index(word))/7)) + 'HAAAA'}]", content, flags=re.IGNORECASE)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    except Exception as err:
        print(f"Error cleaning {file_path}: {err}")


def process_zip(zip_path, password, out_folder):
    filename = os.path.basename(zip_path)
    update_status(f"Extracting: {filename}")

    passw = password.encode() if password else None
    extract_path = os.path.join(TEMP_F, os.path.splitext(filename)[0])
    os.makedirs(extract_path, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(extract_path, pwd=passw)
    except RuntimeError:
        update_status(f"Wrong password: {filename}")
        return False
    except Exception as e:
        update_status(f"Error extracting: {filename}")
        print(e)
        return False

    update_status(f"Cleaning: {filename}")

    for root_dir, _, files in os.walk(extract_path):
        for file in files:
            if file == "data":
                file_path = os.path.join(root_dir, file)
                clean_data_file(file_path)

    update_status(f"Rezipping: {filename}")

    out_zip = os.path.join(
        out_folder, os.path.splitext(filename)[0] + "_cleaned.zip"
    )

    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as new_zip:
        for root_dir, _, files in os.walk(extract_path):
            for file in files:
                file_path = os.path.join(root_dir, file)
                arcname = os.path.relpath(file_path, extract_path)
                new_zip.write(file_path, arcname)

    return True


def clean_all_zips(folder, password):
    zips = [f for f in os.listdir(folder) if f.endswith(".zip")]

    if not zips:
        update_status("No zip files found in folder.")
        return

    # Build dated output subfolder
    folder_name = os.path.basename(folder)
    date_str = datetime.datetime.now().strftime("%d-%m-%Y")
    subfolder_name = f"{folder_name}_cleaned@{date_str}"
    out_folder = os.path.join(OUT_F, subfolder_name)
    os.makedirs(out_folder, exist_ok=True)

    succeeded = []
    failed = []

    for i, file in enumerate(zips, 1):
        update_status(f"Processing {i}/{len(zips)}: {file}")
        ok = process_zip(os.path.join(folder, file), password, out_folder)
        if ok:
            succeeded.append(file)
        else:
            failed.append(file)

    # Build popup message
    msg = f"Cleaned: {len(succeeded)} / {len(zips)} zip(s)\n"
    msg += f"Saved to: output_cleaned/{subfolder_name}/\n"

    if failed:
        msg += f"\nFailed ({len(failed)}):\n"
        msg += "\n".join(f"  - {f}" for f in failed)

    update_status(f"Done. {len(succeeded)} cleaned, {len(failed)} failed.")
    root.after(0, lambda: messagebox.showinfo("Done!", msg))


# ---------------- UI HELPERS ---------------- #

def update_status(text):
    root.after(0, lambda: status_label.config(text=text))


# ---------------- UI ---------------- #

folder_path = ""

def select_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_label.config(text=f"Selected: {folder_path}")


def start_cleaning():
    password = password_entry.get()

    if not folder_path:
        status_label.config(text="Please select a folder first.")
        return

    btn_clean.config(state="disabled")
    btn_select.config(state="disabled")
    status_label.config(text="Starting...")

    def run():
        clean_all_zips(folder_path, password)
        root.after(0, lambda: btn_clean.config(state="normal"))
        root.after(0, lambda: btn_select.config(state="normal"))

    threading.Thread(target=run, daemon=True).start()


# Create window
root = tk.Tk()
root.title("Zip Cleaner")
root.geometry("500x300")

btn_select = tk.Button(root, text="Input Zips Folder", command=select_folder)
btn_select.pack(pady=10)

folder_label = tk.Label(root, text="No folder selected")
folder_label.pack()

tk.Label(root, text="Enter Password (leave empty if none):").pack()
password_entry = tk.Entry(root, show="*")#🗿
password_entry.pack(pady=5) 

btn_clean = tk.Button(root, text="Clean", command=start_cleaning)
btn_clean.pack(pady=10)

status_label = tk.Label(root, text="Status: Waiting")
status_label.pack(pady=10)

root.mainloop()