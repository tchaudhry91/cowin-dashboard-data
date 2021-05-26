#!/usr/bin/env python

from lib import get_district_list, build_district_top_level_data, get_district_public_reports, write_csv, get_vac_weekly_reports, write_csv_weekly
from common import get_formatted_date

if __name__ == "__main__":
    district_list = get_district_list()
    district_weekly_data_list = []
    for district in district_list:
        print("Building Weekly Data for: " + district.get("district_name"))
        district_weekly_data_list.append(get_vac_weekly_reports(district.get(
            "district_id"), district.get("state_id"), district.get("district_name"), get_formatted_date()))

    print("Writing Weekly CSV")
    write_csv_weekly("weekly_report.csv", district_weekly_data_list)

    district_top_level_data_list = []
    for district in district_list:
        print("Building data for: " + district.get("district_name"))
        district_top_level_data_list.append(
            build_district_top_level_data(get_district_public_reports(district.get(
                "district_id"), district.get("state_id"), district.get("district_name"), get_formatted_date()))
        )
    print("Writing Top Level CSV")
    write_csv("district_vaccination.csv", district_top_level_data_list)
