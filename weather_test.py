from asyncflows import AsyncFlows


async def main():
    query = input("Input your location ")
    flow = AsyncFlows.from_file("weather_flow.yaml").set_vars(
        query=query,
    )

    # Run the flow and return the default output (result of the blue hat)
    result = await flow.run()
    print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
