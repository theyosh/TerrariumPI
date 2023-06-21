# This script is used inside docker to make sure the engine is stil running and updating.
# If the motd.sh file not updated for 2 minutes, the engine is stuck, and the docker image is unhealthy.
#
# Usage: HEALTHCHECK --interval=120s --timeout=2s --start-period=120s CMD python contrib/docker_health.py

from pathlib import Path
from datetime import datetime
import os

TIMEOUT = 120
FILE_TO_CHECK = "motd.sh"


def restart_docker():
    restart = Path(".restart")
    if not restart.exists():
        restart.write_text("restart")
        print(f"Restarting unhealty docker {datetime.now()}")
        os.system("bash -c 'kill -s 2 -1 && (sleep 60; kill -s 9 -1)'")


health_file = Path(FILE_TO_CHECK)

if not health_file.exists():
    restart_docker()
    exit(1)

timeout = (datetime.now() - datetime.fromtimestamp(health_file.stat().st_mtime)).total_seconds()
if timeout > TIMEOUT:
    restart_docker()
    exit(1)

print(f"OK {datetime.now()}")
exit(0)
