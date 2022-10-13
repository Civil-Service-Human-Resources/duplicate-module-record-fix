from dotenv import load_dotenv
import os

print("Loading environment variables...")
load_dotenv()

LEARNER_RECORD_DATABASE_HOST=os.getenv("LEARNER_RECORD_DATABASE_HOST")
LEARNER_RECORD_DATABASE_USER=os.getenv("LEARNER_RECORD_DATABASE_USER")
LEARNER_RECORD_DATABASE_PW=os.getenv("LEARNER_RECORD_DATABASE_PW")
LEARNER_RECORD_DATABASE_DATABASE=os.getenv("LEARNER_RECORD_DATABASE_DATABASE")