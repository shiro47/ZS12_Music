from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .ConfigFile import SR_config
from schedule import Scheduler
import threading
import time

time_interval=SR_config().check_request_time_period()
users_ids=[]



def reset_users_requests(user_ids_list):
    for user_id in user_ids_list:
        try:
            user = User.objects.get(pk=user_id)
            user.profile.requests=0
            user.save()
        except ObjectDoesNotExist:
            continue
    return users_ids.clear()


def run_continuously(self, interval=1):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run

Scheduler.run_continuously = run_continuously


def start_scheduler():
    scheduler = Scheduler()
    scheduler.every(int(time_interval)).seconds.do(lambda: reset_users_requests(users_ids))
    scheduler.run_continuously()
    
start_scheduler()