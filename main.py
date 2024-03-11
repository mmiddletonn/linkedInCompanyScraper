import os_detection
import linkedin

import time

platform = os_detection.platform
session = linkedin.session(platform)

session.login()

session.wait()

session.search("google")

# session.find_employee()

time.sleep(5)
session.end()