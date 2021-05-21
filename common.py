import datetime

BROWSER_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"


def get_common_headers():
    return {
        "User-Agent": BROWSER_USER_AGENT
    }


def get_formatted_date():
    return datetime.datetime.today().strftime("%Y-%m-%d")
