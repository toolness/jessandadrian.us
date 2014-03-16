import os
import gspread
from django.core.management.base import CommandError

from .importguests import ImportGuestListCommand

ENV_VAR_DOCS = """
Required environment variables:

  GOOGLE_SECRET_AUTH should be set to username:password, e.g.
  'foo@gmail.com:mypassword'.

  GUESTLIST_URL should be set to the Google spreadsheet URL for the
  guest list.

  WORDLIST_URL should be set to the Google spreadsheet URL for the word
  list."""

def validate_env_vars():
    if (not 'GOOGLE_SECRET_AUTH' in os.environ or
        len(os.environ['GOOGLE_SECRET_AUTH'].split(':')) != 2):
        raise CommandError('GOOGLE_SECRET_AUTH env var must be '
                           'in "username:password" format.')
    for var in ['GUESTLIST_URL', 'WORDLIST_URL']:
        if (not var in os.environ
            or not os.environ[var].startswith('https://')):
            raise CommandError('%s env var must be a HTTPS URL to a '
                               'Google spreadsheet.' % var)

class Command(ImportGuestListCommand):
    help = 'Import guest list from Google spreadsheets.\n' + ENV_VAR_DOCS

    def get_rows_and_word_list(self, *args, **options):
        validate_env_vars()
        gc = gspread.login(*os.environ['GOOGLE_SECRET_AUTH'].split(':'))
        guestlist = gc.open_by_url(os.environ['GUESTLIST_URL']).sheet1
        wordlist = gc.open_by_url(os.environ['WORDLIST_URL']).sheet1
        return (guestlist.get_all_values(),
                [row[0] for row in wordlist.get_all_values()])
