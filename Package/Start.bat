copy /Y ..\input\input.csv DAT_input.csv
copy /Y ..\input\input.csv SQL_input.csv
call python DAT_Process.py
call python SQL_Process.py
del DAT_input.csv
del SQL_input.csv
call ..\Output\Output_Move.bat
json2item.exe Weapons_16384-23039_Item.json "C:\Program Files (x86)\PlayOnline\SquareEnix\FINAL FANTASY XI\ROM\0\6.DAT" "C:\Program Files (x86)\PlayOnline\SquareEnix\FINAL FANTASY XI\ROM\118\108.DAT"
pause
json2item.exe Armor_10240-16386_Item.json "C:\Program Files (x86)\PlayOnline\SquareEnix\FINAL FANTASY XI\ROM\0\7.DAT" "C:\Program Files (x86)\PlayOnline\SquareEnix\FINAL FANTASY XI\ROM\118\109.DAT" 
pause
