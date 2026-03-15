from dotenv import load_dotenv
import hashlib
import hmac
import os
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

load_dotenv()

# Key for GitHub to use for sign requests
# Stored in the .env file
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', '')

class WebhookHandler(BaseHTTPRequestHandler):
	def do_POST(self):
		# Read the incoming request body
		content_length = int(self.headers.get("Content-Length", 0))
		body = self.rfile.read(content_length)

		# Verify the request is actually from GitHub using the secret
		signature = self.headers.get("X-Hub-Signature-256", "")
		expected = "sha256=" + hmac.new(WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest()

		if not hmac.compare_digest(signature, expected):
			# Secret doesn't match so ignore the request
			self.send_response(403)
			self.end_headers()
			self.wfile.write(b"Forbidden")
			print("Rejected: invalid signature")
			return

		# Secret matches so pull latest code and restart bot
		print("Valid webhook received, updating...")
		subprocess.run(["git", "pull"], cwd="/home/pi/Doge-Discord-Bot")
		subprocess.run(["bash", "/home/pi/Doge-Discord-Bot/restart_bot.sh"])

		self.send_response(200)
		self.end_headers()
		self.wfile.write(b"Updated")

	def do_GET(self):
		# Ignore any non-POST requests
		self.send_response(404)
		self.end_headers()

# Start the server on port 9000
server = HTTPServer(("0.0.0.0", 9000), WebhookHandler)
print("Webhook server running on port 9000...")
server.serve_forever()
