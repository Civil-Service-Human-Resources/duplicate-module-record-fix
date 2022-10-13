# Delete duplicate module records

The module record table in the learner_record database currently doesn't have uniqueness on module_id and user_id. This can cause errors loading completion status of some courses.

## Running

### Requirements

Requirements for this script can be found in `requirements.txt`

### Environment

The script expects the following environment variables to be set in a `.env` file:
- LEARNER_RECORD_DATABASE_HOST
- LEARNER_RECORD_DATABASE_USER
- LEARNER_RECORD_DATABASE_PW
- LEARNER_RECORD_DATABASE_DATABASE

### Run

The script can be run using the command:

`python main.py`

the command `delete` must be passed as a command-line argument in order for the duplicates to be deleted; the script will simply count if not.