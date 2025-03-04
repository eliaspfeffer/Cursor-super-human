from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig
import asyncio
from dotenv import load_dotenv
load_dotenv()

async def main():
    # Konfigurieren Sie den Browser mit dem Pfad zu Ihrer Chrome-Installation
    browser = Browser(
        config=BrowserConfig(
            # Pfad zu Ihrer Chrome-Installation
            chrome_instance_path='/usr/bin/google-chrome',  # Für Linux
            # Fügen Sie hier zusätzliche Chrome-Argumente hinzu, wenn nötig
            # extra_chromium_args=['--profile-directory=Default']  # Optional: Spezifisches Profil verwenden
        )
    )
    
    agent = Agent(
        task="Go and buy the longjevity drink from brian johnson.",
        llm=ChatOpenAI(model="gpt-4o"),
        browser=browser,  # Übergeben Sie die Browser-Instanz an den Agenten
    )
    
    await agent.run()
    await browser.close()  # Schließen Sie den Browser nach der Verwendung

asyncio.run(main())
