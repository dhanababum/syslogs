from django.core.management.base import BaseCommand
from django.conf import settings

from syslogs.models import SysLog, Occurence


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            import cPickle as pickle
        except:
            import pickle
        try:
            input = open('%s/file_seeker.pkl' % settings.BASE_DIR, 'rb')
            FILE_SEEK = pickle.load(input)
            input.close()
        except:
            FILE_SEEK = 0
        self.stdout.write("%s" % settings.BASE_DIR)
        with open("/var/log/syslog", "r") as f:
            f.seek(FILE_SEEK)
            for line in f:
                line_list = line.split(" ")
                logged = " ".join(line_list[:3])
                programme = line_list[4].replace(":", "")
                msg = " ".join(line_list[5:])
                system_logger = SysLog()
                system_logger.create_log(programme, msg, logged)
                check_programme = Occurence.objects.filter(programme=programme)
                if not check_programme:
                    occured = Occurence(programme=programme)
                else:
                    occured = check_programme[0]
                occured.create_log()
            with open('%s/file_seeker.pkl' % settings.BASE_DIR, 'wb') as \
                    output:
                FILE_SEEK = f.tell()
                pickle.dump(FILE_SEEK, output, pickle.HIGHEST_PROTOCOL)
