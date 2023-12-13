import asyncio
import aiofiles

async def file_to_char_channel(file_path, char_channel):
    async with aiofiles.open(file_path, mode='r', encoding='utf-8') as file:
        async for line in file:
            for char in line:
                await char_channel.put(char)
    await char_channel.put(None)  # Signal the end of file

async def char_channel_to_string_channel(char_channel, string_channel):
    result = ''
    while True:
        char = await char_channel.get()
        if char is None:
            break  # End of file
        result += char
    await string_channel.put(result)
    await string_channel.put(None)  # Signal the end of string channel

async def main():
    file_path = 'путь_к_вашему_файлу.txt'

    char_channel = asyncio.Queue()
    string_channel = asyncio.Queue()

    task1 = asyncio.create_task(file_to_char_channel(file_path, char_channel))
    task2 = asyncio.create_task(char_channel_to_string_channel(char_channel, string_channel))

    while True:
        result = await string_channel.get()
        if result is None:
            break  # End of string channel
        print(result)

    await asyncio.gather(task1, task2)

if __name__ == "__main__":
    asyncio.run(main())