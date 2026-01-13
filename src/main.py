from flask import (
    Flask,
    redirect,
    request,
    render_template,
)

from exceptions import (
    NotExistError,
    ShortCodeLeak,
    URLError,
)
from services import url_shortener_service

app = Flask(__name__, template_folder="../templates")


@app.route("/<short_code>/")
def redirect_to_original(short_code: str):
    try:
        original = url_shortener_service.get_original(short_code)
    except NotExistError:
        return "NOT FOUND", 404

    return redirect(original)


@app.route(
    "/",
    methods=(
        "GET",
        "POST",
    ),
)
def home():
    short_url, error = None, None
    if request.method == "POST":
        try:
            short_url = url_shortener_service.shorten(request.form["url"])
        except URLError as e:
            error = str(e)
        except ShortCodeLeak as e:
            error = "DOWN SERVICE"

    return render_template(
        "index.html",
        request=request,
        short_url=short_url,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True)
