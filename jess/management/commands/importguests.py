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

def convert_rows_to_dicts(rows):
    column_names = None
    dicts = []
    for i, row in enumerate(rows):
        if i == 0:
            # Column headers.
            column_names = tuple([slugify(unicode(val)) for val in row])
        else:
            # An actual row with information about a guest.
            info = {'row': i + 1}
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
                user_id = int(info['id'])
                last_name = info['last-name']
                num_guests = int(info['actual-number-of-guests'] or 0)
                is_attending = bool(info['is-attending'])
                music_selection = info['music-selection']
                passphrase = info['passphrase']
                is_admin = bool(info['is-admin'])
                email = info['email']
                username = info['username'] or slugify(u'%s %s' % (first_name, last_name))

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
                if not rsvp.passphrase:
                    rsvp.passphrase = self.generate_passphrase(word_list)
                    self.stdout.write('new passphrase for %s: %s' % (
                        first_name,
                        rsvp.passphrase
                    ))

                user.first_name = first_name
                user.last_name = last_name
                user.is_active = True
                user.is_staff = user.is_superuser = is_admin
                user.email = email
                user.save()

                rsvp.is_attending = is_attending
                rsvp.song = music_selection
                rsvp.number_of_guests = num_guests
                rsvp.save()
            except Exception:
                self.stderr.write('Error importing row '
                                  '%d (%s)' % (info['row'], first_name))
                raise

    def handle(self, *args, **options):
        rows, word_list = self.get_rows_and_word_list(*args, **options)

        try:
            with transaction.atomic():
                self.import_rows(rows, word_list)
                if options['dry_run']: raise DryRunFinished()
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
