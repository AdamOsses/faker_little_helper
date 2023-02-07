import random
import os
import sys
import readline
from faker import Faker                     # pip install faker
from pathvalidate import sanitize_filename  # pip install pathvalidate

fake = Faker()
DATA = []
fake_gender = '-X-'
fake_name = '-X-'
fake_first_name = '-X-'
fake_last_name = '-X-'
selected_column = ''
row_count = 0
locale = []  # ['en', 'pl_PL' ...]
files = []  # .csv
selected_column_raw = ''
columns_data = ''
text = ''
providers = {
    'a': '{{name}}',
    'b': '{{first_name}}',
    'c': '{{last_name}}',
    'd': '{{gender}}',
    'e': '{{email}}',       # a-e can't touch this
    'f': '{{password}}',
    'g': '{{country}}',
    'h': '{{city}}',
    'i': '{{street_address}}',
    'j': '{{job}}',
    'k': '{{company}}',
    'l': '{{company_email}}',
    'm': '{{domain_name}}',
    'n': '{{phone_number}}',
    #    '': '{{}}',
}  # {{iban}} {{credit_card_number}} {{credit_card_provider}} {{currency}} ...
providers_char = ''.join(key for key in providers)


def txt_input(prompt, prefill=''):
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()


def remove_doubles_and_unused_chars(col):
    sel_col = ''
    for c in col:
        if c not in sel_col and c in providers_char:
            sel_col += c
    return sel_col


def set_data(sel_col):
    d = []
    for column in sel_col:
        d.append(providers.get(column, ''))
    return d


# -- Menu -- prints all providers
os.system('clear')
print('*' * 100)
print('\t\t\t\t\t"FAKER LITTLE HELPER"')
print('*' * 100)
for i in range(97, len(providers)+97):
    print(f'{chr(i)} - {providers[chr(i)][2:-2]}', end='\t')
    if not (i % 6):
        print('')
print('')
print('*' * 100)
print('Set columns you want using above letters. FLH write 20 rows fake datas to "file.csv"')
print('Default filename: "file.csv", default rows count: 20, default locale: en')
print('Use [] to change default values: \n'
      '   [cz_CZ 100 "my_file.csv"]acj - write 100 data rows to my_file.csv, locale: Czech, columns: acj\n'
      '   [10 "file1.csv" "file2.csv"]mgah - write 10 data rows to file1.csv and file2.csv, columns: mgah')
print('*' * 100)

