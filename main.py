import sys
from script import run
from config import LEARNER_RECORD_DATABASE_DATABASE, LEARNER_RECORD_DATABASE_HOST, LEARNER_RECORD_DATABASE_PW, LEARNER_RECORD_DATABASE_USER

args = sys.argv
delete_records = False

if (len(args) > 1):
    delete_records = args[1] == "delete"

print(f"Running with delete records flag set to {delete_records}")

run(LEARNER_RECORD_DATABASE_USER, LEARNER_RECORD_DATABASE_PW, LEARNER_RECORD_DATABASE_HOST, LEARNER_RECORD_DATABASE_DATABASE, delete_records)