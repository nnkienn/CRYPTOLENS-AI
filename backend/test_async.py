import asyncio
import httpx
import time

RSS_SOURCES = [
    "https://cointelegraph.com/rss",
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cryptopanic.com/news/rss/"
]

async def fetch_news(client, url):
    start = time.perf_counter()
    print("Starting fetch for:", url)
    try:
        response = await client.get(url, timeout=10)
        end = time.perf_counter()
        print(f"✅ Xong {url} - {len(response.text)} ký tự - Thời gian: {end - start:.2f}s")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
async def main():
    start_total =  time.perf_counter()
    async with httpx.AsyncClient() as client:
        tasks = [fetch_news(client, url) for url in RSS_SOURCES]
        await asyncio.gather(*tasks)
    end_total = time.perf_counter()
    print(f"\n🔥 TỔNG THỜI GIAN CÀO 3 TRANG: {end_total - start_total:.2f} giây")
if __name__ == "__main__":
    asyncio.run(main())