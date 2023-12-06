import os
import sys
import shutil
import datetime
import pickle

# Load the existing lists from files
with open("Capitalization_Dict.pickle", "rb") as f:
    Capitalization_Dict = pickle.load(f)
with open("quoted_stat.pickle", "rb") as f:
    quoted_stat = pickle.load(f)
with open("Partial_Quotation.pickle", "rb") as f:
    Partial_Quotation = pickle.load(f)
with open("Partial_Correction.pickle", "rb") as f:
    Partial_Correction = pickle.load(f)
with open('ModID_Dict.pickle', 'rb') as f:
    ModID_Dict = pickle.load(f)
with open('PercentageList.pickle', 'rb') as f:
    PercentageList = pickle.load(f)
with open('lessismore.pickle', 'rb') as f:
    lessismore = pickle.load(f)
with open('PercentageinStats.pickle', 'rb') as f:
    PercentageinStats = pickle.load(f)
with open('ignore_list.pickle', 'rb') as f:
    ignore_list = pickle.load(f)
with open('Base256.pickle', 'rb') as f:
    Base256 = pickle.load(f)
with open('Enhanced_Tooltip.pickle', 'rb') as f:
    Enhanced_Tooltip = pickle.load(f)

'''
--- DAT_Process Dictionaries ---
Capitalization_Dict
Partial_Correction
quoted_stat
Partial_Quotation
Enhanced_Tooltip

--- SQL_Process Dictionaries ---
ModID_Dict
PercentageList
lessismore
PercentageinStats
ignore_list
Base256

'''

def modify_list(existing_list, new_stat):
    existing_list.append(new_stat)

def Modify_Key_Pair(existing_dict, new_key, new_value):
    existing_dict[new_key] = new_value

stats_added = ''
desired_list = ''
new_stat_quoted_stat = None
new_stat_Partial_Quotation = None

while True:
    while True:
        stat_name = input("Enter the stat name: ")
        Check_stat_name = stat_name.lower().replace(' ', '').replace('"', '')
        if not Check_stat_name.isalpha():
            print("Invalid input. Please enter only letters.")
        elif Check_stat_name in Capitalization_Dict:
            print( stat_name + " already exists")
        else:
            break

    while True:
        mod_id = input("Enter the ModID. If N/A, put 0: ")
        if not mod_id.isdigit():
            print("Invalid input. Please enter only numbers.")
        elif int(mod_id) in ModID_Dict.values():
                print(mod_id + " already exists")
        else:
            break

    while True:
        answer = input("DAT: Does this tooltip contain partially quoted text? (y/n/exit) ")
        if answer.lower() == "y":
            ispartialquoted = True
            break
        elif answer.lower() == "n":
            ispartialquoted = False
            break
        elif answer.lower() == "exit":
            print("Exiting the script.")
            sys.exit()
        else:
            print("Invalid input. Please enter 'y' or 'n', or 'exit'.")

    while True:
        answer = input("DAT: Do you want the tooltip to read : Enhances " + stat_name + " effect? (y/n/exit) ")
        if answer.lower() == "y":
            isenhanced = True
            break
        elif answer.lower() == "n":
            isenhanced = False
            break
        elif answer.lower() == "exit":
            print("Exiting the script.")
            sys.exit()
        else:
            print("Invalid input. Please enter 'y' or 'n', or 'exit'.")

        '''while True:
        answer = input("Does this stat have a ModID associated with it? (y/n/exit) ")
        if answer.lower() == "y":
            sqlinclude = True
            break
        elif answer.lower() == "n":
            sqlinclude = False
            break
        elif answer.lower() == "exit":
            print("Exiting the script.")
            sys.exit()
        else:
            print("Invalid input. Please enter 'y' or 'n', or 'exit'.")'''

    if mod_id == 0:
        sqlinclude = False
    else:
        sqlinclude = True

    if sqlinclude == True:
        while True:
            answer = input("SQL: Is the value percentage based? Ex. Damage Taken -10% would be 1000. (y/n/exit) ")
            if answer.lower() == "y":
                is1000base = True
                break
            elif answer.lower() == "n":
                is1000base = False
                break
            elif answer.lower() == "exit":
                print("Exiting the script.")
                sys.exit()
            else:
                print("Invalid input. Please enter 'y' or 'n', or 'exit'.")

        while True:
            answer = input("SQL: Is the value 256 based? This is very rare. (y/n/exit) ")
            if answer.lower() == "y":
                is256base = True
                break
            elif answer.lower() == "n":
                is256base = False
                break
            elif answer.lower() == "exit":
                print("Exiting the script.")
                sys.exit()
            else:
                print("Invalid input. Please enter 'y' or 'n', or 'exit'.")

        while True:
            answer = input("SQL: Is the tooltip inverted from the SQL value? (y/n/exit) ")
            if answer.lower() == "y":
                islessismore = True
                break
            elif answer.lower() == "n":
                islessismore = False
                break
            elif answer.lower() == "exit":
                print("Exiting the script.")
                sys.exit()
            else:
                print("Invalid input. Please enter 'y' or 'n', or 'exit'.")

        while True:
            answer = input("SQL: Is the ModID depend on a %? Ex. HP vs HP% (y/n/exit) ")
            if answer.lower() == "y":
                ispercentinstat = True
                break
            elif answer.lower() == "n":
                ispercentinstat = False
                break
            elif answer.lower() == "exit":
                print("Exiting the script.")
                sys.exit()
            else:
                print("Invalid input. Please enter 'y' or 'n', or 'exit'.")

        while True:
            answer = input("Please confirm that this is correct:\n" + stat_name + "\n" + mod_id + "\n(y/n/exit) ")
            if answer.lower() == "y":
                break
            elif answer.lower() == "n":
                print("Exiting the script.")
                sys.exit()
            elif answer.lower() == "exit":
                print("Exiting the script.")
                sys.exit()
            else:
                print("Invalid input. Please enter 'y' or 'n', or 'exit'.")




                # ---   DAT Data Manipulation   ---

    # ---   Capitalization_Dict
    Key_Capitalization_Dict = stat_name.lower().replace(' ', '').replace('"', '')
    Value_Capitalization_Dict = stat_name.replace('"', '')
    Modify_Key_Pair(Capitalization_Dict, Key_Capitalization_Dict, Value_Capitalization_Dict)

    # ---   Partial_Quotation
    if ispartialquoted == True:
        new_stat_Partial_Quotation = stat_name.replace('"', '')
        Key_Partial_Correction = stat_name.replace('"', '')
        Value_Partial_Correction =  stat_name.replace('"', '\\"')
        modify_list(Partial_Quotation, new_stat_Partial_Quotation)
        Modify_Key_Pair(Partial_Correction, Key_Partial_Correction, Value_Partial_Correction)

    # ---   quoted_stat
    if stat_name.startswith('"') and stat_name.endswith('"'):
        new_stat_quoted_stat = stat_name.replace('"', '')
        modify_list(quoted_stat, new_stat_quoted_stat)

    # ---   enhanced_tooltip
    if isenhanced == True:
        modify_list(Enhanced_Tooltip, stat_name.replace('"', ''))

                # ---   SQL Data Manipulation   ---
    SQL_stat_name = stat_name.lower().replace(' ', '').replace('"', '')
    if sqlinclude == True:
        # ---   ModID_Dict
        value_modid = int(mod_id)
        Modify_Key_Pair(ModID_Dict, SQL_stat_name, value_modid)

        # ---   PercentageList
        if is1000base == True:
            modify_list(PercentageList, SQL_stat_name)

        # ---   lessismore
        if islessismore == True:
            modify_list(lessismore, SQL_stat_name)

        # ---   PercentageinStats
        if ispercentinstat == True:
            SQL_percent_stat_name = SQL_stat_name + '%'
            modify_list(PercentageinStats, SQL_percent_stat_name)

        # ---   Base256
        if is256base == True:
            modify_list(Base256, SQL_stat_name)

        # ---   ignore_list
    if sqlinclude == False:
        modify_list(ignore_list, SQL_stat_name)

    stats_added += stat_name + ': ' + mod_id + '\n'
    desired_list += "'" + stat_name.replace('"', '') + "',\n"

    answer = input("Would you like to add another ModID? (y/n)")
    if answer.lower() == "y":
        continue
    elif answer.lower() == "n":
        break
    else:
        print("Invalid input. Please enter 'y' or 'n'.")

        # ---   Backup Process Start    ---
