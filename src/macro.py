from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def exercisetype_equals(reserve, exercise_type):
    return (exercise_type in reserve.text)


def is_hayoung_want_exercisetype(reserve):
    if exercisetype_equals(reserve, "1/바렐&보드"):
        return True

    if exercisetype_equals(reserve, "1/리포머"):
        return True

    return False


def parse_minute_from(time_as_str):
    return int(time_as_str[:2]) * 60 + int(time_as_str[3:5])


def starttime_in_range(reserve, minimum, maximum):
    startendtime_idx = reserve.text.find("시　　간")
    found_idx = reserve.text.find("~", startendtime_idx)
    starttime_as_str = reserve.text[found_idx-6:found_idx-1]

    print("starttime_as_str: {}".format(starttime_as_str))
    starttime_as_minute = parse_minute_from(starttime_as_str)
    minimum_as_minute = minimum * 60
    maximum_as_minute = maximum * 60
    print("min: {} starttime: {} max: {}".format(
        minimum_as_minute, starttime_as_minute, maximum_as_minute))
    if minimum_as_minute <= starttime_as_minute <= maximum_as_minute:
        return True

    return False


def is_hayoung_want_starttime(reserve):
    # 19:00 ~
    # 19:30 ~
    # 20:00 ~
    # 19~20에 시작하는것
    return starttime_in_range(reserve, 19, 20)


def is_hayoung_want(reserve):
    if not is_hayoung_want_exercisetype(reserve):
        return False

    if not is_hayoung_want_starttime(reserve):
        return False

    return True


def execute_reserve(driver, reserve):
    execute_dd = reserve.find_element_by_class_name("rbutton")
    execute_button = execute_dd.find_element_by_tag_name("button")
    print("execute_dd.id={}".format(execute_dd.id))

    print(execute_button.text)
    if execute_button.text == "예약":
        def _wait_documentready(_driver):
            return _driver.execute_script("return document.readyState") == "complete"

        # WebDriverWait(driver, 30).until(_wait_documentready)

        # element = WebDriverWait(driver, 20)\
        #     .until(expected_conditions.staleness_of(execute_button))
        sleep(10)
        # WebDriverWait(driver, 30).until(expected_conditions.element_to_be_clickable((By.ID, execute_dd.id)))
        print("execute_button.click()")

        execute_dd = reserve.find_element_by_class_name("rbutton")
        execute_button = execute_dd.find_element_by_tag_name("button")
        execute_button.click()
        print("clicked")

        # from datetime import datetime
        # driver.screenshot("reserved_{:d}.png".format(int(datetime.now().timestamp())))
        alert = driver.switch_to.alert
        print("alert={}".format(alert.text))
        alert.accept()
        return True

    return False


def macro(driverpath, targetdate):
    driver = webdriver.Chrome(driverpath)
    driver.implicitly_wait(10)

    driver.get("http://sbodyworksh.flexgym.pro/mobile/reservation.asp")

    alert = driver.switch_to.alert
    alert.accept()

    account = driver.find_element_by_name("memberID")
    password = driver.find_element_by_name("memberPW")
    account.send_keys(credentials.ACCOUNT)
    password.send_keys(credentials.PASSWORD)

    btn_login = driver.find_element_by_class_name("btnLogin")
    btn_login.click()

    btn_popclose = driver.find_element_by_class_name("pop_close")
    btn_popclose.click()

    # todo doesn't work
    driver.execute_script("funcSearch01('{}','C');".format(targetdate))

    reserve_list = driver.find_element_by_id("reserveList").find_elements_by_tag_name("li")
    for idx, each_reserve in enumerate(reserve_list):
        # print("Idx: {}, text: {}".format(idx, each_reserve.text))
        if is_hayoung_want(each_reserve):
            if execute_reserve(driver, each_reserve):
                print("picked")
                break
            pass


if __name__ == '__main__':
    macro("../driver/chromedriver", "2018-11-20")
    macro("../driver/chromedriver", "2018-11-22")

    #
    # "44887213"
    pass
