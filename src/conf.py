from src.middlewares import main_middleware

code_success = "200 OK"
code_not_found = "404 NOT FOUND"
header = [("Content-Type", "text/html")]

middlewares = [main_middleware]
