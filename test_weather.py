import httpx
import asyncio

async def test():
    key = "f7c8fdf460fc4867dae01a9132d66522"
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Sivas,TR&appid={f7c8fdf460fc4867dae01a9132d66522}&units=metric&lang=tr"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        print("Status:", r.status_code)
        print("Cevap:", r.json())

asyncio.run(test())
