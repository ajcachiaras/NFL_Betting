import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def game_xpath(game_num):
    return '/html/body/div[1]/main/div[2]/div/div/div/div[1]/bc-scores-table/div/div[2]/div/div[' + str(game_num) + "]"


def get_team_name_xpath_suffix(index):
    return '/div[2]/div[1]/div[1]/div['+str(index)+']/div/a[1]'


def get_closing_values_xpath_suffix(index):
    return '/div[2]/div[1]/div[2]/div[1]/div[' + str(index) + ']'


def get_scores_xpath_suffix(index):
    return '/div[2]/div[2]/div[2]/div[2]/div/div[' + str(index) + ']'


def get_scores(driver, year, week):
    # num_games = 2
    # for game in range(num_games):
    # print("getting data for year " + str(year) + " week " + str(week))
    output = []
    # for game in range(num_games):
    game = 0
    while True:
        html_game_idx = game+1
        try:  # this will break when we run out of games to scrape on that page
            away_team = driver.find_element(By.XPATH, game_xpath(html_game_idx)+get_team_name_xpath_suffix(1))
            home_team = driver.find_element(By.XPATH, game_xpath(html_game_idx)+get_team_name_xpath_suffix(2))
            first_close = driver.find_element(By.XPATH, game_xpath(html_game_idx)+get_closing_values_xpath_suffix(1))
            second_close = driver.find_element(By.XPATH, game_xpath(html_game_idx)+get_closing_values_xpath_suffix(2))
            away_score = driver.find_element(By.XPATH, game_xpath(html_game_idx)+get_scores_xpath_suffix(1))
            home_score = driver.find_element(By.XPATH, game_xpath(html_game_idx)+get_scores_xpath_suffix(2))

            # print("Away Team: " + away_team.text + " Home Team: " + home_team.text)
            # print("Away score: " + str(away_score.text) + " Home score: " + str(home_score.text))
            # print("First close: " + first_close.text + " Second close: " + second_close.text)
            total_score_line = max(float(first_close.text), float(second_close.text))
            away_spread = 0.0
            home_spread = 0.0
            # need to figure out if home or away is favored
            if float(first_close.text) == min(float(first_close.text), float(second_close.text)):  # away team is favored
                away_spread = float(first_close.text)
                home_spread = abs(float(first_close.text))
            else:  # home team is favored
                home_spread = float(second_close.text)
                away_spread = abs(float(second_close.text))

            point_diff_line = min(float(first_close.text), float(second_close.text))
            # print("Away spread: " + str(away_spread) + " Home spread: " + str(home_spread))
            # print("Point diff line: " + str(point_diff_line)+" Total line: " + str(total_score_line))

            hit_score_total_line = (float(home_score.text) + float(away_score.text)) > total_score_line
            # print("Total hit: " + str(hit_score_total_line))
            hit_away_spread = (float(away_score.text) + away_spread) > float(home_score.text)
            hit_home_spread = (float(home_score.text) + home_spread) > float(away_score.text)
            # print("Away spread hit: " + str(hit_away_spread) + " Home spread hit: " + str(hit_home_spread))
            # print()

            output.append([away_team.text, home_team.text, float(away_score.text), float(home_score.text), away_spread, home_spread, hit_away_spread,
                           hit_home_spread, total_score_line, hit_score_total_line])
        except:
            print("got data for year " + str(year) + " week " + str(week)+" and " + str(game)+" games")
            break  # stop searching for games
        game = game + 1
    return output


def get_lines(driver, year, week):
    # driver.get('https://www.vegasinsider.com/nfl/matchups/')

    games = driver.find_elements(By.CLASS_NAME, "betting-trends-event-card")
    matchup1 = games[0].find_elements(By.CLASS_NAME, "team-name")

    # print(matchup1[0].text + " vs " + matchup1[2].text)

    matchup2 = games[1].find_elements(By.CLASS_NAME, "team-name")

    odds_row = []
    all_output = []
    for matchup in games:
        teams = matchup.find_elements(By.CLASS_NAME, "team-name")
        all_odds = matchup.find_element(By.CLASS_NAME, "betting-trends-data")
        ind_odd = all_odds.find_elements(By.CLASS_NAME, "betting-trends-pill")
        # for i in range(0, len(ind_odd)):
        #     print(ind_odd[i].text)

        odds_row.append([teams[0].text, teams[2].text, ind_odd[0].text, ind_odd[1].text,
                         ind_odd[2].text, ind_odd[3].text])

        all_output.append([year + 2021, week + 1, teams[0].text, teams[2].text, ind_odd[0].text,
                           ind_odd[1].text, ind_odd[2].text, ind_odd[3].text])

        # print(teams[0].text + "vs " + teams[2].text)
        # print("Spread| Bets: " + ind_odd[0].text + " Money: " + ind_odd[1].text)
        # print("O/U| Bets: " + ind_odd[2].text + " Money: " + ind_odd[3].text)
        # print()
    return all_output
