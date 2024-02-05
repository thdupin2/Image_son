from django.http import HttpResponse

def hello_world(request):
    content = """
    <html>
        <head>
            <title>Hello World</title>
        </head>
        <body>
            <h1>Hello, World!</h1>
            <form action="/traitement_images/nouvelle_vue/" method="post">
                <input type="submit" value="Cliquez ici" />
            </form>
        </body>
    </html>
    """
    return HttpResponse(content)