# Create backup folder with date and time
backup_folder = os.path.join("Pickle_Backups", datetime.datetime.now().strftime("%m-%d-%Y_%H-%M"))
os.makedirs(backup_folder)

# Define list of pickle files to backup
pickle_files = ["Capitalization_Dict.pickle", "quoted_stat.pickle",
                "Partial_Quotation.pickle", "Partial_Correction.pickle", "ModID_Dict.pickle",
                "PercentageList.pickle", "lessismore.pickle", "PercentageinStats.pickle",
                "ignore_list.pickle", "Base256.pickle", "Enhanced_Tooltip.pickle"]

# Loop through pickle files and copy them to backup folder
for file in pickle_files:
    source_file = os.path.join(".", file)
    destination_file = os.path.join(backup_folder, file)
    shutil.copyfile(source_file, destination_file)
            # ---   Backup Process End  ---


            # ---   DAT Pickle Dumps    ---
with open("Capitalization_Dict.pickle", "wb") as f:
    pickle.dump(Capitalization_Dict, f)
with open("quoted_stat.pickle", "wb") as f:
    pickle.dump(quoted_stat, f)
with open("Partial_Quotation.pickle", "wb") as f:
    pickle.dump(Partial_Quotation, f)
with open("Partial_Correction.pickle", "wb") as f:
    pickle.dump(Partial_Correction, f)
with open('Enhanced_Tooltip.pickle', 'wb') as f:
    pickle.dump(Enhanced_Tooltip, f)

            # ---   SQL Pickle Dumps    ---
with open('ModID_Dict.pickle', 'wb') as f:
    pickle.dump(ModID_Dict, f)
with open('PercentageList.pickle', 'wb') as f:
    pickle.dump(PercentageList, f)
with open('PercentageList.pickle', 'wb') as f:
    pickle.dump(PercentageList, f)
with open('lessismore.pickle', 'wb') as f:
    pickle.dump(lessismore, f)
with open('PercentageinStats.pickle', 'wb') as f:
    pickle.dump(PercentageinStats, f)
with open('ignore_list.pickle', 'wb') as f:
    pickle.dump(ignore_list, f)

print('The following stats have been added:\n' + stats_added + 'Don\'t forget to add these items into Desired_Order!\n' + desired_list)
