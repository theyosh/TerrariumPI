# This script is used inside docker to make sure the engine is stil running and updating.
# If the motd.sh file not updated for 2 minutes, the engine is stuck, and the docker image is unhealthy.
#
# Usage: HEALTHCHECK --interval=30s --timeout=2s --start-period=120s CMD python contrib/docker_health.py

from pathlib import Path
from datetime import datetime

TIMEOUT=120
FILE_TO_CHECK='motd.sh'

health_file = Path(FILE_TO_CHECK)

if not health_file.exists():
  exit(1)

timeout = (datetime.now() - datetime.fromtimestamp(health_file.stat().st_mtime)).total_seconds()
if timeout > TIMEOUT:
  exit(1)

exit(0)