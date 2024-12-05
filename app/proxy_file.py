# import http.server
# import socketserver
# import socket
# import urllib.request
# import select
#
# class MyProxy(http.server.SimpleHTTPRequestHandler):
#
#     def do_GET(self):
#         print(self.path)
#         url = self.path
#         try:
#             self.send_response(200)
#             self.end_headers()
#             self.copyfile(urllib.request.urlopen(url), self.wfile)
#         except Exception as e:
#             self.send_error(500, f"Error: {e}")
#
#     def do_POST(self):
#         self._handle_request_with_body("POST")
#
#     def do_DELETE(self):
#         self._handle_request_with_body("DELETE")
#
#     def do_PATCH(self):
#         self._handle_request_with_body("PATCH")
#
#     def do_CONNECT(self):
#         """Handle HTTPS (CONNECT) requests."""
#         try:
#             host, port = self.path.split(":")
#             port = int(port)
#
#             # Create a socket to connect to the target server
#             with socket.create_connection((host, port)) as target_socket:
#                 self.send_response(200, "Connection Established")
#                 self.end_headers()
#
#                 # Relay data between the client and the target server
#                 self._relay_data(self.connection, target_socket)
#         except Exception as e:
#             self.send_error(500, f"Error: {e}")
#
#     def _relay_data(self, client_socket, target_socket):
#         """Relay data between the client and the target server."""
#         client_socket.setblocking(False)
#         target_socket.setblocking(False)
#
#         sockets = [client_socket, target_socket]
#
#         while True:
#             readable, _, exceptional = select.select(sockets, [], sockets)
#             if exceptional:
#                 break
#             for sock in readable:
#                 try:
#                     data = sock.recv(4096)
#                     if not data:
#                         return  # Connection closed
#                     if sock is client_socket:
#                         target_socket.sendall(data)
#                     elif sock is target_socket:
#                         client_socket.sendall(data)
#                 except Exception as e:
#                     print(f"Error during data relay: {e}")
#                     return
#
#     def _handle_request_with_body(self, method):
#         """Generic method to handle HTTP methods with request body (POST, DELETE, PATCH)."""
#         try:
#             url = self.path
#             print(f"{method} {url}")
#
#             # Get the content length and read the request body
#             content_length = int(self.headers.get("Content-Length", 0))
#             body = self.rfile.read(content_length) if content_length > 0 else None
#
#             # Create a request object with the appropriate method and body
#             req = urllib.request.Request(url, data=body, method=method)
#             for header, value in self.headers.items():
#                 if header.lower() not in ["host", "content-length"]:
#                     req.add_header(header, value)
#
#             # Send the request and return the response
#             with urllib.request.urlopen(req) as response:
#                 self.send_response(response.getcode())
#                 for header, value in response.getheaders():
#                     self.send_header(header, value)
#                 self.end_headers()
#                 self.copyfile(response, self.wfile)
#         except Exception as e:
#             self.send_error(500, f"Error: {e}")
#
# # --- main ---
# PORT = 7777
#
# httpd = None
#
# try:
#     socketserver.TCPServer.allow_reuse_address = True  # Allow reusing the same port
#     httpd = socketserver.TCPServer(("", PORT), MyProxy)
#     print(f"Proxy at: http://localhost:{PORT}")
#     httpd.serve_forever()
# except KeyboardInterrupt:
#     print("Pressed Ctrl+C")
# finally:
#     if httpd:
#         httpd.shutdown()


import http.server
import socketserver
import socket
import select


class MyProxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_error(400, "Bad request: direct GET not supported for HTTPS")

    def do_POST(self):
        self.send_error(400, "Bad request: direct POST not supported for HTTPS")

    def do_CONNECT(self):
        """Handle HTTPS CONNECT requests to establish a tunnel."""
        try:
            host, port = self.path.split(":")
            port = int(port)

            with socket.create_connection((host, port)) as target_socket:
                self.send_response(200, "Connection Established")
                self.end_headers()

                # Relay data between client and server
                self._relay_data(self.connection, target_socket)
        except Exception as e:
            self.send_error(500, f"Error during CONNECT: {e}")

    def _relay_data(self, client_socket, target_socket):
        """Relay data between the client and target server."""
        try:
            sockets = [client_socket, target_socket]
            while True:
                readable, _, exceptional = select.select(sockets, [], sockets)
                if exceptional:
                    break
                for sock in readable:
                    data = sock.recv(4096)
                    if data:
                        if sock is client_socket:
                            target_socket.sendall(data)
                        else:
                            client_socket.sendall(data)
                    else:
                        return  # Connection closed by peer
        except Exception as e:
            print(f"Relay error: {e}")


# Main
PORT = 7777

httpd = None
try:
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("", PORT), MyProxy)
    print(f"HTTPS Proxy running at http://localhost:{PORT}")
    httpd.serve_forever()
except KeyboardInterrupt:
    print("Server interrupted")
finally:
    if httpd:
        httpd.shutdown()
