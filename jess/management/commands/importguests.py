import csv
import datetime
import random
from optparse import make_option
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import transaction
from django.utils.text import slugify

from jess.models import RSVP

class DryRunFinished(Exception):
    pass

class RowDict(dict):
    def __init__(self, row, column_names, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.row = row
        self.column_names = column_names

    def colnum(self, column_name):
        return self.column_names.index(column_name) + 1

def normalize_guest_rowdict(info):
    COERCIONS = {
        'id': int,
        'actual-number-of-guests': int,
        'is-attending': bool,
        'is-admin': bool,
    }
    if not info['actual-number-of-guests']:
        info['actual-number-of-guests'] = '0'
    for key, coercer in COERCIONS.items():
        info[key] = coercer(info[key])
    if not info['username']:
        info['username'] = slugify(u'%(first-name)s %(last-name)s' % info)
    return info

def convert_rows_to_dicts(rows):
    column_names = None
    dicts = []
    for i, row in enumerate(rows):
        if i == 0:
            # Column headers.
            column_names = tuple([slugify(unicode(val)) for val in row])
        else:
            # An actual row with information about a guest.
            info = RowDict(row=i + 1, column_names=column_names)
            for colnum, val in enumerate(row):
                colname = column_names[colnum]
                if colname:
                    info[colname] = val.strip()
            dicts.append(info)
    return dicts

class ImportGuestListCommand(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--dry-run',
            dest='dry_run',
            default=False,
            help='don\'t commit imported data to database',
            action='store_true'
        ),
    )

    def generate_passphrase(self, word_list, num_words=3):
        while True:
            words = [random.choice(word_list) for i in range(num_words)]
            phrase = slugify(u'-'.join(words))
            try:
                rsvp = RSVP.objects.get(passphrase=phrase)
            except ObjectDoesNotExist:
                return phrase

    def get_rows(self, *args, **options):
        raise NotImplementedError()

    def import_rows(self, rows, word_list):
        for info in convert_rows_to_dicts(rows):
            first_name = info['first-name']
            try:
                normalize_guest_rowdict(info)
                user_id = info['id']
                last_name = info['last-name']
                num_guests = info['actual-number-of-guests']
                is_attending = info['is-attending']
                music_selection = info['music-selection']
                passphrase = info['passphrase']
                is_admin = info['is-admin']
                email = info['email']
                username = info['username']

                try:
                    user = User.objects.get(pk=user_id)
                except ObjectDoesNotExist:
                    user = User(pk=user_id, username=username)
                    user.set_unusable_password()
                    user.save()

                try:
                    rsvp = user.rsvp
                except ObjectDoesNotExist:
                    rsvp = RSVP(user=user)
                if not passphrase:
                    passphrase = self.generate_passphrase(word_list)
                    self.stdout.write('new passphrase for %s: %s' % (
                        first_name,
                        passphrase
                    ))

                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.is_active = True
                user.is_staff = user.is_superuser = is_admin
                user.email = email
                user.save()

                rsvp.is_attending = is_attending
                rsvp.song = music_selection
                rsvp.number_of_guests = num_guests
                rsvp.passphrase = passphrase
                rsvp.save()
            except Exception:
                self.stderr.write('Error importing row '
                                  '%d (%s)' % (info.row, first_name))
                raise

    def handle(self, *args, **options):
        rows, word_list = self.get_rows_and_word_list(*args, **options)

        try:
            with transaction.atomic():
                self.import_rows(rows, word_list)
                if options['dry_run']: raise DryRunFinished()
            self.stdout.write("Import complete.")
        except DryRunFinished:
            self.stdout.write("Dry run complete.")

class Command(ImportGuestListCommand):
    help = 'Import guest list from a CSV file.'
    args = '<guest-list-filename> <word-list-filename>'

    def get_rows_and_word_list(self, *args, **options):
        if len(args) != 2:
            raise CommandError('Please specify two CSV filenames.')
        rows = [row for row in csv.reader(open(args[0], 'rb'))]
        word_list = [row[0] for row in csv.reader(open(args[1], 'rb'))]
        return rows, word_list
