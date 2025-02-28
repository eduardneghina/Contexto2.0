import time
import asyncio
from GameController import *

async def main():
    GameControllerObject = GameController()
    await GameControllerObject.start_the_game()
    await GameControllerObject.first_word_insert_to_start()
    time.sleep(20)

if __name__ == "__main__":
    asyncio.run(main())