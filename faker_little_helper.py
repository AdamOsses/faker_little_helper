import random
from faker import Faker

fake = Faker()
DATA = []
fake_gender = '-X-'
is_gender_column = False
gender_column_position = 0

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
    print(f'Gender col. index: {gender_column_position}')

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
    if is_gender_column:
        fake_gender = random.choice(['male', 'female'])
        DATA = DATA[:gender_column_position] + [fake_gender] + DATA[gender_column_position+1:]
    row = fake.csv(data_columns=DATA, num_rows=1, include_row_ids=False)
    print(row, end='')
    file.write(row)
file.close()