# FAME-ML Forensics and Fuzzing Summary

## 4a: Fuzzing `py_parser.py`
- **Created `fuzz.py` for `py_parser.py`**
  - Learned how to perform fuzz testing to identify hidden bugs and edge cases.  
  - Gained experience generating invalid or unexpected inputs to test code robustness and security.  

- **Methods fuzzed**
  - `py_parser.getPythonParseObject`  
    - Learned how AST parsing works and the importance of handling exceptions.  
  - `py_parser.commonAttribCallBody`  
    - Learned to test nested or chained function calls for edge cases.  
  - `py_parser.getFunctionAssignments`  
    - Learned to extract and verify function assignments for program analysis.  
  - `py_parser.getPythonAtrributeFuncs`  
    - Learned to handle attribute-based function calls and complex attribute chains.  
  - `py_parser.getFunctionDefinitions`  
    - Learned to identify function definitions and handle uncommon patterns.

- **Fuzzing output**
  - Saved under `4a_fuzz_report.txt`

---

## 4b: Adding Logging to `py_parser.py`
- **Implemented detailed logging**
  - Learned to use Python logging to capture key events: parsing, exceptions, function assignments, and feature extraction.  
  - Gained insight into how logging aids debugging, tracing program flow, and enhancing security.  
  - Learned to balance logging levels: `DEBUG` for details, `INFO`/`WARNING` for higher-level events.

- **Log output**
  - Saved under `fame_ml_forensics.log`

---

## 4c: Continuous Integration with GitHub Actions
- **Added GitHub Action**
  - Learned to automate testing workflows using GitHub Actions.  
  - Gained experience in running scripts automatically, capturing outputs, and ensuring reproducible security checks.  
  - Learned how automation improves software security by detecting issues immediately and providing audit-ready logs and reports.

- **Location of GitHub Action**
  - `.github/workflows/main.yml`
