=======================================
  Zip Cleaner v1.5
=======================================

WHAT IT DOES
------------
Scans a folder of password-protected zip files, removes sensitive
customer keywords from the "data" file inside each zip, and saves
cleaned copies to a dated output folder.


HOW TO USE (exe version)
------------------------
1. Double-click tk_testx_xxxx.exe to launch
2. Click "Input Zips Folder" and select the folder containing your zips
3. The app will show how many zip files were found
4. Enter the zip password (leave blank if none)
5. Click "Clean"
6. When done, a popup will confirm how many were cleaned
7. Click "Open Output Folder" to go straight to the results


OUTPUT
------
Cleaned zips are saved to:
  output_cleaned/<your folder name>_cleaned at DD_MM_YYYY/

A log file (log_DD_MM_YYYY.txt) is also saved in the same folder,
listing which files were cleaned successfully and which failed.


HOW TO USE (developer / source version)
----------------------------------------
Requirements: Python 3.7+

1. Create a virtual environment:
     python -m venv venv

2. Activate it:
     Windows:   venv\Scripts\activate
     Mac/Linux: source venv/bin/activate

3. Install dependencies:
     pip install -r requirements.txt

4. Run the script:
     python tk_testx_xxxx.py

5. To rebuild the exe after making changes:
     pyinstaller --onefile --windowed tk_testx_xxxx.py


ADDING OR REMOVING KEYWORDS
-----------------------------
Open tk_testx_xxxx.py and edit the WORDS list near the top of the file.
Each word must be in "quotes" and separated by a comma.
Matching is case-insensitive.


FILES
-----
tk_testx_xxxx.py      — main script
requirements.txt    — Python dependencies
readme.txt          — this file
dist/               — contains the built tk_testx_xxxx.exe
output_cleaned/     — cleaned zips are saved here (created on first run)
temp_extract/       — temporary working folder (created on first run)


NOTES
-----
- All zips in the selected folder are assumed to share the same password
- Only the file named "data" inside each zip is cleaned
- The output zip is not password-protected
- The temp_extract folder is not automatically deleted after each run
=======================================