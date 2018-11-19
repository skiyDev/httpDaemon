# code for launch daemon
import daemon
import traceback

from controller import run_service

out = open('/store/log.txt', 'w+', encoding='utf8')
with daemon.DaemonContext(stdout=out) as d:
    try:
        print('service run')
        run_service()
    except Exception as ex:
        print('error')
        print(str(ex))
        print(traceback.format_exc())
        d.terminate()
