#!/usr/bin/env python3

import aiohttp
from aiohttp import web
import asyncio
import random

class RequestCounter:
    def __init__(self):
        self._count = 0
        self._lock = asyncio.Lock()

    async def increment(self):
        async with self._lock:
            self._count += 1

    async def decrement(self):
        async with self._lock:
            self._count -= 1

    async def get_count(self):
        async with self._lock:
            return self._count

async def handle(request):
    
    await request.app['counter'].increment()
    
    # Simulate processing time
    await asyncio.sleep(random.uniform(0.5, 1.5))

    # get status
    count = await request.app['counter'].get_count()
    print(count)

    # Decrement the request count when processing is complete
    await request.app['counter'].decrement()

    return web.Response(text="Hello, World!")

async def status(request):
    # Get the current request count
    count = await request.app['counter'].get_count()
    return web.Response(text=f"Currently processing {count} requests.")

async def on_startup(app):
    # Initialize the request counter on server startup
    app['counter'] = RequestCounter()

async def on_cleanup(app):
    # Clean up resources on server shutdown
    del app['counter']

app = web.Application()
app.router.add_get('/', handle)
app.router.add_get('/status', status)

app.on_startup.append(on_startup)
app.on_cleanup.append(on_cleanup)

if __name__ == '__main__':
    web.run_app(app, port=5052)
