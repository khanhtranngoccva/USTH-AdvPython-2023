import os
import time

from .domains.classroom import Classroom

new_classroom = Classroom()
new_classroom.start_manager()
