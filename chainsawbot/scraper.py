import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright

import os
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
email = os.getenv("EMAIL_LOGIN")
senha = os.getenv("SENHA_LOGIN")

async def login_AVA():
    async with async_playwright() as p:
        print("Entering try/catch")
        try: 
            if sys.platform == "win32":
                print(sys.platform)
                browser = await p.chromium.launch(headless=False, channel="chrome")
            else:
                browser = await p.chromium.launch(headless=False)

            context = await browser.new_context()
            page = await context.new_page()

            await page.goto("https://pucpr.instructure.com")

            await page.get_by_label("Email, telefone ou Skype").fill(str(email))
            await page.get_by_role("button", name="Avançar").click()

            await page.get_by_label("Senha").fill(senha)
            await page.get_by_role("button", name="Entrar").click()

            await page.get_by_role("button", name="Sim").click()
                    
            print("Login concluído com sucesso!")
            
            await browser.close()

        except NameError:
            print(NameError)

asyncio.run(login_AVA())