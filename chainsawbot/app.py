import sys, asyncio
from scraper import execute_scraper
from calendar_gen import set_events, create_ics

def main():
    asyncio.run(execute_scraper())
    create_ics(set_events())
    return 0

main()