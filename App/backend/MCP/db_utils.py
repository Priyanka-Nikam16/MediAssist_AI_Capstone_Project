"""
---------------------------------------------------------
Database Utility Functions
---------------------------------------------------------

Purpose
-------
1. Extract patient_id from user question.
2. Format database records into readable text.
---------------------------------------------------------
"""

import re


def extract_patient_id(question):
    """
    Extract patient id from user question.

    Examples
    --------
    "get lab results of patient 15" -> 15
    "patient history 102" -> 102
    "show payment summary for patient id 7" -> 7

    Returns
    -------
    int | None
    """

    match = re.search(r"\d+", question)

    if match:
        return int(match.group())

    return None


def format_records(records):
    """
    Convert database records into readable text.

    Parameters
    ----------
    records : list of dict

    Returns
    -------
    str
    """

    if not records:
        return "No records found."

    answer = ""

    for index, record in enumerate(records, start=1):

        answer += f"Record {index}\n"
        answer += "-" * 30 + "\n"

        for key, value in record.items():
            answer += f"{key}: {value}\n"

        answer += "\n"

    return answer