import requests
from bs4 import BeautifulSoup
import csv
import os


date = input('Enter the date as mm/dd/yy: ')
page = requests.get(f'https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}') 

def main(page):
    src = page.content
    soup = BeautifulSoup(src, 'lxml')
    champions = soup.find_all("div", {'class':'matchCard'})
    match_details = []

    def get_match_info(champion): 
        champion_title = champion.contents[1].find('h2').text.strip()
        all_matches = champion.contents[3].find_all("div", {'class':'teamsData'})
        num_of_matches = len(all_matches)

        for i in range(num_of_matches):
            # Get teams names
            team_a = all_matches[i].find("div", {'class':'teamA'}).text.strip()
            team_b = all_matches[i].find("div", {'class':'teamB'}).text.strip()

            # Get score
            match_result = all_matches[i].find("div", {'class':'MResult'}).find_all("span", {'class':'score'})
            score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"

            # Get time 
            match_time = all_matches[i].find("div", {'class':'MResult'}).find("span", {'class':'time'}).text.strip()

            match_details.append({
                'نوع البطولة': champion_title, 
                'الفريق الاول': team_a, 
                'الفريق الثاني': team_b,
                'الوقت': match_time,
                'النتيجة': score
            })     
            
    for champion in champions:
        get_match_info(champion)   

    # Ensure the directory exists
    os.makedirs('yallkora', exist_ok=True)

    keys = match_details[0].keys()
    with open('yallkora/matches_details.csv', 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(match_details)

        print('File Created')

main(page)
