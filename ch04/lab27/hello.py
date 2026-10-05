import asyncio

async def report():
    for item in ["메모 1", "메모 2", "메모 3"]:
        await asyncio.sleep(0.5)
        yield item

async def main():
    async for item in report():
        print("받았습니다:", item)

asyncio.run(main())
