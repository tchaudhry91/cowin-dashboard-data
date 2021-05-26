import datetime

BROWSER_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"


def get_common_headers():
    return {
        "User-Agent": BROWSER_USER_AGENT
    }


def get_formatted_date():
    return datetime.datetime.today().strftime("%Y-%m-%d")


def clean_date(date_str):
    d = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return d.strftime("%d-%m-%Y")
