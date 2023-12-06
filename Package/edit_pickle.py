import os
import sys
import pickle


'''
=== This is not the tool you should be using to add new MODIDs. Use "Add ModIDs" in the Reforge folder for that. ===

This tool is used to edit the shared pickle lists that the two main scripts use.
Use this tool when you have made incorrect entries or small typos.

--- DAT_Process Dictionaries ---
Capitalization_Dict
Partial_Correction
desired_order
quoted_stat
Partial_Quotation


--- SQL_Process Dictionaries ---
ModID_Dict
PercentageList
lessismore
PercentageinStats
ignore_list
Base256
'''

export_lists = [
    'Capitalization_Dict',
    'Partial_Correction',
    'quoted_stat',
    'Partial_Quotation',
    'ModID_Dict',
    'PercentageList',
    'lessismore',
    'PercentageinStats',
    'ignore_list',
    'Base256',
    ]

textfile = 'pickle_lists.py'

for dict in export_lists:
    picklefile = dict + '.pickle'

    Key_value =[
        'Capitalization_Dict',
        'Partial_Correction',
        'ModID_Dict',
        ]

    lists = [
        'desired_order',
        'quoted_stat',
        'Partial_Quotation',
        'Base256',
        'PercentageList',
        'lessismore',
        'PercentageinStats',
        'ignore_list',
        'Base256',
        'Enhanced_Tooltip',
        ]

    # Load the pickle file
    with open(picklefile, 'rb') as f:
        picklelist = pickle.load(f)
    if dict in Key_value:
        with open(textfile, 'a') as f:
            f.write(dict +" = {" + '\n')
            for key, value in picklelist.items():
                f.write("'" + str(key) + "': '" + str(value) + "'," + '\n')
            f.write('}\n\n')

    if dict in lists:
        with open(textfile, 'a') as f:
            f.write(dict +" = [" + '\n')
            for item in picklelist:
                f.write("'" + str(item) + "'," + '\n')
            f.write(']\n\n')


print('\n\nExported PICKLE lists to Reforge\Package\pickle_lists.py.\nPlease open this file, make your edits, and save.\nNote: You can only make changes to these lists while this program is active.\n')
while True:
    import_ready = input('Are you ready to import your list changes? Enter \'Yes\' to import. Enter \'Exit\' to exit without saving changes: ')
    if import_ready.lower() == 'yes':
        import pickle_lists as pl
        for list in export_lists:
            lists_to_import = getattr(pl, list)
            with open(list + '.pickle', 'wb') as f:
                pickle.dump(lists_to_import, f)
        with open(textfile, 'w') as deleteme:
            deleteme.truncate(0)
        break
    elif import_ready.lower() == 'exit':
        with open(textfile, 'w') as deleteme:
            deleteme.truncate(0)
        sys.exit()
    else:
        print('Invalid input.')
