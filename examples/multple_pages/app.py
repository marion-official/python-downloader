from flask import Flask, render_template_string

app = Flask(__name__)

# Sample Lorem Ipsum text
lorem_ipsum = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus lacinia odio vitae vestibulum
vestibulum. Cras venenatis euismod malesuada. Curabitur vehicula tellus non tellus aliquam,
vel faucibus massa sagittis. Aenean ut efficitur ante. Donec bibendum, eros quis luctus dictum,
arcu mauris dictum est, eget scelerisque erat urna ut est. Integer volutpat eros eu nisl
hendrerit, ut dapibus elit egestas. Vivamus gravida convallis tincidunt.
"""

# Create the template for the page with some basic styling
page_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body {
            font-family: 'Georgia', serif;
            line-height: 1.6;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f7f7f7;
            color: #333;
        }
        h1 {
            text-align: center;
            font-size: 24px;
            margin-bottom: 40px;
        }
        p {
            text-align: justify;
        }
        .nav {
            display: flex;
            justify-content: space-between;
            margin-top: 40px;
        }
        .nav a {
            text-decoration: none;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border-radius: 5px;
            font-size: 18px;
        }
        .nav a[disabled] {
            background-color: #ccc;
            pointer-events: none;
        }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>
    <p>{{ text }}</p>
    <div class="nav">
        <a href="{{ prev_link }}" {% if prev_link == '#' %}disabled{% endif %}>Previous</a>
        <a href="{{ next_link }}" {% if next_link == '#' %}disabled{% endif %}>Next</a>
    </div>
</body>
</html>
"""


@app.route('/page/<int:page_num>')
def book_page(page_num):
    # Handle page boundaries
    if page_num < 0:
        page_num = 0
    elif page_num > 100:
        page_num = 100

    # Set the title based on the page number
    if page_num == 0:
        title = "Index"
        prev_link = "#"
    else:
        title = f"Title of Page {page_num}"
        prev_link = f"/page/{page_num - 1}"

    # Handle next link
    if page_num == 100:
        next_link = "#"
    else:
        next_link = f"/page/{page_num + 1}"

    # Use the same lorem ipsum text for all pages for demonstration
    text = lorem_ipsum

    # Render the page
    return render_template_string(page_template, title=title, text=text, prev_link=prev_link, next_link=next_link)


@app.route('/')
def index():
    # Redirect to the first page of the book
    return book_page(0)


if __name__ == '__main__':
    app.run(debug=True)
