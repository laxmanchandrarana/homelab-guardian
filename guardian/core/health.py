import psutil
import shutil


class Health:

    def cpu(self):
        return psutil.cpu_percent(interval=1)

    def memory(self):
        return psutil.virtual_memory()._asdict()

    def disk(self):
        usage = shutil.disk_usage("/")
        return {
            "total": usage.total,
            "used": usage.used,
            "free": usage.free
        }

    def network(self):
        return psutil.net_io_counters()._asdict()

    def boot_time(self):
        return psutil.boot_time()
