import gkeepapi
import http.server
import socketserver
import os

class handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print("Recieved GET")

        # Sending an '200 OK' response
        self.send_response(200)

        # Setting the header
        self.send_header("Content-type", "text/html")

        # Whenever using 'send_header', you also have to call 'end_headers'
        self.end_headers()

        print("Calling Google API")
        keep = gkeepapi.Keep()
        success = keep.login(os.getenv("sync_username"), os.getenv("sync_password"))
        print(success)

        #note = keep.createNote('Todo', 'Eat breakfast')
        #note.pinned = True
        #note.color = gkeepapi.node.ColorValue.Red
        #keep.sync()

        note = keep.get("1b3CkvjF0IZ2VnIXTIsaKVzOfg2e1JUo7Qsrbc3ivVXae5ikmxOpIO12rsS2XpA")

        unchecked = ""
        checked = ""
        for item in note.items:
            if item.checked:
                if len(checked) > 0:
                    checked += ","
                checked += item.text
            else:
                if len(unchecked) > 0:
                    unchecked += ","
                unchecked += item.text
                
        self.wfile.write(bytes(unchecked + "|" + checked + "|", "utf8"))

        return

handler_object = handler

PORT = 8000
print("Starting HTTP server")
my_server = socketserver.TCPServer((os.getenv("sync_host_ip"), PORT), handler_object)
my_server.serve_forever()



