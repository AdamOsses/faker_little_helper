#### Faker is a Python package that generates fake data.   
#### GitHub project: https://github.com/joke2k/faker      
###
#### "Faker little helper" helps to generate .csv files with random values.

All you need to do is select columns you want generate.
Optionally you can set:
- how many rows FLH generate (20 is default)
- locales (default is english "en")
- filename(s) (default: "file.csv")

### Virtualenv and run: ###
```commandline
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ python3 faker_little.helper.py
```