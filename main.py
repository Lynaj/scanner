import settings

from models.upwork_user import UpWorkUserRecord
from scanner import UpWorkScanner

def start():
    # Parse the user data & scan it account
    account_list = UpWorkUserRecord.parse_accounts_from_the_file(settings.account_data_path)

    for account in account_list:
        try:
            scanner = UpWorkScanner(upwork_account=account, headless=True)
            scanner.authenticate()
        except Exception as e:
            print(str(e))

if __name__ == '__main__':
    start()