# User input data
while True:
    text = txt_input("Input data: ", text)
    if len(text) == 0 or text[-1] == 'X':
        sys.exit("Thank you for using faker little helper.")
    elif text == selected_column_raw:
        if len(selected_column) == 0:
            sys.exit("No columns selected.\nThank you for using faker little helper.")
        break
    row_count = 0
    locale = []
    files = []
    selected_column_raw = text
    columns_data = text
    bracket_l_pos = selected_column_raw.find('[')
    bracket_r_pos = selected_column_raw.find(']')
    # read data in brackets [] - row count; locales (cz_CZ, en...); filename
    if bracket_r_pos > bracket_l_pos:
        bracket_data = selected_column_raw[bracket_l_pos+1:bracket_r_pos]
        columns_data = selected_column_raw[:bracket_l_pos] + selected_column_raw[bracket_r_pos+1:]
        print(f'-text->{text}<-')
        print(f'-selected_column_raw:->{selected_column_raw}<-')
        print(f'-bracket_data->{bracket_data}<-')
        print(f'-columns_data->{columns_data}<-')
        filename_pos = [i for i, c in enumerate(bracket_data) if c == '"']  # files in ""
        print(f'filename pos->{filename_pos}<-')
        if len(filename_pos) % 2 != 0:      # " should be even
            print('Sth. wrong with " in []')
        elif len(filename_pos) > 0:
            # & check if proper .csv names
            files_count = int(len(filename_pos)/2)
            tmp_bracket_data = bracket_data[:]
            for i in range(0, files_count*2, 2):
                file = tmp_bracket_data[filename_pos[i]+1:filename_pos[i+1]]  # slice off file name from bracket data
                print(f'file->{file}<-')
                bracket_data = bracket_data.replace('"' + file + '"', "")  # remove "filename" from bracket data
                print(f'bracket data after replace filename->{bracket_data}<-')
                if file[-4:] == '.csv': #  "sdfsdf.csv sgsgsg.csv"
                    # sanitize filename: https://pathvalidate.readthedocs.io/en/latest/pages/examples/sanitize.html
                    file = sanitize_filename(file)
                    files.append(file)
            print(f"-files->{files}<- bracket_data->{bracket_data}<-")  # filename is between every two "
        # locales(en cz_Cz ...) and row count
        elem = bracket_data.split(' ')
        print(f'bracket_data->{bracket_data}<-')
        print(f'elem->{elem}<-')
        for e in elem:
            if e.isdigit():
                row_count += int(e)
            elif len(e) < 2:
                continue
            else:
                try:
                    Faker(e)
                except AttributeError:
                    print(f'Locale issue: {e} - check: https://faker.readthedocs.io/en/master/locales.html')
                else:
                    if e not in locale:
                        locale.append(e)
    # if empty set default locale (en), row_count (20) and filename (file.csv)
    if len(locale) == 0:
        locale.append('en')
    if row_count == 0:
        row_count = 20
    if len(files) == 0:
        files.append("file.csv")
    # cleaning columns and data in brackets
    selected_column = remove_doubles_and_unused_chars(columns_data)
    DATA = set_data(selected_column)
    bracket_data = ''
    for file in files:
        bracket_data += ' "' + file + '"'
    bracket_data += ' ' + str(row_count)
    for loc in locale:
        bracket_data += ' ' + loc
    if len(bracket_data) > 0:
        bracket_data = '[' + bracket_data + ']'
        bracket_data = bracket_data.replace('[ ', '[')
    text = bracket_data + selected_column
    selected_column_raw = text

    print(f'\n*** File(s)  : {files if len(files)>0 else "file.csv"}')
    print(f'*** Rows     : {row_count if row_count>0 else "20"}')
    print(f'*** Locale(s): {locale if len(locale)>0 else "en"}')
    print(f'*** Column(s): {selected_column}')
    d = ' '.join(DATA)
    print(f'*** Column(s): {d}')
    print(f'\nPress ENTER to start or change input.\n')

# generate and write fake rows
fake = Faker(locale)
column_names = (('"' + '","'.join(DATA) + '"').replace('{{', '')).replace('}}', '')
for current_file in files:
    file = open(current_file, 'w', newline='')    # add list of files
    print(column_names)
    file.write(column_names + '\n')
    for _ in range(row_count):
        # fake: name, last_name, first_name, gender and email are depend on each other:
        fake_last_name = fake.last_name()
        fake_first_name = fake.first_name()
        fake_name = fake_first_name + " " + fake_last_name
        if 'c' in selected_column:
            DATA[selected_column.index('c')] = fake_last_name
        if 'd' in selected_column:
            fake_gender = random.choice(['male', 'female'])
            DATA[selected_column.index('d')] = fake_gender
            fake_first_name = fake.first_name_male() if fake_gender == 'male' else fake.first_name_female()
            fake_name = fake_first_name + " " + fake_last_name
        if 'a' in selected_column:
            DATA[selected_column.index('a')] = fake_name
        if 'b' in selected_column:
            DATA[selected_column.index('b')] = fake_first_name
        if 'e' in selected_column:
            email_str = fake_first_name+'.'+fake_last_name+'_'+fake.domain_name()
            email_str = email_str.lower()
            DATA[selected_column.index('e')] = email_str

        row = fake.csv(data_columns=DATA, num_rows=1, include_row_ids=False)
        row = row.replace('_', '@')  # for some reason fake.csv() doesn't display '@' correctly
        print(row, end='')
        file.write(row)
    file.close()
print("Thank you for using faker little helper.")
