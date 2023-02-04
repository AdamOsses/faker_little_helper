import random
import os
import sys
import readline
from faker import Faker                     # pip install faker
from pathvalidate import sanitize_filename  # pip install pathvalidate


def txt_input(prompt, prefill=''):
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()


os.system('clear')

fake = Faker()
DATA = []
fake_gender = '-X-'
fake_name = '-X-'
fake_first_name = '-X-'
fake_last_name = '-X-'
is_gender_column = False
is_name_column = False
is_first_name_column = False
is_last_name_column = False
is_email_column = False
gender_column_position = 0
name_column_position = 0
first_name_column_position = 0
last_name_column_position = 0
email_column_position = 0
selected_column = ''


providers = {
    'a': '{{name}}',
    'b': '{{first_name}}',
    'c': '{{last_name}}',
    'd': '--gender--',
    'e': '{{email}}',
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

}  # {{iban}} {{credit_card_number}} {{credit_card_provider}} {{currency}}
providers_char = ''.join(key for key in providers)

# Menu - prints all providers
print('*' * 100)
for i in range(97, len(providers)+97):
    print(f'{chr(i)} - {providers[chr(i)][2:-2]}', end='\t')
    if not (i % 6):
        print('')
print('')
print('*' * 100)
print('Set columns you want using above letters. FLH write 20 rows to file.csv')
print('Default filename: file.csv, default rows count: 20, default locale: en')
print('Use [] to change default values: \n'
      '   [cz_CZ 100 "my_file.csv"]acj - write 100 data rows to my_file.csv, locale: Czech, columns: acj\n'
      '   [10 "file1.csv" "file2.csv"]mgah - write 10 data rows to file1.csv and file2.csv, columns: mgah')
print('*' * 100)

selected_column_raw = '' # selected_column_raw ='["my_file*1.csv" cz_CZ 1 pl_PLx "my_file.csv"]ejklmn'
text = ''
# temp - add: input() - doubles and 'empty' char possible

# read data in brackets [] - row count; locales (cz_CZ, en...); filename
while True:
    text = txt_input("Input data: ", text)
    if text[-1] == 'X':
        sys.exit("Thank you for using faker little helper.")
    elif text == selected_column_raw:
        break
    selected_column_raw = text
    columns_data = text
    row_count = 0
    locale = []  # ['en', 'pl_PL']
    files = []   # .csv
    bracket_l_pos = selected_column_raw.find('[')
    bracket_r_pos = selected_column_raw.find(']')
    if bracket_r_pos > bracket_l_pos:
        bracket_data = selected_column_raw[bracket_l_pos+1:bracket_r_pos]
        columns_data = selected_column_raw[:bracket_l_pos] + selected_column_raw[bracket_r_pos+1:]
        print(f'-bracket_data: {bracket_data}')
        print(f'-selected_column_raw: {selected_column_raw}')
        # file names: in ""
        filename_pos = [i for i, c in enumerate(bracket_data) if c == '"']
        print(f'filename pos: {filename_pos}')
        if len(filename_pos) % 2 != 0:      # " should be even
            print('Sth. wrong with " in []')
        elif len(filename_pos) > 0:
            # & check if proper .csv names
            files_count = int(len(filename_pos)/2)
            tmp_bracket_data = bracket_data[:]
            for i in range(0, files_count+1, 2):
                file = tmp_bracket_data[filename_pos[i]+1:filename_pos[i+1]]  # slice off file name from bracket data
                print(file)
                bracket_data = bracket_data.replace('"' + file + '"', '')  # remove "filename" from bracket data
                if file[-4:] == '.csv': #  "sdfsdf.csv sgsgsg.csv"
                    # sanitize filename: https://pathvalidate.readthedocs.io/en/latest/pages/examples/sanitize.html
                    file = sanitize_filename(file)
                    files.append(file)
            print(f"-{files}-->{bracket_data}<-")  # filename is between every two "

        # locales(en cz_Cz ...) and row count
        elem = bracket_data.split(' ')
        print(elem)
        for e in elem:
            if e.isdigit():
                row_count += int(e)
            else:
                try:
                    Faker(e)
                except AttributeError:
                    print(f'Locale issue: {e} - check: https://faker.readthedocs.io/en/master/locales.html')
                else:
                    locale.append(e)
if len(locale) == 0:
    locale.append('en')     # default locale is en
if row_count == 0:
    row_count = 5

# remove doubles and unused chars
for c in columns_data:
    if c not in selected_column and c in providers_char:
        selected_column += c

#print(f'providers_char: {providers_char}\nselected_column_raw: {columns_data}'
#      f'\nselected_column: {selected_column}')

# columns that affect each other
if 'd' in selected_column:
    is_gender_column = True
    gender_column_position = selected_column.index('d')
if 'a' in selected_column:
    is_name_column = True
    name_column_position = selected_column.index('a')
if 'b' in selected_column:
    is_first_name_column = True
    first_name_column_position = selected_column.index('b')
if 'c' in selected_column:
    is_last_name_column = True
    last_name_column_position = selected_column.index('c')
if 'e' in selected_column:
    is_email_column = True
    email_column_position = selected_column.index('e')

for column in selected_column:
    DATA.append(providers.get(column, ''))

# generate and write fake rows
fake = Faker(locale)
file = open('file.csv', 'w', newline='')    # add list of files
for _ in range(row_count):
    fake_last_name = fake.last_name()
    fake_first_name = fake.first_name()
    fake_name = fake_first_name + " " + fake_last_name
    if is_gender_column:
        fake_gender = random.choice(['male', 'female'])
        DATA = DATA[:gender_column_position] + [fake_gender] + DATA[gender_column_position+1:]
    if (is_name_column or is_first_name_column) and is_gender_column:
        fake_first_name = fake.first_name_male() if fake_gender == 'male' else fake.first_name_female()
        #  print(f'{fake_gender}-->{fake_first_name}')
        fake_name = fake_first_name + " " + fake_last_name
        if is_first_name_column:
            DATA = DATA[:first_name_column_position] + [fake_first_name] \
                   + DATA[first_name_column_position+1:]
    if is_name_column and (is_first_name_column or is_last_name_column or is_email_column or is_gender_column):
        DATA = DATA[:name_column_position] + [fake_name] + DATA[name_column_position + 1:]
    if is_last_name_column and (is_name_column or is_email_column):
        DATA = DATA[:last_name_column_position] + [fake_last_name] + DATA[last_name_column_position + 1:]
    if is_first_name_column and (is_name_column or is_email_column):
        DATA = DATA[:first_name_column_position] + [fake_first_name] + DATA[first_name_column_position + 1:]
    if is_email_column:
        email_str = fake_first_name+'.'+fake_last_name+'_'+fake.domain_name()
        email_str = email_str.lower()
        DATA = DATA[:email_column_position] + [email_str] + DATA[email_column_position+1:]

    row = fake.csv(data_columns=DATA, num_rows=1, include_row_ids=False)
    row = row.replace('_', '@')  # for some reason fake.csv() doesn't display '@' correctly
    print(row, end='')
    file.write(row)
file.close()
