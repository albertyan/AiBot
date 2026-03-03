from monitor.monitor import monitor
from utils.perf_util import instrument_class

class MonitorService:
    def __init__(self):
        pass

    def start_monitor(self):
        monitor.start()

    def stop_monitor(self):
        monitor.stop()

    def get_monitor_status(self) -> bool:
        return monitor.running

MonitorService = instrument_class(MonitorService, prefix="service.MonitorService")
monitor_service = MonitorService()
