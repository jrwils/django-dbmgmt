from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import connection
from os import listdir, path


class Command(BaseCommand):

    def handle(self, *args, **options):
        files_rmext = [path.splitext(sqlfile)[0] for sqlfile in listdir(settings.SQL_DIR)]
        ## print a notice if any of the arguments don't exist as files in SQL_DIR
        for arg in args:
            if arg not in files_rmext:
                self.stdout.write('{} file not found in {} - this file will be skipped'.format(arg, settings.SQL_DIR))
        for file in listdir(settings.SQL_DIR):
            file_rmext = path.splitext(file)[0]
            if not args or file_rmext in args:
                fhandle = open(path.join(settings.SQL_DIR, file))
                sql_txt = fhandle.read()
                cursor = connection.cursor()
                cursor.execute(sql_txt)
                self.stdout.write('Updated {}'.format(file_rmext))