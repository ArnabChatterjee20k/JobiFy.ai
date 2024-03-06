import os
from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
import asyncio
from playwright.sync_api import sync_playwright, Playwright
def get_files():
    return os.listdir("./contents/")

def create_file(company_name,content):
    try:
        with open(f"contents/{company_name}.txt","w") as f:
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


def generate_content(company_name,link):
    html = scrape(link)
    content = get_content_from_llm(company_name,html)
    create_file(company_name,content)
