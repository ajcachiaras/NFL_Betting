import time
import WeekScraper
from selenium import webdriver
from selenium.webdriver.common.by import By

weeks_per_year = [18, 11]

def iterate_lines(driver):
    # driver.get('https://www.vegasinsider.com/nfl/matchups/')
    dropdowns = driver.find_elements(By.CLASS_NAME, "bc-dropdown")
    line_output = []
    score_output = []

    for year in range(2):
        # print('year: ' + str(year))
        year_arrow = dropdowns[0].find_element(By.CLASS_NAME, "fa-angle-down")

        year_arrow.click()
        time.sleep(0.25)
        # redefining dropdowns because the elements are redrawn
        dropdowns = driver.find_elements(By.CLASS_NAME, "bc-dropdown")
        year_menu = dropdowns[0].find_element(By.CLASS_NAME, "dropdown-menu")
        year_menu_items = year_menu.find_elements(By.CLASS_NAME, "dropdown-item")

        year_menu_items[year].click()
        time.sleep(1)
        for week in range(weeks_per_year[year]):
            act_week = week + 4
            # print('week: ' + str(week))
            dropdowns = driver.find_elements(By.CLASS_NAME, "bc-dropdown")
            week_arrow = dropdowns[1].find_element(By.CLASS_NAME, "fa-angle-down")
            week_arrow.click()

            time.sleep(0.5)

            week_menu = dropdowns[1].find_element(By.CLASS_NAME, "dropdown-menu")

            week_menu_items = week_menu.find_elements(By.CLASS_NAME, "dropdown-item")

            week_menu_items[act_week].click()
            time.sleep(0.75)
            line_output.append(WeekScraper.get_lines(driver, year, week))
            # print('got week ' + week.__str__())
    return line_output


def iterate_scores(driver):
    # driver.get('https://www.vegasinsider.com/nfl/matchups/')
    dropdowns = driver.find_elements(By.CLASS_NAME, "bc-dropdown")
    score_output = []
    time.sleep(30)

    for year in range(2):
        print('year: ' + str(year))
        year_arrow = dropdowns[0].find_element(By.CLASS_NAME, "fa-angle-down")

        year_arrow.click()
        time.sleep(.5)
        # redefining dropdowns because the elements are redrawn
        dropdowns = driver.find_elements(By.CLASS_NAME, "bc-dropdown")
        year_menu = dropdowns[0].find_element(By.CLASS_NAME, "dropdown-menu")
        year_menu_items = year_menu.find_elements(By.CLASS_NAME, "dropdown-item")

        year_menu_items[year].click()
        time.sleep(1)
        for week in range(weeks_per_year[year]):
            week_menu_idx = week + 4
            dropdowns = driver.find_elements(By.CLASS_NAME, "bc-dropdown")
            week_arrow = dropdowns[1].find_element(By.CLASS_NAME, "fa-angle-down")
            week_arrow.click()
            time.sleep(.25)

            week_menu = dropdowns[1].find_element(By.CLASS_NAME, "dropdown-menu")

            week_menu_items = week_menu.find_elements(By.CLASS_NAME, "dropdown-item")
            clicked = False
            count = 0
            while not clicked:
                try:
                    week_menu_items[week_menu_idx].click()
                    clicked = True
                except:
                    print("failed to click on week "+str(week)+" for click "+str(count))
                    count = count + 1
                    time.sleep(0.2)
            time.sleep(.5)
            score_output.append(WeekScraper.get_scores(driver, year, week))
    return score_output
