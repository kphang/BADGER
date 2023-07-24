#from anyio import create_task_group, run
import anyio
import time
import httpx
import logging

# TODO: build request with headers, body, etc

async def send_request(client, method, url):
    
    if method == "GET":            
        response = await client.get(url)
    elif method == "POST":
        response = await client.post(url)
    
    return response

async def build_requests(client, urls):    
    async with anyio.create_task_group() as tg:        
        for url in urls:            
            tg.start_soon(send_request,client,"GET",url)
    
async def main(n):#urls):
    start_time=time.time()
    # TODO: adjust timeouts, retries, exception handling
    async with httpx.AsyncClient(http2=True) as client:
        await build_requests(client,n)
    logging.info("--- %s seconds ---" % (time.time() - start_time))
     

anyio.run(main)        

async def main():
    urls = ["http://127.0.0.1:9000/limited"]*1000
    responses = await run_requests()#"GET",urls)
    responses = responses.results
    return responses


if __name__=="__main__":
    start_time=time.time()
    # TODO: implement test?
    #urls = ["http://127.0.0.1:9000/limited"]*1000    
    #anyio.run(main())
    anyio.run(run_requests())#, urls)
    #test = run_sync_requests(urls)
    #print(len(test))
    print("--- %s seconds ---" % (time.time() - start_time))
    
asyncio.run(run_requests())#, urls)