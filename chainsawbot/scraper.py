import asyncio, sys
from loguru import logger
from pathlib import Path
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

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

        await page.get_by_label("Senha").fill(str(senha))
        await page.get_by_role("button", name="Entrar").click()

        await page.get_by_role("button", name="Sim").click()
                
        logger.info(TAG + "Succesfully loged on account -> " + email)

async def go_to_course_assignment(page, course: str):
     await page.goto(course)
     logger.info(TAG + "Succesfully resdirecto to -> " + course)

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
        await page.get_by_role("tab", name="Painel de controle").click()

        await page.wait_for_load_state("networkidle")

        # carregar os dados da página em soup
        page_content = await page.content()
        soup = BeautifulSoup(page_content)

        # retirar dados inuteis como scripts e styles
        for entity in soup(["script", "style"]):
             entity.extract()

        # pega o texto
        text = soup.get_text()
        # quebra em linhas
        lines = (line.strip() for line in text.splitlines())
        # quebra multiplas linhas em uma
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # retira linhas vazias
        text = '\n'.join(chunk for chunk in chunks if chunk)

        print(text.encode("utf-8"))

