from flask import (
    Flask,
    redirect,
    request,
    render_template,
    render_template_string,
)

from exceptions import (
    NotExistError,
    ShortCodeLeak,
    URLError,
)
from services import url_shortener_service

app = Flask(__name__)

HTML_FORM = """
<!doctype html>
<title>URL Shortener</title>
<form method="post">
  <input type="url" name="url" placeholder="Enter URL" required>
  <input type="submit" value="Shorten">
</form>
{% if short_url %}
<p>Shortened URL: <a href="/{{ short_url }}">{{ request.host_url }}{{ short_url }}</a></p>
{% endif %}
{% if error %}
<p style="color:red;">{{ error }}</p>
{% endif %}
"""


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

    return render_template_string(
        HTML_FORM,
        request=request,
        short_url=short_url,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True)
