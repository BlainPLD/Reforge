# Reforge
Scripting that helps modify existing items in FFXI. 

Files needed and not included. 
Package/Armor_10240-16386_Item.json
Package/Weapons_16384-23039_Item.json

I dont include these files since they will depend heavily on the server you are working on. However, the EXEs are included.
We leverage these exes to extract the DATs into a JSON and then after edits, re-upload it to the DATs.
https://github.com/clanofartisans/ShiningFantasia
Use this exe to extact the Japanese and Englist DAT files into a single JSON.
EX:
item2json.exe "C:\Program Files (x86)\PlayOnline\SquareEnix\FINAL FANTASY XI\ROM\0\6.DAT" "C:\Program Files (x86)\PlayOnline\SquareEnix\FINAL FANTASY XI\ROM\118\108.DAT" "C:\FFXI_JSON\Weapons_16384-23039_Item.json"

Required Filename               JP File location  EN File Location
Weapons_16384-23039_Item.json   ROM\0\6.DAT       ROM\118\108.DAT
Armor_10240-16386_Item.json     ROM\0\7.DAT       ROM\118\109.DAT

EXE File requirements
item2json.exe <japanese item dat> <english item dat> <output json>
json2item.exe <input.json> <japanese item dat> <english item dat>

Here is a resource for knowing what DATs are relevent to what we are trying to do. 
https://docs.google.com/spreadsheets/d/e/2PACX-1vQCnOdHlPKCl9w5jZc35ukG6qgbFxQZhK6Slkmz49iJxZ_ithtVTm4c1xWb4NdBRbxd8ddZtuod1e1-/pubhtml
