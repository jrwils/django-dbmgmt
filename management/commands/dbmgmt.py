from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import connection
from os import listdir, path
from optparse import make_option


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
                    make_option(
                        '--all',
                        action='store_true',
                        dest='run_all',
                        ),
                    )

    def handle(self, *args, **options):
        if not hasattr(settings, 'SQL_DIR'):
            raise AttributeError('Please assign a SQL_DIR directory in settings.py')

        run_all = options.get('run_all')

        if run_all is None and len(args) == 0:
            raise ValueError('Please pass a file argument or --all')

        files_rmext = [path.splitext(sqlfile)[0] for sqlfile in listdir(settings.SQL_DIR)]
        ## print a notice if any of the arguments don't exist as files in SQL_DIR
        for arg in args:
            if arg not in files_rmext:
                self.stdout.write('{} file not found in {} - this file will be skipped'.format(arg, settings.SQL_DIR))
        for file in listdir(settings.SQL_DIR):
            file_rmext = path.splitext(file)[0]
            if run_all or file_rmext in args:
                fhandle = open(path.join(settings.SQL_DIR, file))
                sql_txt = fhandle.read()
                cursor = connection.cursor()
                cursor.execute(sql_txt)
                self.stdout.write('Updated {}'.format(file_rmext))
                cursor.close()