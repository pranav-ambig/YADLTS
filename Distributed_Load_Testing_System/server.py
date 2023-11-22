#!/usr/bin/env python3

import _socket
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from concurrent.futures import ThreadPoolExecutor
from typing import Any
from random import randint

# Define the number of simultaneous requests to handle
MAX_SIMULTANEOUS_REQUESTS = 5

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class RequestHandler(SimpleHTTPRequestHandler):

    processed = 0

    def log_message(self, format: str, *args: Any) -> None:
        pass

    def do_GET(self):
        with ThreadPoolExecutor(max_workers=MAX_SIMULTANEOUS_REQUESTS) as executor:
            executor.submit(self.process_request, self)

    def process_request(self, handler):
        # Simulate processing time
        import time
        time.sleep(randint(5, 25)/10)  # Simulate processing time of 1 second
        RequestHandler.processed += 1
        print(RequestHandler.processed)

        # Send the response
        handler.send_response(200)
        handler.end_headers()
        handler.wfile.write(b'Hello, World!')

if __name__ == '__main__':
    server_address = 'localhost', 5052
    httpd = ThreadedHTTPServer(server_address, RequestHandler)
    print('Server started on port 5052...')
    httpd.serve_forever()
