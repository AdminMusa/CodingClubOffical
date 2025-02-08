from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        if self.path == "/signin":
            username = data.get("username")
            password = data.get("password")

            if username == "admin" and password == "password":  # Example authentication
                self.respond({"success": True})
            else:
                self.respond({"success": False, "message": "Invalid credentials"}, 401)

        elif self.path == "/submit":
            username = data.get("username")
            project = data.get("project")

            if username and project:
                self.save_project(username, project)
                self.respond({"success": True, "message": "Project submitted successfully!"})
            else:
                self.respond({"success": False, "message": "Missing fields"}, 400)

        else:
            self.respond({"success": False, "message": "Invalid endpoint"}, 404)

    def save_project(self, username, project):
        """Save submitted projects to a file"""
        try:
            with open("projects.txt", "a") as file:
                file.write(f"{username}: {project}\n")
        except Exception as e:
            print("Error writing to file:", e)

    def respond(self, response_data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode("utf-8"))

server_address = ("", 3000)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

print("Server running on http://localhost:3000")
httpd.serve_forever()
