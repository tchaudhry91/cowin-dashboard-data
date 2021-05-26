#!/usr/bin/env python

from lib import get_district_list, build_district_top_level_data, get_district_public_reports, write_csv, get_vac_weekly_reports, write_csv_weekly_vac, write_csv_registeration_national_weekly, get_weekly_registration_trends, get_session_daily_reports, write_csv_daily_sessions
from common import get_formatted_date
import argparse


def write_district_wise_vac_weekly_csv(fname, district_list):
    district_weekly_data_list = []
    for district in district_list:
        print("Building Weekly Vaccination Data for: " +
              district.get("district_name"))
        district_weekly_data_list.append(get_vac_weekly_reports(district.get(
            "district_id"), district.get("state_id"), district.get("district_name"), get_formatted_date()))

    print("Writing Weekly CSV to: " + fname)
    write_csv_weekly_vac(fname, district_weekly_data_list)


def write_district_wise_daily_sessions_csv(fname, district_list):
    district_daily_sessions_list = []
    for district in district_list:
        print("Building Daily Session Data for: " +
              district.get("district_name"))
        district_daily_sessions_list.append(get_session_daily_reports(district.get(
            "district_id"), district.get("state_id"), district.get("district_name"), get_formatted_date()))

    print("Writing Daily Session CSV to: " + fname)
    write_csv_daily_sessions(fname, district_daily_sessions_list)


def write_district_top_level_data_csv(fname, district_list):
    district_top_level_data_list = []
    for district in district_list:
        print("Building data for: " + district.get("district_name"))
        district_top_level_data_list.append(
            build_district_top_level_data(get_district_public_reports(district.get(
                "district_id"), district.get("state_id"), district.get("district_name"), get_formatted_date()))
        )
    print("Writing Top Level CSV to" + fname)
    write_csv(fname, district_top_level_data_list)


def write_national_registration_trend_csv(fname):
    national_registration_data = get_weekly_registration_trends(
        get_formatted_date())
    print("Writing National Registration Trends to: " + fname)
    write_csv_registeration_national_weekly(fname, national_registration_data)


def main(args):
    district_list = get_district_list()
    if args.type == "weekly_vac_report_district" or args.type == "all":
        write_district_wise_vac_weekly_csv(
            "weekly_vac_report_district_wise.csv", district_list)
    if args.type == "top_level_district_report" or args.type == "all":
        write_district_top_level_data_csv(
            "district_vaccination_top_level.csv", district_list)
    if args.type == "national_registration_trends" or args.type == "all":
        write_national_registration_trend_csv(
            "national_registration_trend.csv")
    if args.type == "daily_session_report_district" or args.type == "all":
        write_district_wise_daily_sessions_csv(
            "district_sessions_daily.csv", district_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Gather CoWin Dashboard Data into CSVs")
    parser.add_argument(
        '--type', default="all", help="top_level_district_report/weekly_vac_report_district/national_registration_trends/daily_session_report_district")

    args = parser.parse_args()
    main(args)
