4a:
    • Created fuzz.py for py_parser.py
        ◦ Learned how to fuzz methods which helps to identify weaknesses in code for more robust, secure code by generating many random, corrupt inputs which could be exploited by the wrong users.
    • Fuzzes methods:
        ◦ 
	  py_parser.getPythonParseObject,
        py_parser.commonAttribCallBody,
        py_parser.getFunctionAssignments,
        py_parser.getPythonAtrributeFuncs,
        py_parser.getFunctionDefinitions 
    • Fuzz data saved under file 4a_fuzz_report.txt

4b:
    • Added Logging to py_parser.py
        ◦ Learned to use logging to add forensics which can help trace or observe a programs functionality which adds security and can even make it easier to debug.
    • Log data saved under fame_ml_foresensics.log
4c:
    • Added Github action to automatically run fuzz.py and py_parser.py which automatically outputs the fuzz report and the logging results which helps to ensure security whenever a new change is made to the repo. This ensures a secure software development process by automating security.

Location of github action: 
.github/workflows/main.yml
