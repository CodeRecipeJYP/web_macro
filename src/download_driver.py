from src.utils.shell import get_statement_with_cd, execute_with_message


def download_driver(target_directory):
    url = "https://chromedriver.storage.googleapis.com/2.43/chromedriver_mac64.zip"
    statement = get_statement_with_cd(target_directory, "wget -O {} {}".format("chromedriver.zip", url))
    execute_with_message(statement)


def extract_driver(target_directory):
    statement = get_statement_with_cd(target_directory, "tar xf {}".format("chromedriver.zip"))
    execute_with_message(statement)


def install_driver(target_directory):
    download_driver(target_directory)
    extract_driver(target_directory)


if __name__ == '__main__':
    install_driver("../driver")
