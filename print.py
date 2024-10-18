from termcolor import colored
from random import uniform
import time


def print_account_info(account_number, exemptions, current_amt_due, years_due_str, last_payment_date, suit_type):
    print(f"Account Number: {account_number}")
    time.sleep(uniform(0.0, 0.125))

    # print(f"Exemptions: {colored(exemptions, 'red') if exemptions and exemptions != 'None'
    #                      else exemptions if exemptions
    #                      else 'Data not found.'}")
    # time.sleep(uniform(0.0, 0.25))

    print(f"Current Amt Due: {current_amt_due if current_amt_due 
                              else 'Data not found.'}")
    time.sleep(uniform(0.0, 0.125))

    print(f"Current Yrs Due: {years_due_str if years_due_str 
                              else 'Data not found.'}")
    time.sleep(uniform(0.0, 0.125))

    print(f"Last Pymt Date: {last_payment_date if last_payment_date 
                             else 'Data not found.'}")
    time.sleep(uniform(0.0, 0.125))

    if exemptions != 'None':
        print(f"Notes: {colored((exemptions if exemptions else '') + suit_type, 'red') if 'BPP' in suit_type 
                        or 'Mobile Home' in suit_type 
                        or 'Judg yrs paid' in suit_type 
                        or (exemptions and exemptions != 'None') 
                        else (suit_type if suit_type else 'N/A')}")
        time.sleep(uniform(0.0, 0.125))
    else:
        print(f"Notes: {colored(suit_type, 'red') if 'BPP' in suit_type 
                        or 'Mobile Home' in suit_type 
                        or 'Judg yrs paid' in suit_type 
                        else (suit_type if suit_type else 'N/A')}")
        time.sleep(uniform(0.0, 0.125))

    print("")


def write_account_info_to_csv(writer, account_number, exemptions, current_amt_due,
                              years_due_str, last_payment_date, suit_type):
    if exemptions != 'None':
        writer.writerow({
            'Account Number': account_number,
            'Current Amt Due': current_amt_due if current_amt_due else 'Data not found.',
            'Current Yrs Due': years_due_str,
            'Last Pymt Date': last_payment_date,
            'Notes': (exemptions if exemptions else '') + (suit_type if suit_type else '')
        })
    else:
        writer.writerow({
            'Account Number': account_number,
            'Current Amt Due': current_amt_due if current_amt_due else 'Data not found.',
            'Current Yrs Due': years_due_str,
            'Last Pymt Date': last_payment_date,
            'Notes': suit_type if suit_type else ''
        })
