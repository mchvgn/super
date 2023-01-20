import pandas  as pd
import calendar
from time import  sleep
from selenium import  webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def construct_year_dataframe(driver, year):

    driver.get(f'https://www.superenalotto.com/risultati/{year}')
    sleep(10)
    table = driver.find_element(By.XPATH, '/html/body/div[1]/section[2]/table/tbody')

    trs = table.find_elements(By.TAG_NAME, 'tr')
    ths = table.find_elements(By.TAG_NAME, 'th')


    all_numbers = []
    for i in range(int(len(trs)/2)):
        for j in range(7):
            number = table.find_element(By.XPATH, f'/html/body/div[1]/section[2]/table/tbody/tr[{i+1}]/td/table/tbody/tr/td[{j+1}]')
            all_numbers.append(int(number.text))

    all_numbers_by_7  =[list(x) for x in zip(*[iter(all_numbers)]*7)]

    list_of_rows = []

    converter = {'gennaio':'January', 'febbraio':'February', 'marzo':'March', 'aprile':'April', 'maggio':'May', 'giugno':'June', 'luglio':'July', 'agosto':'August', 'settembre':'September', 'ottobre':'October', 'novembre':'November', 'dicembre':'December'}
    for i, th in enumerate(ths):

        row = []
        data = th.text
        for key in converter.keys():
            data = data.replace(key, converter[key])
            # print(data)
        data = datetime.strptime(data, "%d %B %Y")
        row.append(data.date())

        for number in [*all_numbers_by_7[i]]:
            row.append(number)
        list_of_rows.append(row)
    
    df = pd.DataFrame(list_of_rows, columns=['data', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'star'])

    df['data'] = pd.to_datetime(df['data'])
    df['day_of_week'] = df['data'].dt.weekday
    df['day_of_week'] = df['day_of_week'].apply(lambda x: calendar.day_name[x])

    df = df[['data', 'day_of_week', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'star']]
    df = df.set_index('data', drop=True)

    return df

def scrape_superanalotto(year=2023):

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    list_df = []

    list_of_years = [*range(1997,year+1,1)]
    for year in list_of_years:
        df = construct_year_dataframe(driver, year)
        list_df.append(df)
    
    final_df = pd.concat(list_df)


    final_df = final_df.sort_index(ascending=False)

    driver.close()
    # final_df.to_csv('super_analotto.csv')
    return final_df




scrape_superanalotto()