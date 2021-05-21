#!/usr/bin/env python

from lib import get_district_list, build_district_top_level_data, get_district_public_reports, get_formatted_date, write_csv

if __name__ == "__main__":
    district_list = get_district_list()
    district_top_level_data_list = []
    for district in district_list:
        print("Building data for: " + district.get("district_name"))
        district_top_level_data_list.append(
            build_district_top_level_data(get_district_public_reports(district.get(
                "district_id"), district.get("state_id"), district.get("district_name"), get_formatted_date()))
        )
    print("Writing CSV")
    write_csv("district_vaccination.csv", district_top_level_data_list)
    print("Done")
