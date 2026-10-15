import asyncio, sys
from loguru import logger
from pathlib import Path
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

import os
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
email = os.getenv("EMAIL_LOGIN")
senha = os.getenv("SENHA_LOGIN")
TAG = "SCRAPER: "

# Usa as variaveis em .env para abrir uma pagina no ava da pucpr e logar.
async def login_AVA(page):
        await page.goto("https://pucpr.instructure.com")

        await page.get_by_label("Email, telefone ou Skype").fill(str(email))
        await page.get_by_role("button", name="Avançar").click()

        await page.get_by_label("Senha").fill(str(senha))
        await page.get_by_role("button", name="Entrar").click()

        await page.get_by_role("button", name="Sim").click()
                
        logger.info(TAG + "Succesfully loged on account -> " + email)

# função genérica para mover entre paginas com logs
async def go_to_course_assignment(page, course: str):
     await page.goto(course)
     logger.info(TAG + "Succesfully resdirecto to -> " + course)

# função genérica para retornar o link atual da página
async def read_course_assignment(page):
     return await page.locator()

# função inicial do módulo scrpper.py, será chamada em __main__.py para iniciar a sequência de execução da aplicação 
async def init_scrapper():
    tasks_list = []
    async with async_playwright() as p:
        try: 
            # identificar sistema atual
            if sys.platform == "win32":
                browser = await p.chromium.launch(headless=True, channel="chrome")
            else:
                browser = await p.chromium.launch(headless=False)
                
            logger.info(TAG + f"Plataform: {sys.platform}")
            context = await browser.new_context()
            page = await context.new_page()

        except NameError:
            logger.error(TAG + NameError)
            return NameError

        await login_AVA(page)
        await page.get_by_role("tab", name="Painel de controle").click()

        await page.wait_for_load_state("networkidle")

        # carregar os dados da página em soup
        page_content = await page.content()
        soup = BeautifulSoup(page_content, 'html.parser')

        # retirar dados inuteis como scripts e styles
        for entity in soup(["script", "style"]):
             entity.extract()
        
        itens_trabalho = soup.find_all('li', {'data-cid': 'ListItem'})
        
        for itens in itens_trabalho:
            span_group = itens.find("span", {'role': 'group'})
            if not span_group:
                continue    
            
            activity_name = span_group.get('arial-label')
            
            # Se não achar no aria-label, tenta buscar pelo link da atividade
            if not activity_name:
                logger.warning(TAG + f"Could not find activity_name by arial-label. Trying by link.")
                link_ativ = itens.find('a', {'data-testid': lambda x: x and 'course-work-item-link-' in x})
                activity_name = link_ativ.get_text(strip=True) if link_ativ else "not-found"
                logger.info(TAG + f"Found activity name by link, name: {activity_name}")

            # Nome do Curso
            curso_span = itens.find('span', class_=lambda x: x and 'svtni9-text' in x)
            course_name = curso_span.get_text(strip=True) if curso_span else "not-found"

            # Data de Entrega (geralmente no final do item, ex: "Amanhã 23:59" ou uma data formatada)
            # Procuramos o elemento de texto que exibe o prazo
            data_span = itens.find('span', class_=lambda x: x and '152y9kz-text' in x)
            date = data_span.get_text(strip=True) if data_span else "not-found"
            
            # "Amanhã" não é uma data válida, então formatamos em dia/mês/ano hora:minuto
            if 'Amanhã' in date:
                try:
                    now = datetime.now()
                    logger.info(TAG + str(now))
                    tomorrow = now + timedelta(days=1, hours=23, minutes=59)
                    logger.info(TAG + str(tomorrow))
                    date = tomorrow.strftime("%d/%m/%Y %H:%M")
                    logger.info(TAG + f"Date formated succesfully to: {date}")
                    
                except(NameError):
                    logger.error(TAG + NameError)

            if activity_name != 'not-found':
                task = {
                    'date': date,
                    'course_name': course_name,
                    'activity_name': activity_name
                }
                if task not in tasks_list:
                    tasks_list.append(task)
            
            for task in tasks_list:
                logger.debug(f"[{task['date']}] {task['course_name']} - {task['activity_name']}")
