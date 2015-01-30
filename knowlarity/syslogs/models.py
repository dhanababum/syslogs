import mongoengine as mongo
import datetime
import time


def convert_date_int(date):
    '''
      datetime object to number
      parms: date object
    '''
    t1 = date.timetuple()
    return time.mktime(t1)


class SysLog(mongo.Document):
    """
       Complete system messages with programmes
    """
    programme = mongo.StringField()
    msg = mongo.StringField()
    logged = mongo.DateTimeField()

    def create_log(self, programme, msg, logged):
        FORMATE = "%Y %b %d %H:%M:%S"
        self.programme = programme
        self.msg = msg
        logged = "%s %s" % (datetime.datetime.now().year,
                            logged)
        self.logged = datetime.datetime.strptime(logged, FORMATE)
        self.save()


class Occurence(mongo.Document):
    """
        Programme Count
    """
    programme = mongo.StringField(unique=True)
    occured = mongo.IntField(default=0)
    created_date = mongo.IntField()
    updated_date = mongo.IntField()

    def create_log(self):
        self.occured += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = convert_date_int(datetime.datetime.now())
        self.updated_date = convert_date_int(datetime.datetime.now())
        return super(Occurence, self).save(*args, **kwargs)
