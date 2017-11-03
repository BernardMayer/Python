import http.server
import socketserver

PORT = 8888
ADD = "127.0.0.1"
ADDPORT = (ADD, 8888)

try :
    server = http.server.HTTPServer
    handler = http.server.CGIHTTPRequestHandler
    handler.cgi_directories = ["/cgi-bin"]

    httpd = server(ADDPORT, handler)

    print("Ecoute sur port " + str(PORT))
    httpd.serve_forever()

except KeyboardInterrupt :
    print('^C received, shutting down the web server')
    httpd.socket.close()
