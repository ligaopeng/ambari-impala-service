from resource_management import *
from impala_base import ImpalaBase


class ImpalaCatalog(ImpalaBase):
    def install(self, env):
        self.install_packages(env)
        self.install_impala(env)
        self.configure(env)

    def configure(self, env):
        self.configure_impala(env)

    def start(self, env):
        self.configure(env)
        cmd = 'service impala-catalog start'
        Execute('echo "Running cmd: ' + cmd + '"')
        Execute(cmd)

    def stop(self, env):
        cmd = 'service impala-catalog stop'
        Execute('echo "Running cmd: ' + cmd + '"')
        Execute(cmd)

    def status(self, env):
        check_process_status("/var/run/impala/catalogd-impala.pid")


if __name__ == "__main__":
    ImpalaCatalog().execute()
