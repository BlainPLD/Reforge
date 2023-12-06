import csv
import re
import pickle
import json

#Load lists
with open("Capitalization_Dict.pickle", "rb") as f:
    Capitalization_Dict = pickle.load(f)
with open("quoted_stat.pickle", "rb") as f:
    quoted_stat = pickle.load(f)
with open("Partial_Quotation.pickle", "rb") as f:
    Partial_Quotation = pickle.load(f)
with open("Partial_Correction.pickle", "rb") as f:
    Partial_Correction = pickle.load(f)
with open('Enhanced_Tooltip.pickle', 'rb') as f:
    Enhanced_Tooltip = pickle.load(f)

#Open JSon files for editting later
with open('Armor_10240-16386_Item.json', "r", encoding="utf-8") as file:
    Armor_10240_16386_data = file.read()
with open('Weapons_16384-23039_Item.json', "r", encoding="utf-8") as file:
    Weapons_16384_23039_data = file.read()

armor_data = json.loads(Armor_10240_16386_data)
weapon_data = json.loads(Weapons_16384_23039_data)

# Open the input CSV file in read mode
with open('DAT_input.csv', 'r') as input_file:

    # Create a CSV reader object
    csv_reader = csv.reader(input_file)

    # Iterate over each row in the input CSV file
    for row in csv_reader:

        try:
            # Extract the item ID and data set from each row. Also checks for additional information, including level and job changes.
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

            # We use raw_data_set for reference when handling a VALUETYPE error.
            raw_data_set = data_set

            # Initial Data cleanup
            int_item_id = int(item_id)
            data_set = data_set.strip()
            data_set = data_set.replace('  ', ' ')

            # Find and separate Superior tag
            SuperiorCapture = re.search(r'^(.*)(Superior Lv)\.(\d+)', data_set, re.IGNORECASE)
            if SuperiorCapture:
                data_set = SuperiorCapture.group(1)
                SuperiorLabel = SuperiorCapture.group(2)
                SuperiorLevel = SuperiorCapture.group(3)
                SuperiorLabel = SuperiorLabel.lower()
                SuperiorLabel = SuperiorLabel.replace(' ','')
                data_set = data_set.strip()
            else:
                SuperiorTag = ""

            # Find and separate Additional Effects. We identify additional effects by placing a '$' before it. This is the easiest way Ive found to deal with this.
            AdditionalEffectscapture = re.search(r'^(.*?)\s*\$(.*)', data_set)
            if AdditionalEffectscapture:
                data_set = AdditionalEffectscapture.group(1)
                AdditionalEffects = AdditionalEffectscapture.group(2)
                AdditionalEffects = AdditionalEffects.replace('""', '"')
                AdditionalEffects = AdditionalEffects.replace('$', '')
                AdditionalEffects = AdditionalEffects.lstrip()

                data_set = data_set.strip()
            else:
                AdditionalEffects = ""

            #Attempt at handling AE #1
            #AE_Split = AdditionalEffects.split()
            #CorrectedAE = ""
            #for word in AE_Split:
            #    CorrectedAE += word + ' '
            #    if len(CorrectedAE) - CorrectedAE.rfind('\\\\n') > 32:
            #       CorrectedAE = CorrectedAE + '\\\\n'
            #AdditionalEffects = CorrectedAE

            #Attempt at handling AE #2
            # #if 'set:'.lower() not in AdditionalEffects.lower() and 'effect:'.lower() not in AdditionalEffects.lower():
            #    AdditionalEffects = AdditionalEffects.replace(':', ':\\\\n')
            #if len(AdditionalEffects.replace('\\uEF1', '').replace('\\uEF2', '').replace('\\"', '"')) - AdditionalEffects.rfind('\\\\n') > 35:
            #    print(f"Additional Effect tooltip in {item_id} may need \\\\n retooling.")

            # A bit of cleanup for the Additional Effect text block
            if AdditionalEffects:
                AdditionalEffects = '\\\\n' + AdditionalEffects
                AdditionalEffects = AdditionalEffects.replace(' \\\\n', '\\\\n')
                AdditionalEffects = AdditionalEffects.replace('"', '\\"')

            # Check to see if there may be formatting issues with additional effects text block. *** Newline characters need to be added to Additional Effects manually. ***
            if len(AdditionalEffects.replace('\\uEF1', '').replace('\\uEF2', '').replace('\\"', '"').replace('\\\\n', '')) > 40:
                print(f"Additional Effect tooltip in {item_id} may need \\\\n retooling.")


            # Cleans up data_set before processing
            data_set = data_set.lower()
            data_set = data_set.replace('"', '' )
            data_set = data_set.replace ('def.','def')
            data_set = data_set.replace ('atk.','atk')
            data_set = data_set.replace('def:', 'def+' )
            data_set = data_set.replace('defence', 'defense')
            data_set = data_set.replace(' ', '')
            data_set = data_set.replace('dmg:+', 'hhdmg+')
            data_set = data_set.replace('delay:+', 'hhdelay+')
            data_set = data_set.replace('affinity:', 'affinity')

            # Initially setup variables. Also clears the variables on subsequent itterations.
            pet_data_set = []
            pet_data_list = []
            pet_sorted_data = []
            data_list = []
            sorted_data = []
            petname = ""
            damage = None
            delay = None
            hhdamage = None
            hhdelay = None
            temp_stat = None

            # Define what we should be looking for when looking for pet stats.
            PetGroups = "pet:|avatar:|wyvern:|automaton:|harlaquin:|valoredge:|sharpshot:|stormwalker:|luopan:"

            PetCapitalization = {
                'pet:':'Pet:',
                'avatar:':'Avatar:',
                'wyvern:':'Wyvern:',
                'automaton:':'Automaton:',
                'harlaquin:':'Harlaquin:',
                'valoredge:':'Valoredge:',
                'sharpshot:':'Sharpshot:',
                'stormwalker:':'Stormwalker:',
                'luopan:':'Luopan:',
            }

            # Seperates out the pet section of the stat block using Regular Expression
            Petcapture = re.match(fr"^(.*?)(?=\s*(?:{PetGroups})):?\s*(.*)$", data_set)

            # If we find pet stats, we declare variables, and start iterating over the data to extract each item (Ex. Attack+15) in stat (attack), sign (+), and value (15)
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

                pet_data_list = []
                if pet_data_set:
                    for pet_item in re.split(r"(?<=\d|%)(?=[^\d%])", pet_data_set):
                        pet_match = re.match(r"(\D+)([:\+\-])(\d*%?)", pet_item)
                        if pet_match:
                            pet_stat, pet_sign, pet_value = pet_match.groups()
                            pet_sign = pet_sign.strip()
                            pet_value = pet_sign + pet_value
                            pet_stat = pet_stat.replace(' ', '')
                            pet_sign = None
                        else:
                            print(f"Formatting incorrect for pet_data_set: {item_id} {pet_data_set}")
                            import sys
                            sys.exit(1)

                        # We look up the stat in this dictionary to get the correctly capitalization stat name.
                        # ----- This is where we expect to find KEYERROR exceptions. ------
                        temp_stat = pet_stat
                        pet_stat = Capitalization_Dict[pet_stat]
                        temp_stat = None

                        # We place stat and sign+value into a list. We use this later in the script to place in correct order.
                        pet_data_list.append({"pet_stat": pet_stat.strip(), "pet_value": pet_value.strip()})


            # If we find player stats, we declare variables, and start iterating over the data to extract each item (Ex. Attack+15) in stat (attack), sign (+), and value (15)
            data_list = []
            if data_set:
                for item in re.split(r"(?<=\d|%)(?=[^\d%])", data_set):
                    match = re.match(r"(\D+)([\:\+\-])(\d*%?)", item)
                    if match:
                        stat, sign, rawvalue = match.groups()
                        sign = sign.strip()
                        value = sign + rawvalue
                        stat = stat.replace(' ', '')
                        sign = None
                    else:
                        print(f"Formatting incorrect for data_set:{item_id} {data_set}.")
                        import sys
                        sys.exit(1)

                    # We look up the stat in this dictionary to get the correctly capitalization stat name.
                    # ----- This is where we expect to find KEYERROR exceptions. ------
                    temp_stat = stat
                    stat = Capitalization_Dict[stat]
                    temp_stat = None

                    if stat == "DMG":
                        damage = int(rawvalue)

                    if stat == "Delay":
                        delay = int(rawvalue)

                    # HH stands for Hand to Hand. The value on these items are handled differently because MNK is weird.
                    if stat == "HHDMG":
                        hhdamage = int(rawvalue) + 3

                    if stat == "HHDelay":
                        hhdelay = int(rawvalue) + 240

                    data_list.append({"stat": stat.strip(), "value": value.strip()})

            # Define the desired order of stats in the tooltip
            desired_order = [
                    'DMG',
                    'Delay',
                    'HHDMG',
                    "HHDelay",
                    'DEF',
                    'Test Attack',
                    'HP',
                    'MP',
                    'STR',
                    'DEX',
                    'VIT',
                    'AGI',
                    'INT',
                    'MND',
                    'CHR',
                    "Fire",
                    "Ice",
                    "Wind",
                    "Earth",
                    "Thunder",
                    "Water",
                    "Light",
                    "Dark",
                    'Attack',
                    'Ranged Attack',
                    'Accuracy',
                    'Ranged Accuracy',
                    'Magic Atk. Bonus',
                    'Magic damage',
                    'Magic Accuracy',
                    'Evasion',
                    'Magic Evasion',
                    'Magic Def. Bonus',
                    'Regen',
                    'Refresh',
                    'Damage taken',
                    "Slashing damage taken",
                    "Piercing damage taken",
                    "Impact damage taken",
                    "Hand-to-Hand damage taken",
                    "Physical damage taken",
                    "Magic damage taken",
                    "Breath damage taken",
                    'Haste',
                    'Slow',
                    'Delay',
                    'Ranged Delay',
                    'Snapshot',
                    'Rapid Shot',
                    'Recycle',
                    'Zanshin',
                    'Store TP',
                    'Weaponskill Accuracy',
                    'Weaponskill damage',
                    'Double Attack',
                    'Double Attack damage',
                    'Triple Attack',
                    'Triple Attack damage',
                    'Quad Attack',
                    'Berserk Duration',
                    'Augments SA',
                    'Augments TA',
                    'Critical hit rate',
                    'Critical hit damage',
                    'Enmity',
                    'Counter',
                    'Counterstance',
                    'Chakra',
                    'Focus',
                    'Cure potency',
                    'Cure spellcasting time',
                    'Regen effect duration',
                    'Elemental resistance spells',
                    'Spell interuption rate down',
                    'Conserve MP',
                    'Elemental Celerity',
                    'Enspell damage bonus',
                    'Steal',
                    'Shield Bash',
                    'Weapon Bash',
                    'Phalanx',
                    'Kick Attacks damage',
                    'Meditate duration',
                    'Retaliation damage',
                    'Fast Cast',
                    'Cursna',
                    'Quick Magic',
                    'Magic critical hit rate',
                    'Drain and Aspir potency',
                    'Subtle Blow',
                    'Absorb Duration',
                    'Charm',
                    'Tame Success Rate',
                    'Reward',
                    'Aggressor',
                    'Enfeebling Potency',
                    'All Songs',
                    'Warcry duration',
                    'Maximum Songs',
                    'Song Duration',
                    'Song spellcasting time',
                    'Ninja tool expertise',
                    'Song Recast Delay',
                    'Avatar level',
                    'Avatar Perpetuation Cost',
                    'Blood Pact damage',
                    'Blood Pact ability delay',
                    'Blood Pact recast time II',
                    'Elemental Siphon',
                    'Dual Wield',
                    'Jump TP Bonus',
                    'Movement speed',
                    'Hand-to-Hand skill',
                    'Dagger skill',
                    'Sword skill',
                    'Great Sword skill',
                    "Axe skill",
                    "Great Axe skill",
                    "Scythe skill",
                    "Polearm skill",
                    "Katana skill",
                    "Great Katana skill",
                    "Club skill",
                    "Staff skill",
                    "Archery skill",
                    "Marksmanship skill",
                    "Throw skill",
                    "Guarding skill",
                    "Evasion skill",
                    "Shield skill",
                    "Parrying skill",
                    "Divine magic skill",
                    "Healing magic skill",
                    "Enhancing magic skill",
                    "Enfeebling magic skill",
                    "Elemental magic skill",
                    "Dark magic skill",
                    "Summoning magic skill",
                    "Ninjutsu skill",
                    "Singing skill",
                    "String instrument skill",
                    "Wind instrument skill",
                    "MP Recovered while healing",
                    "HP Recovered while healing",
                    "Fire Affinity",
                    "Ice Affinity",
                    "Wind Affinity",
                    "Earth Affinity",
                    "Thunder Affinity",
                    "Water Affinity",
                    "Light Affinity",
                    "Dark Affinity",
                    "Resist Amnesia",
                    "Resist Bind",
                    "Resist Blind",
                    "Resist Gravity",
                    "Resist Paralyze",
                    "Resist Petrify",
                    "Resist Poison",
                    "Resist Silence",
                    "Resist Sleep",
                    "Resist Slow",
                    "Resist Virus",
                    "Aquan Killer",
                    "Arcana Killer",
                    "Amorph Killer",
                    "Beast Killer",
                    "Bird Killer",
                    "Demon Killer",
                    "Dragon Killer",
                    "Empty Killer",
                    "Humanoid Killer",
                    "Lizard Killer",
                    "Lumorian KIller",
                    "Luminion Killer",
                    "Plantoid Killer",
                    "Undead Killer",
                    "Vermin Killer",
                    'Fishing skill',
                    'Woodworking skill',
                    'Smithing skill',
                    'Goldsmithing skill',
                    'Clothcraft skill',
                    'Leathercraft skill',
                    'Bonecraft skill',
                    'Alchemy skill',
                    'Cooking skill',
                    'Synergy skill',
                    'Riding skill',
                    'Converts HP to MP',
                    'Converts MP to HP',
                    'Skillchain damage',
                    'TP Bonus',
                    'Divine Caress',
                    'Occasionally attacks twice',
                    'Occasionally attacks thrice',
                    'Occasionally attacks 2 to ',
                    'Weapon skill DEX',
                    'Weapon skill STR',
                    'Weapon skill VIT',
                    'Weapon skill AGI',
                    'Weapon skill INT',
                    'Weapon skill MND',
                    'Weapon skill CHR',
                    'Resistance to all status ailments',
                    "Superior Lv",
                ]

            # There are special icons for element resistances on equipment. These two lists help with identifying these stats and converting the written "element" into its icon.
            Elements = [
                'Fire',
                'Ice',
                'Wind',
                'Earth',
                'Thunder',
                'Water',
                'Light',
                'Dark',
            ]
            Elemental_Conversion = {
                'Fire': "\\uEF1F",
                'Ice': "\\uEF20",
                'Wind': "\\uEF21",
                'Earth': "\\uEF22",
                'Thunder': "\\uEF23",
                'Water': "\\uEF24",
                'Light': "\\uEF25",
                'Dark': "\\uEF26",
            }

            # Sort stats according to the desired order
            if data_list:
                sorted_data = sorted(data_list, key=lambda x: desired_order.index(x['stat']) if x['stat'] in desired_order else float('inf') + desired_order.index(x['stat']))
                data_list = None

            # Sort the pet stats according to the desired order
            if pet_data_list:
                pet_sorted_data = sorted(pet_data_list, key=lambda x: desired_order.index(x['pet_stat']) if x['pet_stat'] in desired_order else float('inf') + desired_order.index(x['pet_stat']))
                pet_data_list = None

            # If the equipment has a superior level attacted to it (which we captured earlier), we standardize the text and clean it up
            if SuperiorCapture:
                SuperiorLabel = Capitalization_Dict[SuperiorLabel]
                SuperiorTag = '\\\\n' + SuperiorLabel + '.' + SuperiorLevel

            #Depending if there is Superior and Additional Effect Data, we combine them for proper formatting.
            if SuperiorTag and AdditionalEffects:
                AppendBlock = AdditionalEffects + SuperiorTag
            elif SuperiorTag == "" and AdditionalEffects:
                AppendBlock = AdditionalEffects
            elif AdditionalEffects == "" and SuperiorTag:
                AppendBlock = SuperiorTag
            else:
                AppendBlock = ""

            # Process the sorted list of stats. This generally entails that we put he final touches on tooltip formatting. This is also where we put in newline characters for tooltip formatting.
            # To-do - This section needs heavy revisions to its use of "\\". These used to be used when we wrote these tooltips to a CSV, instead of directly to JSON.
            output_str = ""
            if sorted_data:
                for item in sorted_data:
                    if output_str:
                        len_stat = item['stat']
                        len_value = item['value']
                        if len(output_str.replace('\\uEF1', '').replace('\\uEF2', '').replace('\\"', '"')) + len(len_stat.replace('\\uEF1', '').replace('\\uEF2', '').replace('\\"', '"')) + len(len_value) - output_str.rfind('\\\\n')> 35:
                            output_str += '\\\\n'
                        len_stat = None
                        len_value = None
                    if item['stat'] == 'DEF':
                        DEFValue = str(item['value'])
                        output_str += item['stat'] + DEFValue.replace("+", ":", 1) + ' '
                        DEFValue = None
                    elif item['stat'] == 'HHDMG':
                        output_str += 'DMG:' + item['value'] + ' '
                    elif item['stat'] == 'HHDelay':
                        output_str += 'Delay:' + item['value'] + ' '
                    elif item['stat'] == 'Converts HP to MP':
                        Convert_Value = str(item['value'])
                        output_str += 'Converts' + Convert_Value.replace("+", ' ', 1) + ' HP to MP '
                        Convert_Value = None
                    elif item['stat'] == 'Converts MP to HP':
                        Convert_Value = str(item['value'])
                        output_str += 'Converts' + Convert_Value.replace("+", ' ', 1) + ' MP to HP '
                        Convert_Value = None
                    elif item['stat'] in Enhanced_Tooltip:
                        output_str += 'Enhances' + ' \\"' + item['stat'] + '\\"' + 'affect'
                    elif item['stat'] == 'DMG':
                        DMGValue = str(item['value'])
                        output_str += item['stat'] + DMGValue.replace("+", ":", 1) + ' '
                        DMGValue = None
                    elif item['stat'] in quoted_stat and output_str == "":
                        output_str += ' \\"' + item['stat'] + '\\"' + str(item['value']) + ' '
                    elif item['stat'] in quoted_stat:
                        output_str += '\\"' + item['stat'] + '\\"' + str(item['value']) + ' '
                    elif item['stat'] in Elements:
                        TempStat = item['stat']
                        output_str +=  Elemental_Conversion[TempStat] + str(item['value']) + ' '
                        TempStat = None
                    elif item ['stat'] == 'Superior Lv':
                        if value == '0':
                            output_str += ''
                        else:
                            output_str += '\\''\\n'+ item['stat'] + '.' + str(item['value']) + ' '
                    elif item['stat'] in Partial_Quotation:
                        QuoteVar = item['stat']
                        output_str += Partial_Correction[QuoteVar] + str(item['value']) + ' '
                    elif item['stat'] == 'Occasionally attacks twice':
                        output_str += item['stat']+ ' '
                    elif item['stat'] == 'Occasionally attacks thrice':
                        output_str += item['stat'] + ' '
                    elif item['stat'] == 'Occasionally attacks 2 to ':
                        Tempvalue = str(item['value'])
                        Tempvalue = Tempvalue.strip('+')
                        output_str += item['stat'] + str(item['value']) + 'times '
                        Tempvalue = None
                    else:
                        output_str += item['stat'] + str(item['value']) + ' '

                    if len(output_str.replace('\\uEF1', '').replace('\\uEF2', '').replace('\\"', '"')) - output_str.rfind('\\\\n') > 30:
                        output_str += '\\\\n'

                    if len(output_str.replace('\\uEF1', '').replace('\\uEF2', '').replace('\\"', '"')) - output_str.rfind('\\\\n') > 35:
                        print(f"{item_id} may need \\n retooling.")

                    if output_str.startswith("\\"):
                        output_str = output_str.replace("\\"," \\", 1)

            # Process the sorted list of stats. This generally entails that we put he final touches on tooltip formatting. This is also where we put in newline characters for tooltip formatting.
            # To-do - This section needs heavy revisions to its use of "\\". These used to be needed when we wrote these tooltips to a CSV, instead of directly to JSON.
            pet_output_str = ""
            if pet_sorted_data:
                for pet_item in pet_sorted_data:
                    if pet_output_str:
                        len_pet_stat = pet_item['pet_stat']
                        len_pet_value = pet_item['pet_value']
                        if len(pet_output_str.replace('\\uEF1', '').replace('\\uEF2', '').replace('\\"', '"')) + len(len_pet_stat.replace('\\uEF1', '').replace('\\uEF2', '').replace('\\"', '"')) + len(len_pet_value) - pet_output_str.rfind('\\\\n') > 35:
                            pet_output_str += '\\\\n'
                        len_pet_stat = None
                        len_pet_value = None
                    if pet_item['pet_stat'] == 'DEF':
                        DEFValue = str(pet_item['pet_value'])
                        pet_output_str += pet_item['pet_stat'] + DEFValue.replace("+", ":", 1) + ' '
                        DEFValue = None
                    elif pet_item['pet_stat'] == 'DMG':
                        DMGValue = str(pet_item['pet_value'])
                        pet_output_str += pet_item['pet_stat'] + DMGValue.replace("+", ":", 1) + ' '
                        DMGValue = None
                    elif pet_item['pet_stat'] in quoted_stat and pet_output_str == "":
                        pet_output_str += ' \\"' + pet_item['pet_stat'] + '\\"' + str(pet_item['pet_value']) + ' '
                    elif pet_item['pet_stat'] in quoted_stat:
                        pet_output_str += '\\"' + pet_item['pet_stat'] + '\\"' + str(pet_item['pet_value']) + ' '
                    elif pet_item['pet_stat'] in Elements:
                        TempStat = pet_item['pet_stat']
                        pet_output_str += '\\' + Elemental_Conversion[TempStat] + str(pet_item['pet_value']) + ' '
                        TempStat = None
                    elif pet_item ['pet_stat'] == 'Superior Lv':
                        if pet_value == '0':
                            pet_output_str += ''
                        else:
                            pet_output_str += '\\''\\n'+ pet_item['pet_stat'] + '.' + str(pet_item['pet_value']) + ' '
                    elif pet_item['pet_stat'] in Partial_Quotation:
                        QuoteVar = pet_item['pet_stat']
                        pet_output_str += Partial_Correction[QuoteVar] + str(pet_item['pet_value']) + ' '
                    else:
                        pet_output_str += pet_item['pet_stat'] + str(pet_item['pet_value']) + ' '

                    if len(pet_output_str.replace('\\uEF1', '').replace('\\uEF2', '').replace('\\"', '"')) - pet_output_str.rfind('\\\\n') > 30:
                        pet_output_str += '\\\\n'

                    if len(pet_output_str.replace('\\uEF1', '').replace('\\uEF2', '').replace('\\"', '"')) - pet_output_str.rfind('\\\\n') > 35:
                        print(f"{item_id} may need \\n retooling.")

                    if pet_output_str.startswith("\\"):
                        pet_output_str = pet_output_str.replace("\\"," \\", 1)

            # Open the output CSV file in append mode. This isnt really needed anymore, and its just used for logging what we are doing.
            with open('DAT_output.csv', 'a', newline='') as output_file:
                if output_str == "":
                    petname = PetCapitalization[petname]
                    petname = petname + ' '
                    output_str = item_id + '\t' + petname + pet_output_str + '\n'
                elif petname:
                    petname = PetCapitalization[petname]
                    petname = petname + ' '
                    output_str = item_id + '\t' + output_str + '\\\\n' + petname + pet_output_str + '\n'
                    petname = None
                else:
                    output_str = item_id + '\t' + output_str + '\n'

                if AppendBlock:
                    output_str = output_str.strip('\n') + AppendBlock + '\n'

                # This code cleans up the output strings created above.
                # This section, and both output_str and pet_output_str blocks need heavy revisions. ToDo - revist sections mentioned.
                output_str = output_str.replace('  ', ' ')
                output_str = output_str.replace('\\\\\\n', '\\\\n')
                output_str = output_str.replace(' \\\\n\n', '\n')
                output_str = output_str.replace(' \\\\n\\\\n', '\\\\n')
                output_str = output_str.replace(' \\\\n', '\\\\n')
                output_file.write(output_str)

            # The cleanup here is just me being lazy. When I finally clean up the top sections, most of this cleanup can go away.
            json_output_str = output_str.lstrip(item_id).replace('\t', '').rstrip('\n').replace('\\\\n', '\\n').replace('\\\"','\"').rstrip()

            # Depending on the item_id, we edit the appropriate JSON file.
            if 10240 <= int(item_id) <= 16383:
                for obj in armor_data:
                    if obj["id"] == int(item_id):
                        obj["englishText"][4] =  json_output_str
                        obj["slvl"] = 0
                        obj["ilvl"] = 0
                        if level:
                            obj["level"] = int(level)
                        if jobs:
                            job_list = jobs.upper().split()
                            obj["jobs"] = job_list
                        break

            elif 16384 <= int(item_id) <= 23037:
                for obj in weapon_data:
                    if obj["id"] == int(item_id):
                        obj["englishText"][4] = json_output_str
                        obj["slvl"] = 0
                        obj["ilvl"] = 0
                        if level:
                            obj["level"] = int(level)
                        if jobs:
                            job_list = jobs.upper().split()
                            obj["jobs"] = job_list
                        if damage:
                            obj["dmg"] = damage
                            obj["delay"] = delay
                            dps = int(((damage * 60) / delay) * 100)
                            damage = None
                            delay = None
                            obj["dps"] = dps
                        if hhdamage:
                            obj["dmg"] = hhdamage
                            obj["delay"] = hhdelay
                            dps = int(((hhdamage * 60) / hhdelay) * 100)
                            hhdamage = None
                            hhdelay = None
                            obj["dps"] = dps
                        break

            else:
                print(item_id + " needs to go into a different file.")
                with open('Needs_ModID.csv', 'a', newline='') as needs_modid:
                    needs_modid.write(item_id + '\t' + raw_data_set + '\tError from DAT Script: item_id out of range.\n')
            sorted_data = None
            pet_sorted_data = None

        # This is where we are handling the KEYERROR that we expect from a stat we havent setup yet. We notate the equipment item_id and stat block, and write it to a csv file. We also clear a couple of variables.
        except KeyError:
            print(item_id, '"' + temp_stat + '" does not exist in Capitalization_Dict. Placing in Needs_ModID.csv.' )
            with open('Needs_ModID.csv', 'a', newline='') as needs_modid:
                needs_modid.write(item_id + '\t' + raw_data_set + '\tError from DAT Script. Stat responsible: ' + temp_stat + '\n')
            temp_stat = None
            sorted_data = None
            pet_sorted_data = None
            continue

    # After we are done iterating over all the items we have to create/edit, we dump the held version we were edting back into the .json file.
    modified_armor_data = json.dumps(armor_data, indent=4, ensure_ascii=False)
    modified_weapon_data = json.dumps(weapon_data, indent=4, ensure_ascii=False)

    with open('Armor_10240-16386_Item.json', "w", encoding="utf-8") as file:
        file.write(modified_armor_data)

    with open("Weapons_16384-23039_Item.json", "w", encoding="utf-8") as file:
        file.write(modified_weapon_data)

    print("Sorted data has been written to output.csv")