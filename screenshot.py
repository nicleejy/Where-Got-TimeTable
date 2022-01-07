import asyncio
from pyppeteer import launch
from datetime import datetime


loop = asyncio.get_event_loop()

def get_screenshot(url):
    file_path = f'static/My Timetable.png'
    async def main():
        browser = await launch(handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False)
        page = await browser.newPage()
        await page.setViewport({'width': 1200, 'height': 1000})
        await page.goto(url)
        await page.waitFor(3000)
        await page.screenshot({'path': file_path, 'clip': {'x': 150, 'y': 140, 'width': 1060, 'height': 700}})
        await browser.close()
    loop.run_until_complete(main())
    return ".." + file_path