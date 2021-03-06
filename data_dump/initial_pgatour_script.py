from typing import Dict

import requests


def get_stats_dict(year: str, stat_id: str) -> Dict: 
    
    response = requests.get(f'https://statdata.pgatour.com/r/stats/{year}/{stat_id}.json')
    if response.status_code != 200:
        return
    json_response = response.json()
    player_stats_dict = json_response['tours'][0]['years'][0]['stats'][0]
    
    stat_titles = player_stats_dict['statTitles']
    stat_titles_num = int(player_stats_dict['statTitles']['numOfStatTitles'])
    
    final_dict = []
    for player in player_stats_dict['details']:
        temp = {}

        temp['statId'] = stat_id
        temp['year'] = year 
        temp['playerId'] = player['plrNum']

        players_stats = player['statValues']
        temp['rndEvents'] = players_stats['rndEvents']
        
        for i in range(1, stat_titles_num + 1):
            temp[stat_titles[f'statTitle{i}']] = players_stats[f'statValue{i}']

        final_dict.append(temp)
    return final_dict

def get_players():
    r = requests.get("https://statdata.pgatour.com/players/player.json")
    data = r.json()
    player_details = data['plrs']
    players = [{'player_id': plr['pid'],
             'first_name': plr['nameF'],
             'last_name': plr['nameL'],
             'nationality': plr['ct'],
             'years_on_tour': [int(x) for x in plr['yrs']]}
            for plr in player_details]
    return players


def main():
    year = 2020
    s = get_stats_dict(year = year, stat_id = '101')
    n = 1000
    chunks = [s[i:i + n] for i in range(0, len(s), n)]
    for chunk in chunks:
        for i in range(len(chunk)):
            player = chunk[i]
            chunk[i] = (
                (
                    player['playerId'],
                    year,
                    player['Avg.']
                )
            )

if __name__ == "__main__":
    main()