from faker import Faker

fake = Faker()
DATA = []
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
selected_column = "abcde"  # temp
# add: cut repeated letters
for c in selected_column:
    DATA.append(providers.get(c, ''))
print('raw data: ', DATA)
# raw data generated! so we have list of columns like:
# ['--gender--',  '{{fist_name_male}}', '{{last_name}}'

# check if gender or email or (name and first/last name)
#  mod. DATA if:
#  1. Check if gender col. - (rnd male/female)
#  1a. first_name is affected by gender column
#  email column: use faker.email() if no name/first/last name selected
#  else is composed as:  first_name.last_name@domain_name

# generate fake row
row = fake.csv(data_columns=DATA, num_rows=1, include_row_ids=False)
print(row)

# write row to csv
with open('file.csv', 'w', newline='') as file:
    file.write(row)
