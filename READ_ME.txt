PyLogFinder.py 
© 2017 Amosu Adewale, Hamdi Mahmood

•	PyLogFinder is a python program for automating the process of analyzing a large database of LAS files and selecting the LAS files that contain specific geophysical logs needed. PyLogFinder uses a mnemonic database of 2665 common mnemonics in searching the LAS file database. The mnemonic database can be easily edited and expanded by the user. 
•	It is written in Python 2.7.3
•	Make sure “PyLogFinder.py” is the same directory with the folder containing LAS files and the excel spreadsheet “Database.xls’
•	Usage (Type this in Terminal): 
python PyLogFinder.py Foldername_containing_LAS_files, List_of_Mnemonics_separated_by_commas

•	For example: python 
PyLogFinder.py TEST_DATA,DT,DTS,GR,LLD,PE

•	See 'Database.xls' for full list of Mnemonics or to add new Mnemonics.

