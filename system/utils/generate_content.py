import os
from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
import asyncio
from playwright.sync_api import sync_playwright, Playwright
from system.models.Task import Task
from system.db import db
from flask import current_app
from celery import shared_task
from celery.result import AsyncResult
from celery.signals import task_failure , task_success ,task_postrun , task_prerun

def get_files():
    return os.listdir("system/contents/")

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created successfully.")
    else:
        print(f"Directory '{directory}' already exists.")

def create_file(company_name,content):
    try:
        create_directory_if_not_exists("system/contents")
        with open(f"system/contents/{company_name}.txt","w") as f:
            f.write(content)
        return True
    except Exception as e:
        return False

def scrape(link):
    with sync_playwright() as playwright:
        chromium = playwright.chromium
        browser = chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(link)
        html = page.inner_text(selector="body").encode("utf-8")
        browser.close()
        return html

def get_content_from_llm(company_name,html):
        
        prompt = f"""I am applying for role of sde internship in the company named {company_name}. I have been asked what interests me about the company. I am giving you the details of the company in html format. Write me a proper answer based on the html text and different things present here. I want the answer anyhow. HTML - {html}.Sound less robotic and sound more human and keep it verbose"""

        llm = GoogleGenerativeAI(model="gemini-1.0-pro",google_api_key=os.environ.get("GOOGLE_API_KEY"))
        return llm.invoke(prompt)
@shared_task(ignore_result=False)
def generate_content(company_name,link):
    html = scrape(link)
    content = get_content_from_llm(company_name,html)
    create_file(company_name,content)

@task_prerun.connect
def content_handler(task_id=None,task=None,*args,**kwargs):
    task = AsyncResult(task_id)
    try:
        with current_app.app_context():
            task = Task(task_id=task_id,name=kwargs.get("kwargs").get("company_name"),link=kwargs.get("kwargs").get("link"))
            db.session.add(task)
            db.session.commit()
    except Exception as e:
        print(e)

@task_success.connect
def content_success_handler(result=None,sender=None,*args,**kwargs):
    try:
        task_id = sender.request.id
        with current_app.app_context():
            result = AsyncResult(task_id)
            task = Task.query.filter_by(task_id=task_id).first()
            task.state = True
            db.session.commit()
    except Exception as e:
        print(task_id)
        print(e)