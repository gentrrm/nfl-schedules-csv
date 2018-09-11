import os
import requests
import csv
import json
from datetime import datetime
from bs4 import BeautifulSoup


PATH = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = PATH + 'teams.json'


def get_teams(json_file : str) -> dict:
    """Creates Dictionary of team names with their url from the json file"""
    with open('teams.json', 'r+') as jfile:
        return dict(json.load(jfile))


def get_schedule_rows(url : str) -> list:
    page = requests.get(url)
    # Create soup
    soup = BeautifulSoup(page.content, 'html.parser')
    # Find the table
    table = soup.find('table', attrs={'class' : 'tablehead'})
    # All table rows that have team schedule information have 
    # odd row and even row tags.
    return soup.find_all('tr', attrs={'class' : 'oddrow'}) + \
           soup.find_all('tr', attrs={'class' : 'evenrow'})


def write_to_csv(file_name : str, rows : list) -> None:
    # Write dates and teams to csv file.
    with open(PATH + '/schedules/' + file_name + '.csv', 'w+') as csvfile:
        writer = csv.writer(csvfile)
        # Write headers
        writer.writerow(["Week", "Team", "Date"])
        for row in rows:
            try:
                try:
                    time = row.find_all('td')[3].text
                    time = time[:time.index('M') + 1]
                    date = datetime.strptime(row.find_all('td')[1].text + " " + time, 
                                             '%a, %b %d %I:%M %p').replace(year=2018)
                except Exception:
                    # This means there is not date.
                    date = datetime.strptime(row.find_all('td')[1].text, '%a, %b %d') \
                                   .replace(year=2018)
                writer.writerow([row.find_all('td')[0].text,
                                 row.find_all('td')[2].text, 
                                 date])
                
            except ValueError as e:
                # This means that there is a BYE WEEK
                writer.writerow([row.find_all('td')[0].text, row.find_all('td')[1].text])


def main():
    # Get the teams dictionary
    teams = get_teams(JSON_FILE)
    for team, url in teams.items():
        rows = get_schedule_rows(url)
        write_to_csv(team, rows)
        
        
def test():
    teams = {"cardinals" : "http://www.espn.com/nfl/team/schedule/_/name/ari"}
    for team, url in teams.items():
        rows = get_schedule_rows(url)
        write_to_csv(team, rows)
        


if __name__ == '__main__':
    main()
