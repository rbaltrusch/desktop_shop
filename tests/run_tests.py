# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 23:39:42 2021

@author: Korean_Crimson
"""
import argparse
import datetime
import os
import subprocess
import sys
import time

import py

PACKAGE_NAME = "desktop_shop"
REPORTS_PATH = "reports"


def run_tests(args):
    """Add package under test to PYTHONPATH, run pytest to generate html report
    and open the report in the browser.
    """
    script_dir = os.path.abspath(os.path.dirname(__file__))
    package_path = os.path.join(script_dir, "..", PACKAGE_NAME)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"{timestamp}_report.html"
    report_filepath = os.path.join(REPORTS_PATH, report_filename)

    if args.report:
        command_line_args = [
            f"--html={report_filepath}",
            "--self-contained-html",
            f"--cov={package_path}",
            "--cov-report=html",
        ]
    else:
        command_line_args = []

    excludes = []

    if not args.include_slow and not args.include_all:
        excludes.append("slow")

    if not args.include_generate:
        excludes.append("generate")

    if not args.include_unreliable and not args.include_all:
        excludes.append("unreliable")

    if excludes:
        joined = " or ".join(excludes)
        command_line_args.append(f"-m not ({joined})")

    if args.debug:
        command_line_args.append("--pdb")

    # pylint: disable=E1101
    exit_code = py.test.cmdline.main(args=command_line_args)

    if args.report:
        if args.open_in_browser:
            subprocess.call(f"start {report_filepath}", shell=True)  # open test report
            subprocess.call("start htmlcov/index.html", shell=True)  # open coverage report

        if not args.keep:
            # wait 1 second until test report is open, then delete it
            time.sleep(1)
            os.remove(report_filepath)

    if int(exit_code) > 0:
        sys.exit(int(exit_code))


def get_parser():
    """Constructs cli argument parser"""
    parser = argparse.ArgumentParser(description="Unit test interface")

    parser.add_argument(
        "--all", "-a", dest="include_all", action="store_true", help="Include all tests"
    )

    parser.add_argument(
        "--slow", "-s", dest="include_slow", action="store_true", help="Includes slow tests"
    )

    parser.add_argument(
        "--unreliable",
        "-u",
        dest="include_unreliable",
        action="store_true",
        help="Includes unreliable tests",
    )

    parser.add_argument(
        "--db-generation",
        "-g",
        dest="include_generate",
        action="store_true",
        help="Includes database generation tests",
    )

    parser.add_argument("--debug", "-d", action="store_true", help="Enables debug mode")

    parser.add_argument(
        "--no-report",
        "-nr",
        dest="report",
        action="store_false",
        help="Does not generate test reports",
    )

    parser.add_argument(
        "--no-keep",
        "-nk",
        dest="keep",
        action="store_false",
        help="Removes test report after showing",
    )

    parser.add_argument(
        "--no-open",
        "-no",
        dest="open_in_browser",
        action="store_false",
        help="Suppresses test report",
    )
    return parser


def main():
    """Main function"""
    parser = get_parser()
    args = parser.parse_args()
    sys.argv = [__file__]
    run_tests(args)


if __name__ == "__main__":
    main()
