from bs4 import BeautifulSoup
from colorama import init
from web_scraper import get_html_content
from lb import print_loading_bar
from print import print_account_info, write_account_info_to_csv
import csv
import re

init()


# FIX account_number check for starting w digit

def parse_judgment_years(judgment_data_lines):
    parsed_years = []
    for judgment_line in judgment_data_lines:
        judgment_line = judgment_line.strip()
        if judgment_line == '- ( 0 )':
            parsed_years.append((-1, -1))  # Use a special value to represent "all years are paid"
            continue
        match = re.search(r'(\d{4}) - (\d{4})\s*\(\s*\d+\s*\)', judgment_line)
        if match:
            start_year, end_year = map(int, match.groups())
            parsed_years.append((start_year, end_year))
    return parsed_years


def check_if_judgment_years_paid(judgment_year_ranges, due_years):
    for year in due_years:
        for start_year, end_year in judgment_year_ranges:
            if start_year <= year <= end_year:
                return False
    return True


host = 'actweb.acttax.com'
base_path = '/act_webdev/hidalgo/showdetail2.jsp?can='
payment_path = '/act_webdev/hidalgo/reports/paymentinfo.jsp?can='
taxbyyear_path = '/act_webdev/hidalgo/reports/taxbyyear.jsp?can='
judgment_years_base_path = '/act_webdev/hidalgo/reports/judgmentyears.jsp?can='

with open("accountNumbers.txt", "r") as file:
    account_numbers = [num.strip() for num in file.readlines()]

with open("judgmentYears.txt", "r") as file:
    judgment_years_data = [line.strip() for line in file.readlines()]

all_parsed_judgment_years = []
for judgment_data in judgment_years_data:
    parsed_judgment_year = parse_judgment_years([judgment_data])
    all_parsed_judgment_years.append(parsed_judgment_year)

account_number_counter = 0
no_counter = 0
with (open('account_data.csv', mode='w', newline='') as csv_file):
    fieldnames = ['Account Number', 'Exemptions', 'Current Amt Due', 'Current Yrs Due', 'Last Pymt Date', 'Notes']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for account_number in account_numbers:

        parsed_judgment_years = all_parsed_judgment_years[account_number_counter]
        account_number_counter += 1

        print_loading_bar(100, prefix=f'{account_number_counter}) Scraping Data:', suffix='Complete', length=50)

        html_content = get_html_content(host, base_path + account_number)
        doc = BeautifulSoup(html_content, "html.parser")

        exemptions = None
        current_amt_due = None

        h3_tags = doc.find_all("h3")
        for h3 in h3_tags:
            if "Total Amount Due:" in h3.text:
                current_amt_due_text = h3.text.split("Total Amount Due:")[-1].strip()
                match_result = re.search(r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?', current_amt_due_text)
                if match_result:
                    current_amt_due = match_result.group(0)

            if "<b>Exemptions:</b>" in str(h3):
                exemptions = h3.get_text(separator=" ").replace("Exemptions:", "").strip()

        html_content = get_html_content(host, payment_path + account_number)
        doc = BeautifulSoup(html_content, "html.parser")

        last_payment_date = "N/A"
        payment_table = doc.find("table", align="center")
        if payment_table:
            payment_rows = payment_table.find_all("tr")[1:]

            if payment_rows:
                most_recent_payment_row = payment_rows[0]
                date_cell = most_recent_payment_row.find_all("td")[0]
                if date_cell:
                    date_text = date_cell.text.strip()
                    if '-' in date_text:
                        last_payment_date = '/'.join([date_text.split('-')[1],
                                                      date_text.split('-')[2],
                                                      date_text.split('-')[0]])

        html_content = get_html_content(host, taxbyyear_path + account_number)
        doc = BeautifulSoup(html_content, "html.parser")

        tr_tags = doc.find_all("tr")
        years_due = []

        for tr in tr_tags:
            td_tags = tr.find_all("td")
            if len(td_tags) > 0 and td_tags[0].text.strip().isdigit():
                year_value = int(td_tags[0].text.strip())
                years_due.append(year_value)

        years_due.sort()

        if not years_due:
            years_due_str = "N/A"
        else:
            ranges = []
            start = years_due[0]
            end = years_due[0]
            for i in range(1, len(years_due)):
                if years_due[i] == end + 1:
                    end = years_due[i]
                else:
                    if start == end:
                        ranges.append(f"{start}")
                    else:
                        ranges.append(f"{start}-{end}")
                    start = years_due[i]
                    end = years_due[i]
            if start == end:
                ranges.append(f"{start}")
            else:
                ranges.append(f"{start}-{end}")
            years_due_str = ", ".join(ranges)

        suit_type = ''
        if account_number[5] == '9':
            if account_number[6] == '9':
                suit_type = "BPP"
            if account_number[6] == '7':
                suit_type = "Mobile Home"

        if check_if_judgment_years_paid(parsed_judgment_years, years_due):
            suit_type += " Judg yrs paid"
        elif years_due_str == 'N/A':
            suit_type += " Judg yrs paid"

        if (exemptions and exemptions != 'None') or ('BPP' in suit_type) or ('Judg yrs paid' in suit_type) or (
                'Mobile Home' in suit_type):
            no_counter += 1

        if (
            exemptions == 'Data not found.' and
            current_amt_due == 'Data not found.' and
            years_due_str == 'N/A' and
            last_payment_date == 'N/A'
           ):
            suit_type = 'Invalid Account.'

        write_account_info_to_csv(writer, account_number, exemptions,
                                  current_amt_due, years_due_str, last_payment_date, suit_type)

        print_account_info(account_number, exemptions, current_amt_due,
                           years_due_str, last_payment_date, suit_type)

print("No counter: ", no_counter)
print("Total accounts: ", account_number_counter)
