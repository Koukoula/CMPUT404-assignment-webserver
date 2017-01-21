#  coding: utf-8
import SocketServer, os, mimetypes

# Copyright 2017 Panayioti Koukoulas, Noah Shillington

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2017 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
# https://docs.python.org/2/library/mimetypes.html
# https://docs.python.org/2/library/os.html

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2017 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    directory = os.path.abspath('./www')
    index = 'index.html'

    status = "HTTP/1.1 200 OK\r\n"
    fileText = ''
    contentType = ''

    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.dataArray = self.data.split()
        print ("Got a request of: %s\n" % self.data)

        # Either 'GET' or 405
    	if self.dataArray[0] == 'GET':
            self.handleGet()
        else:
            # Return a status code of “405 Method Not Allowed” for any method you cannot handle (POST/PUT/DELETE)
            self.status = "HTTP/1.1 405 Method Not Allowed\r\n"
            self.fileText = "405 Method Not Allowed\n"
        self.request.sendall(self.status + self.contentType+ '\r\n' + self.fileText)

    def handleGet(self):

        path = self.directory + self.dataArray[1]
        if self.dataArray[1][-1] == '/':
            path += self.index

        path = os.path.realpath(path)

        if os.path.exists(path) and path.startswith(self.directory):
            mime = mimetypes.guess_type(path)
            self.contentType = "Content-Type: " + mime[0] + '\r\n'
            self.fileText = open(path).read()

        else:
            self.status = "HTTP/1.1 404 Not Found\r\n"
            self.fileText = "404 Not Found\n"


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
