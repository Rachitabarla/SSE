# SSE
This repo is a working demonstration of how Server Sent Events are implemented using Fastapi.

1. Clone the repository
2. Open the terminal and use the command to start the server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5050
```
3. Trigger the /stream endpoint by running its get URL in a separate tab.
4. Use /write API to write data and those events are stream in the stream URL.
