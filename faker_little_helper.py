import random
from faker import Faker

fake = Faker()
DATA = []
fake_gender = '-X-'
fake_name = '-X-'
fake_first_name = '-X-'
fake_last_name = '-X-'
is_gender_column = False
gender_column_position = 0
is_name_column = False
is_first_name_column = False
is_last_name_column = False
is_email_column = False
name_column_position = 0
first_name_column_position = 0
last_name_column_position = 0
email_column_position = 0

# Menu
print('*' * 50)
print('a - name\tb - first name\tc - last name')
print('d- gender\te - email')
print('*' * 50)

providers = {
    'a': '{{name}}',
    'b': '{{first_name}}',
    'c': '{{last_name}}',
    'd': '--gender--',
    'e': '{{email}}',
}

selected_column = "abcde"  # temp - add: input()
row_count = 10  # tmp
# add: cut repeated letters

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
print('raw data: ', DATA)
# raw data generated! so we have list of columns like:
# ['--gender--',  '{{fist_name_male}}', '{{last_name}}'
# check if gender or email or (name and first/last name)
#  mod. DATA if:
#  1. Check if gender col. - (rnd male/female)
#  1a. first_name is affected by gender column
#  email column: use faker.email() if no name/first/last name selected
#  else is composed as:  first_name.last_name@domain_name

# generate and write fake rows
file = open('file.csv', 'w', newline='')
for _ in range(row_count):
    fake_last_name = fake.last_name()
    fake_first_name = fake.first_name()
    fake_name = fake_first_name + " " + fake_last_name
    if is_gender_column:
        fake_gender = random.choice(['male', 'female'])
        DATA = DATA[:gender_column_position] + [fake_gender] + DATA[gender_column_position+1:]
    if (is_name_column or is_first_name_column) and is_gender_column:
        fake_first_name = fake.first_name_male() if fake_gender == 'male' else fake.first_name_female()
        #print(f'{fake_gender}-->{fake_first_name}')
        fake_name = fake_first_name + " " + fake_last_name
    if is_first_name_column and is_gender_column:
        DATA = DATA[:first_name_column_position] + [fake_first_name] + DATA[first_name_column_position+1:]
    if is_name_column and is_gender_column:
        DATA = DATA[:name_column_position] + [fake_name] + DATA[name_column_position+1:]
    if is_last_name_column and is_name_column:
        DATA = DATA[:last_name_column_position] + [fake_last_name] + DATA[last_name_column_position+1:]
        DATA = DATA[:name_column_position] + [fake_name] + DATA[name_column_position+1:]
    if is_first_name_column and is_name_column:
        DATA = DATA[:first_name_column_position] + [fake_first_name] + DATA[first_name_column_position + 1:]
        DATA = DATA[:name_column_position] + [fake_name] + DATA[name_column_position + 1:]
    if is_email_column:
        DATA = DATA[:email_column_position] \
               + [fake_first_name+'.'+fake_last_name+'_'+fake.domain_name()] \
               + DATA[email_column_position+1:]

    row = fake.csv(data_columns=DATA, num_rows=1, include_row_ids=False)
    row = row.replace('_', '@')  # for some reason fake.csv() doesn't display '@' correctly
    print(row, end='')
    file.write(row)
file.close()
