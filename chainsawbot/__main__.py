import sys, scraper, asyncio

def main():
    asyncio.run(scraper.init_scrapper())
    return 0

if __name__ == "__main__":
    sys.exit(main())