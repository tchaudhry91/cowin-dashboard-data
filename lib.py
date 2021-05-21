from common import get_common_headers, get_formatted_date
from http import HTTPStatus
import csv
import requests


class FetchException(Exception):
    def __init__(self, url, message):
        self.url = url
        self.message = message


def get_district_list():
    """
    Fetches the state/district list.
    returns: a list of objects : [{'district_id', 'district_name', 'state_id'}]
    """
    url = "https://dashboard.cowin.gov.in/assets/json/csvjson.json"
    resp = requests.get(url, headers=get_common_headers())
    if resp.status_code != HTTPStatus.OK:
        raise FetchException(url, resp.status_code)
    return resp.json()


def get_district_public_reports(district_id, state_id, district_name, date):
    """
    Fetches the public reports for a particular district. This serves as the base JSON for more data parsing
    returns: the entire object containing broad session/registration/vaccination data
    """
    url = "https://api.cowin.gov.in/api/v1/reports/v2/getPublicReports"
    query = {'state_id': state_id, 'district_id': district_id, 'date': date}
    resp = requests.get(
        url, params=query, headers=get_common_headers())
    if resp.status_code != HTTPStatus.OK:
        raise FetchException(url, resp.status_code)
    district_data = resp.json()
    # Add some base information as well
    district_data['district_id'] = district_id
    district_data['state_id'] = state_id
    district_data['district_name'] = district_name
    return district_data


def build_district_top_level_data(district_public_report):
    """
    Builds a filtered 1 level deep object for the given district with only top level data
    """
    data = {
        'district_id': district_public_report.get("district_id"),
        'district_name': district_public_report.get("district_name"),
        'state_id': district_public_report.get("state_id")
    }
    top_block = district_public_report.get("topBlock")
    vaccination_by_age = district_public_report.get("vaccinationByAge")
    # Sites
    data['sites_total'] = top_block.get("sites").get("total")
    data['sites_govt'] = top_block.get("sites").get("govt")
    data['sites_pvt'] = top_block.get("sites").get("pvt")
    # Sessions
    data['sessions_total'] = top_block.get("sessions").get("total")
    data['sessions_govt'] = top_block.get("sessions").get("govt")
    data['sessions_pvt'] = top_block.get("sessions").get("pvt")
    # Vaccination
    data['total_vaccination'] = top_block.get("vaccination").get("total")
    data['male_vaccination'] = top_block.get("vaccination").get("male")
    data['female_vaccination'] = top_block.get("vaccination").get("female")
    data['other_vaccination'] = top_block.get("vaccination").get("others")
    data['18_30_vaccination'] = vaccination_by_age.get("vac_18_30")
    data['30_45_vaccination'] = vaccination_by_age.get("vac_30_45")
    data['45_60_vaccination'] = vaccination_by_age.get("vac_45_60")
    data['60+_vaccination'] = vaccination_by_age.get("above_60")
    data['covishield'] = top_block.get("vaccination").get("covishield")
    data['covaxin'] = top_block.get("vaccination").get("covaxin")
    data['dose1'] = top_block.get("vaccination").get("tot_dose_1")
    data['dose2'] = top_block.get("vaccination").get("tot_dose_2")
    data['aefi'] = top_block.get("vaccination").get("aefi")

    return data


def write_csv(fname, district_top_level_data_list):
    """
    Write top level data out to a csv
    """
    with open(fname, "w") as csvfile:
        fieldnames = [
            "district_id",
            "state_id",
            "district_name",
            "sites_total",
            "sites_govt",
            "sites_pvt",
            "sessions_total",
            "sessions_govt",
            "sessions_pvt",
            "total_vaccination",
            "male_vaccination",
            "female_vaccination",
            "other_vaccination",
            "18_30_vaccination",
            "30_45_vaccination",
            "45_60_vaccination",
            "60+_vaccination",
            "covishield",
            "covaxin",
            "dose1",
            "dose2",
            "aefi",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for district_top_level_data in district_top_level_data_list:
            writer.writerow(district_top_level_data)
