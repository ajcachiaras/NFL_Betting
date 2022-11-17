import csv
import time
import MenuClicker
import WeekScraper
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome('/Applications/driver/chromedriver')
driver.get('https://www.vegasinsider.com/nfl/matchups/')
# MenuClicker.iterate_lines(driver)
header = ['year', 'week', 'away_team', 'home_team',
          'spread_bet_pct', 'spread_money_pct', 'O/U_bet_pct', 'O/U_money_pct',
          'away_team(scores)', 'home_team(scores)', 'away_score', 'home_score', 'away_spread', 'home_spread',
          'hit_away_spread', 'hit_home_spread', 'O/U_total_line', 'O/U_total_hit']


line_output = MenuClicker.iterate_lines(driver)
driver.get('https://www.vegasinsider.com/nfl/scoreboard/')
driver.execute_script("window.scrollTo(0, 100)")
score_output = MenuClicker.iterate_scores(driver)

print(len(line_output))
print(len(score_output))

file = open('C:/Users/ajcac/PycharmProjects/NFL_Betting/CombinedOutputData.csv', 'w')
writer = csv.writer(file)
writer.writerow(header)

for week in line_output:
    # need to combine and write info from scores too
    for game in week:
        writer.writerow(game)

file.close()

time.sleep(3)
driver.quit()




