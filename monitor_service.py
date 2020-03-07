import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time
import logging
import sys
import os
#from MonitorManager import MetaMonitor

# pathexe = r"serviceweb.exe"
logging.basicConfig(
    filename='test-service.log',
    level=logging.DEBUG,
    format='[helloworld-service] %(levelname)-7.7s %(message)s'
)


class TestService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'TestService'
    _svc_display_name_ = 'TestService'
    # data_dir = os.path.join('', '')
    # output_dir = os.path.join('cwd-1', 'output')
    # metadata_file_path = os.path.join(output_dir, 'metadata')
    # fList_json = output_dir + 'fList.json'


    def __init__(self, args):
        logging.info(args)
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        logging.info('Stopping service ...')
        self.stop_requested = True

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()

    def main(self):
        logging.info(os.getcwd())

        # Simulate a main loop
        while not self.stop_requested:
            logging.info(os.getcwd())

            main_pkg_dir = os.path.dirname(os.path.realpath(__file__))
            output_dir = os.path.join(main_pkg_dir, "output")

            logging.info(main_pkg_dir)

            # monitor = MetaMonitor(self._metadata_file_path, self._fList_json, self._data_dir)
            # monitor.scanMetaFile()
            time.sleep(10)
            # subprocess.Popen([pathexe])


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(TestService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(TestService)
