import functools
import pandas as pd
import datetime
import ast
import requests

#keys required for API requests
token = #your token
app_token = #your app token

save_to = "/speeches.csv"
save_errors_to = "/errors.txt"

#getting list of deputies of all convocations of the GosDuma (no duplicate values)
deputies = requests.get(f"http://api.duma.gov.ru/api/{token}/deputies.json?position=Депутат%20ГД&app_token={app_token}").json()

#extracts and processes transcripts from one page and appends speech texts to dep_speech
def extract_speeches(page, dep_factions):
    global df
    for meeting in page['meetings']:
        meeting_date = datetime.datetime.strptime(meeting['date'].split()[0], '%Y-%m-%d')
        cur_faction = None
        for faction in dep_factions:
            start_date = datetime.datetime.strptime(faction['startDate'], '%Y-%m-%d')
            end_date = datetime.datetime.strptime(faction['endDate'], '%Y-%m-%d')
            if start_date <= meeting_date and meeting_date <= end_date:
                cur_faction = faction['name']
                break

        for question in meeting['questions']:
            speech = str()
            for part in question['parts']:
                part = functools.reduce(lambda line_1, line_2: line_1.strip() + ' ' + line_2.strip(), part['lines'])
                speech = speech + '\n' + part
            new_row = pd.DataFrame({'deputy': page['name'],
                                    'faction': cur_faction,
                                    'question': question['name'],
                                    'date': meeting['date'].split()[0],
                                    'text': speech}, index=[0])
            df = pd.concat([df, new_row], ignore_index=True)

def process_page(deputy, page_number) -> bool:
    dep_id = deputy['id']
    dep_factions = deputy['factions']
    response = requests.get(f"http://api.duma.gov.ru/api/{token}/transcriptDeputy/{dep_id}.json?page={page_number}&app_token={app_token}")
    page = response.json()
    if not page['meetings']:
        return False
    else:
        extract_speeches(page, dep_factions)
        return True

def get_deputy_speeches(deputy):
    cont = True
    for page_number in range(1, 10000):
        try:
            if cont == False:
                print(f"completed with {page_number - 2} pages")
                return
            cont = process_page(deputy, page_number)
        except:
            with open(save_errors_to, 'a') as errors:
                errors.write(str(deputy) + ' ' + str(page_number) + '\n')

def gather_data(begin, end):
    count = 0
    for deputy in deputies[begin - 1 : min(end - 1, len(deputies))]:
        count += 1
        print(f"{count} {deputy['name']} {deputy['id']}", end=" ")
        get_deputy_speeches(deputy)

df = pd.DataFrame(columns=['deputy', 'faction', 'question', 'date', 'text'])
gather_data(1, len(deputies))
df.to_csv(save_to)

df = pd.DataFrame(columns=['deputy', 'faction', 'question', 'date', 'text'])
with open(save_errors_to, 'r') as f:
    errors = f.readlines()
    print(len(errors))
    for error in errors:
        error = error.rsplit(maxsplit=1)
        deputy = ast.literal_eval(error[0])
        page_number = int(error[1])
        try:
            process_page(deputy, page_number)
        except:
            print(deputy, page_number, "ERROR")

df.to_csv(save_to)