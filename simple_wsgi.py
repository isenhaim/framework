from src.render import render


def application(environ, start_response):
    start_response(
        "200 OK",
    )

    return [render("index.html").encode("utf-8")]
