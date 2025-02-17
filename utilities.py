import google.generativeai as genai


def read_email_data(path):
    with open(path, "r") as document:
        row = document.readlines()
        to_email = row[0].strip()
        subject = row[1].strip()
        content = "".join(row[2:]).strip()
    return to_email, subject, content
