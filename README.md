# Reforge
Scripting that helps modify existing items in FFXI.  

The Goal:
========================================================
My aim here is to take an item:  
Pixie Earring with an item ID of 13415  
Lets make this into something a bit more interesting.  

13415, STR+5 DEX+5 Accuracy+10 Slow+3%

The above is an example of how to modify an item. All you need is the itemid and what stats you want to put on it.  
Within the "input" folder, you will use the input.csv file. This will hold all the items you want to make changes to.  
There are some restrictions here, but generally this should work. Also, there are stats missing from the lists,  
however there is a system in place to add these missing stats. You will need to know the MODID and how that stat  
works for your private server.  
Ex:  
Slow is not a stat, but a negative form of Haste. Also it is used as a percentage.  
But generally the ADD MODID script should be good enough to get most stats added.  

In the end you will have 2 things done. The DAT files will be edited automatically,  
and you will have a SQL script waiting for you in the "output" folder.  
You will use this to make the edits in your database.  

Additionally, there are some optional changes you can make too.  
13415, STR+5 DEX+5 Accuracy+10 Slow+3%, 65, WAR  

This line will not only change the stats, but also the level required, and the Jobs that can use it.  
These are not required, so feel free to use them as needed.  
Be advised that the postion matters here.  
ITEMID, STATBLOCK, LEVEL, JOBS  

TODO - Add in a function that takes "ALLJOBS" and adds in all jobs for you. Currently, you need to list out every job.  

Please be aware that this is not an APPEND situation. Any stats you include in the tooltip will be the new stats,  
and anything missing will be gone. (with the exception of "Addtional Effects" which I go into later.)  
Ex:  
Pixie Earring   
DEX+3  

Your input file:  
13415, STR+5  

The result will be:  
Pixie Earring  
STR+5  

The Setup:
========================================================
Python 3.11  
We use BATCH files to run through these scripts, move and delete files. 

The default location for FFXI install is:  
C:\Program Files (x86)\PlayOnline\SquareEnix\FINAL FANTASY XI  
If this is different for you, the only place you need to change the path is in the Package\Start.bat  

Files needed and not included.   
Package/Armor_10240-16386_Item.json  
Package/Weapons_16384-23039_Item.json  

I dont include these files since they will depend heavily on the server you are working on. However, the EXEs are included.  
We leverage these exes to extract the DATs into a JSON and then after edits, re-upload it to the DATs.  
https://github.com/clanofartisans/ShiningFantasia  
Use this exe to extact the Japanese and Englist DAT files into a single JSON.  
EX:    
item2json.exe "C:\Program Files (x86)\PlayOnline\SquareEnix\FINAL FANTASY XI\ROM\0\6.DAT" "C:\Program Files (x86)\PlayOnline\SquareEnix\FINAL FANTASY XI\ROM\118\108.DAT" "C:\FFXI_JSON\Weapons_16384-23039_Item.json"  

Output File Name&nbsp;&nbsp;&nbsp;&nbsp;               JP File location&nbsp;&nbsp;&nbsp;&nbsp;  EN File Location&nbsp;&nbsp;&nbsp;&nbsp;  
Weapons_16384-23039_Item.json&nbsp;&nbsp;&nbsp;&nbsp;   ROM\0\6.DAT&nbsp;&nbsp;&nbsp;&nbsp;       ROM\118\108.DAT  
Armor_10240-16386_Item.json&nbsp;&nbsp;&nbsp;&nbsp;     ROM\0\7.DAT&nbsp;&nbsp;&nbsp;&nbsp;       ROM\118\109.DAT  

EXE File requirements  
item2json.exe "japanese item dat" "english item dat" "output json"  
json2item.exe "input.json" "japanese item dat" "english item dat"  

Here is a resource for knowing what DATs are relevent to what we are trying to do.  
https://docs.google.com/spreadsheets/d/e/2PACX-1vQCnOdHlPKCl9w5jZc35ukG6qgbFxQZhK6Slkmz49iJxZ_ithtVTm4c1xWb4NdBRbxd8ddZtuod1e1-/pubhtml

Restrictions:
========================================================
"Convert X HP to MP" and "Convert X MP to HP"  
Convert HP to MP+X  
Convert HP to MP+X  
These both will output the correct formatting, but at first it needs to be in this format.   

In the case of Occasionally Attacks X  
Occasionally attacks twice+1 <- The number here doesnt matter, its just to say its active  
Occasionally attacks thrice+1 <- The number here doesnt matter, its just to say its active  
Occasionally attacks max+X <- This outputs "Occasionally attacks 2 to X times"  

"Additional" Stats  
Ex.    
$Additional effect:  Water damage  
$On Watersdays and Darksdays:  "Regen"+15  
$In sandstorms:  Evasion+15  
$Enchantment:  Pet gains effect of "Meditate"  
$Additional effect vs. vermin:  "Stun"  
$In areas under own nation's control:\\nAccuracy+10 Attack+10 Haste+1%  
$In areas outside own nation's control:\\nConverts 40 MP to HP  

Note that the formatting needs to be correct after the "$". Capitalization, spacing, and " need to be present.   
Also, adding in \\n after about 35-38 characters is needed to make the tooltip formatting correct in the DAT files.   
Very little post processing happens after the $, so be sure that all this information is correct.  

Anything that happens after the $ also needs to to be handled on the server side manually.  

