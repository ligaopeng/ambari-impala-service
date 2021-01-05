from resource_management import *
from impala_base import ImpalaBase


class StateStore(ImpalaBase):
    def install(self, env):
        self.install_packages(env)
        self.install_impala(env)
        Execute("yum -y install python-devel openssl-devel python-pip cyrus-sasl cyrus-sasl-gssapi cyrus-sasl-devel")
        self.configure(env)

    def configure(self, env):
        self.configure_impala(env)

    def start(self, env):
        self.configure(env)
        cmd = 'service impala-state-store start'
        Execute('echo "Running cmd: ' + cmd + '"')
        Execute(cmd)

    def stop(self, env):
        cmd = 'service impala-state-store stop'
        Execute('echo "Running cmd: ' + cmd + '"')
        Execute(cmd)

    @staticmethod
    def status():
        check_process_status("/var/run/impala/statestored-impala.pid")


if __name__ == "__main__":
    StateStore().execute()
