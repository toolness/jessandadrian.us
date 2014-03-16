import os
import gspread
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from .importguests import convert_rows_to_dicts, normalize_guest_rowdict
from .googleimportguests import ENV_VAR_DOCS, get_google_client


def find_changed_cells(rsvp, info, cells, mapping):
    changed_cells = []
    for rsvp_attr, info_key in mapping.items():
        if getattr(rsvp, rsvp_attr) != info[info_key]:
            changed_cells.append

class Command(BaseCommand):
    help = 'Reflect RSVP status of guests back to Google spreadsheet.\n' + \
           ENV_VAR_DOCS

    option_list = BaseCommand.option_list + (
        make_option('--dry-run',
            dest='dry_run',
            default=False,
            help='don\'t commit imported data to database',
            action='store_true'
        ),
    )

    def debug(self, msg):
        if self.verbosity > 1: self.stdout.write(msg)

    def handle(self, *args, **options):
        self.verbosity = int(options['verbosity'])

        gc = get_google_client()
        guestlist = gc.open_by_url(os.environ['GUESTLIST_URL']).sheet1
        alphanum = 'A1:' + guestlist.get_addr_int(guestlist.row_count,
                                                  guestlist.col_count)
        self.debug('Retrieving guest list range %s' % alphanum)
        cells = guestlist.range(alphanum)
        rowdicts = convert_rows_to_dicts(guestlist.get_all_values())

        getcell = lambda row, col: cells[(row-1) * guestlist.col_count +
                                         col-1]

        changed_cells = []
        for info in rowdicts:
            normalize_guest_rowdict(info)
            user = User.objects.get(pk=info['id'])
            rsvp = user.rsvp

            if user.username != info['username']:
                self.stderr.write('username mismatch for %s' % user)

            def change_cells(**mapping):
                for rsvp_attr, info_key in mapping.items():
                    value = getattr(rsvp, rsvp_attr)
                    if value != info[info_key]:
                        self.stdout.write('reflecting %s for %s' % (
                            info_key,
                            user
                        ))
                        cell = getcell(info.row, info.colnum(info_key))
                        cell.value = value
                        changed_cells.append(cell)

            change_cells(is_attending='is-attending',
                         song='music-selection',
                         number_of_guests='actual-number-of-guests',
                         passphrase='passphrase')

        if not changed_cells:
            self.stdout.write('No changes need to be reflected.')
        else:
            if options['dry_run']:
                self.stdout.write('Dry run complete.')
            else:
                guestlist.update_cells(changed_cells)
                self.stdout.write('Changes reflected to Google spreadsheet.')
