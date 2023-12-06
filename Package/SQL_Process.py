import csv
import re
import pickle
import math

# We start with loading our lists
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

# Open the input file
with open('SQL_input.csv', 'r') as input_file:

    PetType = {
                'pet:': 0,
                'avatar:': 1,
                'wyvern:': 2,
                'automaton:': 3,
                'harlaquin:': 4,
                'valoredge:': 5,
                'sharpshot:': 6,
                'stormwalker:': 7,
                'luopan:': 8
                }
    superiorlv1 = [
        {'stat': 'hp', 'value': '25'},
        {'stat': 'mp', 'value': '15'},
        {'stat': 'str', 'value': '3'},
        {'stat': 'dex', 'value': '3'},
        {'stat': 'vit', 'value': '3'},
        {'stat': 'agi', 'value': '3'},
        {'stat': 'int', 'value': '3'},
        {'stat': 'mnd', 'value': '3'},
        {'stat': 'chr', 'value': '3'},
        {'stat': 'accuracy', 'value': '5'},
        {'stat': 'ranged accuracy', 'value': '5'},
        {'stat': 'magic accuracy', 'value': '5'},
        {'stat': 'evasion', 'value': '5'},
        {'stat': 'magic evasion', 'value': '3'},
        {'stat': 'magic def. bonus', 'value': '1'},
        {'stat': 'damage taken', 'value': '100'},
        {'stat': 'haste', 'value': '100'},
        ]
    superiorlv2 = [
        {'stat': 'hp', 'value': '50'},
        {'stat': 'mp', 'value': '30'},
        {'stat': 'str', 'value': '5'},
        {'stat': 'dex', 'value': '5'},
        {'stat': 'vit', 'value': '5'},
        {'stat': 'agi', 'value': '5'},
        {'stat': 'int', 'value': '5'},
        {'stat': 'mnd', 'value': '5'},
        {'stat': 'chr', 'value': '5'},
        {'stat': 'accuracy', 'value': '10'},
        {'stat': 'ranged accuracy', 'value': '10'},
        {'stat': 'magic accuracy', 'value': '10'},
        {'stat': 'evasion', 'value': '10'},
        {'stat': 'magic evasion', 'value': '10'},
        {'stat': 'magic def. bonus', 'value': '2'},
        {'stat': 'damage taken', 'value': '200'},
        {'stat': 'haste', 'value': '200'},
        ]
    superiorlv3 = [
        {'stat': 'hp', 'value': '75'},
        {'stat': 'mp', 'value': '45'},
        {'stat': 'str', 'value': '10'},
        {'stat': 'dex', 'value': '10'},
        {'stat': 'vit', 'value': '10'},
        {'stat': 'agi', 'value': '10'},
        {'stat': 'int', 'value': '10'},
        {'stat': 'mnd', 'value': '10'},
        {'stat': 'chr', 'value': '10'},
        {'stat': 'accuracy', 'value': '20'},
        {'stat': 'ranged accuracy', 'value': '20'},
        {'stat': 'magic accuracy', 'value': '20'},
        {'stat': 'evasion', 'value': '20'},
        {'stat': 'magic evasion', 'value': '15'},
        {'stat': 'magic def. bonus', 'value': '5'},
        {'stat': 'damage taken', 'value': '300'},
        {'stat': 'haste', 'value': '300'},
        ]
    superiorlv4 = [
        {'stat': 'hp', 'value': '100'},
        {'stat': 'mp', 'value': '60'},
        {'stat': 'str', 'value': '15'},
        {'stat': 'dex', 'value': '15'},
        {'stat': 'vit', 'value': '15'},
        {'stat': 'agi', 'value': '15'},
        {'stat': 'int', 'value': '15'},
        {'stat': 'mnd', 'value': '15'},
        {'stat': 'chr', 'value': '15'},
        {'stat': 'accuracy', 'value': '25'},
        {'stat': 'ranged accuracy', 'value': '25'},
        {'stat': 'magic accuracy', 'value': '25'},
        {'stat': 'evasion', 'value': '25'},
        {'stat': 'magic evasion', 'value': '25'},
        {'stat': 'magic def. bonus', 'value': '7'},
        {'stat': 'damage taken', 'value': '400'},
        {'stat': 'haste', 'value': '400'},
        ]
    superiorlv5 = [
        {'stat': 'hp', 'value': '125'},
        {'stat': 'mp', 'value': '75'},
        {'stat': 'str', 'value': '20'},
        {'stat': 'dex', 'value': '20'},
        {'stat': 'vit', 'value': '20'},
        {'stat': 'agi', 'value': '20'},
        {'stat': 'int', 'value': '20'},
        {'stat': 'mnd', 'value': '20'},
        {'stat': 'chr', 'value': '20'},
        {'stat': 'accuracy', 'value': '30'},
        {'stat': 'ranged accuracy', 'value': '30'},
        {'stat': 'magic accuracy', 'value': '30'},
        {'stat': 'evasion', 'value': '30'},
        {'stat': 'magic evasion', 'value': '35'},
        {'stat': 'magic def. bonus', 'value': '10'},
        {'stat': 'damage taken', 'value': '500'},
        {'stat': 'haste', 'value': '500'},
        ]
    job_value_dict = {
        "WAR": 1,
        "MNK": 2,
        "WHM": 4,
        "BLM": 8,
        "RDM": 16,
        "THF": 32,
        "PLD": 64,
        "DRK": 128,
        "BST": 256,
        "BRD": 512,
        "RNG": 1024,
        "SAM": 2048,
        "NIN": 4096,
        "DRG": 8192,
        "SMN": 16384,
        "BLU": 32768,
        "COR": 65536,
        "PUP": 131072,
        "DNC": 262144,
        "SCH": 524288
    }

    # ModIDs that are exempt from the SQL scipt that wipes ModIDs for each ItemID that is processed. These are the ModIDs that control Additional effects
    # If we need to change these, they need to be done manually... For now.
    exemptmodids = '431, 499, 500, 501, 950, 951, 952, 953, 1180'

   # Create CSV reader object
    csv_reader = csv.reader(input_file)

    # Initialize variables and set petflag to 9
    prev_item_id = None
    Petflag = 9
    petname = None
    pet_item_id = ''
    pet_query = ''
    player_item_id = ''
    player_query = ''
    item_weapon_query = ''
    level_query = ''
    job_query = ''

    # Iterate over each row in the input CSV file
    for row in csv_reader:
        try:
            # Extract the item ID and data set from each row, along with the optional level data.
            item_id = row[0]
            data_set = row[1]
            if len(row) >= 3:
                level = row[2]
                level = level.strip()
            else:
                level = None
            if len(row) >= 4:
                jobs = row[3]
                jobs = jobs.strip()
            else:
                jobs = None

            # Save this data for reporting later on, if needed.
            raw_data_set = data_set

            data_set = data_set.strip()

            # Resets Petflag if a new item_id is present
            if item_id != prev_item_id:
                Petflag = 9
                SuperiorTag = ""

            prev_item_id = item_id

            # Find and separate Superior tag
            SuperiorCapture = re.search(r'^(.*)(Superior Lv)\s*\.\s*(\d+)', data_set, re.IGNORECASE)
            if SuperiorCapture:
                data_set = SuperiorCapture.group(1)
                SuperiorLabel = SuperiorCapture.group(2)
                SuperiorLevel = SuperiorCapture.group(3)
                SuperiorLabel = SuperiorLabel.lower()
                data_set = data_set.strip()
                SuperiorTag = SuperiorLabel + SuperiorLevel
                SuperiorTag = SuperiorTag.replace(' ', '')
            else:
                SuperiorTag = ""

            # Find and separate Additional Effects
            AdditionalEffectscapture = re.search(r'^(.*?)\s*\$(.*)', data_set)
            if AdditionalEffectscapture:
                data_set = AdditionalEffectscapture.group(1)
                AdditionalEffects = AdditionalEffectscapture.group(2)
                data_set = data_set.strip()
            else:
                AdditionalEffects = ""

            # Cleans up data_set before processing
            data_set = data_set.lower()
            data_set = data_set.replace ('def.','def')
            data_set = data_set.replace ('atk.','atk')
            data_set = data_set.replace('"', '' )
            data_set = data_set.replace('def:', 'def+' )
            data_set = data_set.replace(' ', '')
            data_set = data_set.replace('defence', 'defense')
            data_set = data_set.replace('magicattackbonus', 'magicatkbonus')
            data_set = data_set.replace('magicdefensekbonus', 'magicdefbonus')
            data_set = data_set.replace('affinity:', 'affinity')
            data_set = data_set.replace('dmg:+', 'dmg+')
            data_set = data_set.replace('delay:+', 'hhdelay+')

            # Declaring Valiables
            stat = None
            value = None
            mod_id = None

            PetGroups = "pet:|avatar:|wyvern:|automaton:|harlaquin:|valoredge:|sharpshot:|stormwalker:|luopan:"

            # Parse pet block out for processing ----- PET PARSE START ------
            Petcapture = re.match(fr"^(.*?)(?=\s*(?:{PetGroups})):?\s*(.*)$", data_set)

            pet_data_set = ''
            if Petcapture:
                data_set = Petcapture.group(1)
                pet_data_set = Petcapture.group(2)
                Petcapture = None

                if pet_data_set:
                    petseparation = re.match(fr"({PetGroups})(.*)\s*(.*)$", pet_data_set)

                if petseparation:
                    petname = petseparation.group(1)
                    pet_data_set = petseparation.group(2)
                    petseparation = None
                    pet_data_set = pet_data_set.strip()


                # This is where we parse out the individual stats in the pet block
                pet_data_list = []
                if pet_data_set:
                    # This parses in whole stat (STR+5)
                    for pet_item in re.split(r"(?<=\d|%)(?=[^\d%])", pet_data_set):
                        # This breaks up the stat into the parts we need to process. stat: STR, sign: +, value: 5
                        pet_match = re.match(r"(\D+)(\s*[:\+\-]\s*)(\d*%?)", pet_item)
                        if pet_match:
                            pet_stat, pet_sign, pet_value = pet_match.groups()

                            pet_sign = pet_sign.strip()
                            pet_value = pet_sign + pet_value
                            pet_stat = pet_stat.strip()
                            pet_sign = None
                        else:
                            print(f"Formatting incorrect for pet_data_set: {item_id} {pet_data_set}")
                            import sys
                            sys.exit(1)

                        # We handle edge-cases here.
                        if pet_stat in PercentageList:
                            pet_value = pet_value.rstrip("%")
                            pet_value = pet_value + "00"

                        if pet_stat in lessismore:
                            pet_value = pet_value.replace('-', '')
                            pet_value = pet_value.replace('+', '-')

                        if pet_stat in PercentageinStats:
                            pet_stat = pet_stat + '%'
                            pet_value = pet_value.rstrip("%")

                        if pet_stat == 'slow':
                            pet_stat = 'haste'
                            pet_value = pet_value.replace('+', '-')
                            pet_value = pet_value + '00'

                        if pet_value.endswith('%'):
                            pet_value = pet_value.rstrip("%")

                        if pet_value.startswith('+'):
                            pet_value = pet_value.lstrip('+')

                        if pet_value.startswith(':'):
                            pet_value = pet_value.lstrip(':')

                        # This is where we hold onto all that information for later processing
                        pet_data_list.append({"stat": pet_stat.strip(), "value": pet_value.strip()})

            # We combine superior stats with the stats in the tooltip
            if pet_data_set:
                if SuperiorTag == 'superiorlv1':
                    for superior_stat in superiorlv1:
                        found = False
                        for for_stat in pet_data_list:
                            if for_stat['stat'] == superior_stat['stat']:
                                for_stat['value'] = str(int(for_stat['value']) + int(superior_stat['value']))
                                found = True
                                break
                        if not found:
                            pet_data_list.append(superior_stat)

                if SuperiorTag == 'superiorlv2':
                    for superior_stat in superiorlv2:
                        found = False
                        for stat in pet_data_list:
                            if stat['stat'] == superior_stat['stat']:
                                stat['value'] = str(int(stat['value']) + int(superior_stat['value']))
                                found = True
                                break
                        if not found:
                            pet_data_list.append(superior_stat)

                if SuperiorTag == 'superiorlv3':
                    for superior_stat in superiorlv3:
                        found = False
                        for stat in pet_data_list:
                            if stat['stat'] == superior_stat['stat']:
                                stat['value'] = str(int(stat['value']) + int(superior_stat['value']))
                                found = True
                                break
                        if not found:
                            pet_data_list.append(superior_stat)

                if SuperiorTag == 'superiorlv4':
                    for superior_stat in superiorlv4:
                        found = False
                        for stat in pet_data_list:
                            if stat['stat'] == superior_stat['stat']:
                                stat['value'] = str(int(stat['value']) + int(superior_stat['value']))
                                found = True
                                break
                        if not found:
                            pet_data_list.append(superior_stat)

                if SuperiorTag == 'superiorlv5':
                    for superior_stat in superiorlv5:
                        found = False
                        for stat in pet_data_list:
                            if stat['stat'] == superior_stat['stat']:
                                stat['value'] = str(int(stat['value']) + int(superior_stat['value']))
                                found = True
                                break
                        if not found:
                            pet_data_list.append(superior_stat)

                # We iterate over the list we created earlier to get the ModID we need.
                for item in pet_data_list:
                    stat = item['stat']
                    value = item['value']

                    # We look up the stat in this dictionary to get the correct ModID.
                    # ----- This is where we expect to find KEYERROR exceptions. ------
                    mod_id = ModID_Dict[stat]

                    # We handle an edge-case here for a base 256 value, and we assign petid to the SQL query
                    if 0 <= Petflag <= 8:
                        if stat in Base256:
                            value = int(value)
                            value = int(256) / value
                            value = int(value)

                    elif petname in PetType:
                        if stat in Base256:
                            value = int(value)
                            value = int(256) / value
                            value = int(value)
                            Petflag = PetType[petname]
                            petname = None
                        else:
                            Petflag = PetType[petname]
                            petname = None

                    # We start building the SQL query text here.
                    pet_query += 'INSERT INTO `item_mods_pet` VALUES (' + item_id + ',' + mod_id + ',' + value + ',' + str(Petflag) + ');\n'
                    mod_id = None
                pet_item_id = item_id
                        #  ----- PET PARSE END ------

           # This is where we parse out the individual stats in the stat block
           # ---- Player Parse Starts Here -----
            data_list = []
            data_set = data_set.strip()
            if data_set:
                # This parses in whole stat (STR+5)
                for item in re.split(r"(?<=\d|%)(?=[^\d%])", data_set):
                    # This breaks up the stat into the parts we need to process. stat: STR, sign: +, value: 5
                    match = re.match(r"(\D+)(\s*[:\+\-]\s*)(\d*%?)", item)
                    if match:
                        stat, sign, value = match.groups()

                        sign = sign.strip()
                        value = sign + value
                        stat = stat.strip()
                        sign = None
                    else:
                        print(f"Formatting incorrect for data_set:{item_id} {data_set}.")
                        import sys
                        sys.exit(1)

                    if stat in PercentageList:
                        value = value.rstrip("%")
                        value = value + "00"

                    if stat in lessismore:
                        value = value.replace('-', '')
                        value = value.replace('+', '-')

                    if stat == 'slow':
                        stat = 'haste'
                        value = value.replace('+', '-')
                        value = value + '00'

                    if stat in PercentageinStats:
                        stat = stat + '%'
                        value = value.rstrip("%")

                    if value.endswith('%'):
                        value = value.rstrip("%")

                    if value.startswith('+'):
                        value = value.lstrip('+')

                    if value.startswith(':'):
                        value = value.lstrip(':')

                    data_list.append({"stat": stat.strip(), "value": value.strip()})

            # We combine superior stats with the stats in the tooltip
            if data_set:
                if SuperiorTag == 'superiorlv1':
                    for superior_stat in superiorlv1:
                        found = False
                        for stat in data_list:
                            if stat['stat'] == superior_stat['stat']:
                                stat['value'] = str(int(stat['value']) + int(superior_stat['value']))
                                found = True
                                break
                        if not found:
                            data_list.append(superior_stat)

                if SuperiorTag == 'superiorlv2':
                    for superior_stat in superiorlv2:
                        found = False
                        for stat in data_list:
                            if stat['stat'] == superior_stat['stat']:
                                stat['value'] = str(int(stat['value']) + int(superior_stat['value']))
                                found = True
                                break
                        if not found:
                            data_list.append(superior_stat)

                if SuperiorTag == 'superiorlv3':
                    for superior_stat in superiorlv3:
                        found = False
                        for stat in data_list:
                            if stat['stat'] == superior_stat['stat']:
                                stat['value'] = str(int(stat['value']) + int(superior_stat['value']))
                                found = True
                                break
                        if not found:
                            data_list.append(superior_stat)

                if SuperiorTag == 'superiorlv4':
                    for superior_stat in superiorlv4:
                        found = False
                        for stat in data_list:
                            if stat['stat'] == superior_stat['stat']:
                                stat['value'] = str(int(stat['value']) + int(superior_stat['value']))
                                found = True
                                break
                        if not found:
                            data_list.append(superior_stat)

                if SuperiorTag == 'superiorlv5':
                    for superior_stat in superiorlv5:
                        found = False
                        for stat in data_list:
                            if stat['stat'] == superior_stat['stat']:
                                stat['value'] = str(int(stat['value']) + int(superior_stat['value']))
                                found = True
                                break
                        if not found:
                            data_list.append(superior_stat)

                # We iterate over the list we created earlier to get the ModID we need.
                for item in data_list:
                    stat = item['stat']
                    value = item['value']

                    # We start building the SQL query text here.
                    if stat in ignore_list:
                        if stat == 'dmg':
                            item_weapon_query += 'UPDATE `xidb`.`item_weapon` SET `dmg`=\'' + value + '\', `ilvl_skill`=\'0\', `ilvl_parry`=\'0\', `ilvlmacc`=\'0\' WHERE `itemId`=' + item_id + ';\n'
                        if stat == 'delay':
                            item_weapon_query += 'UPDATE `xidb`.`item_weapon` SET `delay`=\'' + value + '\' WHERE `itemId`=' + item_id + ';\n'
                        elif stat == 'hhdelay':
                            value = int(value) + 480
                            item_weapon_query += 'UPDATE `xidb`.`item_weapon` SET `delay`=\'' + str(value) + '\' WHERE `itemId`=' + item_id + ';\n'

                        continue

                    # We look up the stat in this dictionary to get the correct ModID.
                    # ----- This is where we expect to find KEYERROR exceptions. ------
                    mod_id = ModID_Dict[stat]

                    player_query += 'INSERT INTO `item_mods` VALUES (' + item_id + ',' + mod_id + ',' + value + ');\n'
                    mod_id = None

                if level:
                    level_query += 'UPDATE `xidb`.`item_equipment` SET `level`=\'' + level + '\', `ilevel`=\'0\', `su_level`=\'0\' WHERE `itemId`=' + item_id + ';\n'

                if jobs:
                    jobs = jobs.upper().split()
                    jobs = [job_value_dict[job] for job in jobs]
                    job_value = int(math.fsum(jobs))
                    job_query += 'UPDATE `xidb`.`item_equipment` SET `jobs`=' + str(job_value) + ' WHERE  `itemId`=' + str(item_id) + ';\n'

                player_item_id = item_id


                # ---- Player Parse Ends Here -----

        #When a ModID is not found, the rest of that item is skipped, and the item entry is transferred to "Needs_ModID.csv" dock.
        #ToDo - Find a way to remove the previous
        except KeyError:
            print(item_id, '"' + stat + '" does not exist in ModID_Dict. Placing in Needs_ModID.csv.' )
            with open('Needs_ModID.csv', 'a', newline='') as needs_modid:
                needs_modid.write(item_id + '\t' + raw_data_set + '\tError from SQL Scrip. Stat responsible:' + str(stat) + '\n')
            Petflag = 9
            petname = None
            pet_item_id = ''
            pet_query = ''
            player_item_id = ''
            player_query = ''
            item_weapon_query = ''
            level_query = ''
            job_query = ''

            continue

        with open('item_mod.txt', 'a') as item_mod_file:
            item_mod_file.write('-- Start of ' + str(item_id) + '\n')
            if player_item_id:
                player_item_id = player_item_id.rstrip(', ')
                item_mod_file.write("DELETE FROM `item_mods` WHERE `itemId` IN (" + player_item_id + ") AND `modID` NOT IN (" + exemptmodids + ") AND `modID` <= 1067;\n")
                item_mod_file.write(player_query)
                player_item_id = ''
                player_query = ''
                if item_weapon_query:
                    item_mod_file.write(item_weapon_query)
                    item_weapon_query = ''
                if level_query:
                    item_mod_file.write(level_query)
                    level_query = ''
                if job_query:
                    item_mod_file.write(job_query)
                    job_query = ''
            if pet_item_id:
                pet_item_id = pet_item_id.rstrip(', ')
                item_mod_file.write("DELETE FROM `item_mods_pet` WHERE `itemId` IN (" + pet_item_id + ") AND `modID` NOT IN (" + exemptmodids + ") AND `modID` <= 1067;\n")
                item_mod_file.write(pet_query)
                pet_item_id = ''
                pet_query = ''
            item_mod_file.write('-- End of ' + str(item_id) + '\n\n')

    print("Sorted data has been written to item_mod.txt")