import time, asyncio


async def coro1():
    while True:
        await asyncio.sleep(0.9)
        print("Blink")
    
        

async def coro2():
    await asyncio.sleep(4)
    print("Event")
    #asyncio.current_task().cancel()
    asyncio.get_event_loop().stop()
    

print("start")

async def idle(i):
    if i == 3:
        return True
    else:
        return False        

async def main(i):
    print("main is running")
    task = asyncio.create_task(idle(i))
           
    await asyncio.sleep(5) 
    task.cancel()

    
for i in range(1,10):
    asyncio.run(main(i))


#try:
    
#except asyncio.CancelledError:
 #   pass


print("GOOO")




    
