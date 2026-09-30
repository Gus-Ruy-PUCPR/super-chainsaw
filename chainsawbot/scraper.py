import asyncio, sys
from loguru import logger
from pathlib import Path
from playwright.async_api import async_playwright

import os
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
email = os.getenv("EMAIL_LOGIN")
senha = os.getenv("SENHA_LOGIN")
TAG = "SCRAPER: "

async def login_AVA(page):
        await page.goto("https://pucpr.instructure.com")

        await page.get_by_label("Email, telefone ou Skype").fill(str(email))
        await page.get_by_role("button", name="Avançar").click()

        await page.get_by_label("Senha").fill(senha)
        await page.get_by_role("button", name="Entrar").click()

        await page.get_by_role("button", name="Sim").click()
                
        logger.info(TAG + "Succesfully loged on account -> " + email)

async def go_to_course_assignment(page, course: str):
     await page.goto(course)

async def read_course_assignment(page):
     await page.locator()
            
async def init_scrapper():
    tarefas_totais = {}
    async with async_playwright() as p:
        try: 
            if sys.platform == "win32":
                print(sys.platform)
                browser = await p.chromium.launch(headless=False, channel="chrome")
            else:
                browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

        except NameError:
            print(NameError)
            return NameError

        await login_AVA(page)
        await go_to_course_assignment(page, "https://pucpr.instructure.com/courses/70123/assignments")
