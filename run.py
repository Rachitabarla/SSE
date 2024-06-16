import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

app = FastAPI(title= "Server Sent Events", description = " Implementation of SSE using async queue", docs_url='/docs')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

client_queue = {} # keeps track of the multiple client connections

@app.post('/write',tags=["Endpoints"])
async def adding_new_line(new_data: str):
    for each_queue in client_queue.values():
        await each_queue.put(f"{new_data}")
    return {"message":"new line added"}
  
@app.get('/stream',tags=["Endpoints"]) 
async def message_stream(request: Request):
    queue = asyncio.Queue()
    client_id = id(queue)
    client_queue[client_id] = queue

    async def event_generator():
        try:
          while True:
              # If client closes connection, stop sending events
              if await request.is_disconnected():
                  break
              try:
                  event = await queue.get()
                  yield event
              except asyncio.CancelledError:
                  break
        finally: client_queue.pop(client_id)

    return EventSourceResponse(event_generator())
