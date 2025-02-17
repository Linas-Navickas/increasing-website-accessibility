import os
import logging

from bs4 import BeautifulSoup
import requests
import google.generativeai as genai
from dotenv import load_dotenv

from gmail_client import GmailClient
from utilities import read_email_data
from scraper import Scraper
from llm_client import LLM_Client
from db import DataBase
from prompts import PROMPT_SEO, PROMPT_WORD
from db_queries import (
    ANTRASCIU_STRUKTURA_CREATE_QUERY, 
    TEKSTO_KOREKCIJOS_REKOMENDACIJOS_CREATE_QUERY, 
    INSERT_INTO_ANTRASCIU_STRUKTURA_QUERY, 
    INSERT_INTO_TEKSTO_KOREKCIJOS
    )

load_dotenv("./api_key.env")
gmail_client = GmailClient()
db = DataBase()
web_scraper = Scraper()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
MODEL = genai.GenerativeModel("gemini-1.5-flash-8b")
llm = LLM_Client(model=MODEL)


URL = "https://15min.lt/"  
ROBOTS_TXT = URL + "robots.txt"
PATH_TO_EMAIL_TEMPLATE = "./mail_duomenys.txt"


db.execute_query("heading_database.db", ANTRASCIU_STRUKTURA_CREATE_QUERY)
db.execute_query("webpage_database.db", TEKSTO_KOREKCIJOS_REKOMENDACIJOS_CREATE_QUERY)


url_response_robots = requests.get(ROBOTS_TXT)
web_scraper.file_exist(response=url_response_robots, file_name="robots.txt")

url_response = requests.get(URL)
url_soup = BeautifulSoup(url_response.text, "html.parser")

url_antrastes = url_soup.find_all("h1")
description, keywords = web_scraper.extract_meta(url_soup)
headings_info = web_scraper.extract_headings_and_content(url_response.text)

seo_llm_response = MODEL.generate_content(PROMPT_SEO.format(text=headings_info))
heading_text_list = llm.clean_text_list(
    text=seo_llm_response.text, prompt=(PROMPT_SEO.format(text=headings_info))
)

url_text = url_soup.get_text()

clean_text = " ".join(url_text.split())

word_llm_response = MODEL.generate_content(PROMPT_WORD.format(text=clean_text))
corection_text_list = llm.clean_text_list(
    text=word_llm_response.text, prompt=(PROMPT_WORD.format(text=clean_text))
)

if corection_text_list and heading_text_list:
    for text in heading_text_list:
        query = INSERT_INTO_ANTRASCIU_STRUKTURA_QUERY.format(
            heading=text["heading"], suggestion=text["your_suggestion"]
        )
        db.execute_query(database="heading_database.db", query=query)

    for text in corection_text_list:
        query = INSERT_INTO_TEKSTO_KOREKCIJOS.format(
            original_word=text.get("original_word", "").replace("'", ""),
            suggested_correction=text.get("suggested_correction", "").replace("'", ""),
            reasoning=text.get("reasoning", "").replace("'", ""),
        )
        db.execute_query(database="webpage_database.db", query=query)
else:
    logging.warning("Not written to the DB")

to_email, subject, content = read_email_data(PATH_TO_EMAIL_TEMPLATE)
gmail_client.send_email(to_email, subject, content)
logging.warning(
    """
    Work completed:
    - Web page read
    - Data uploaded to the database
    - Email sent
"""
)
