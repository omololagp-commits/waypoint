from django.shortcuts import render


def home(request):
    """Homepage with a greeting."""
    return render(request, "home.html", {"greeting": "Welcome to Waypoint"})


def report(request):
    """Trail report form. GET shows blank form; POST shows thank-you."""
    if request.method == "POST":
        name = request.POST.get("name", "Hiker")
        return render(request, "thanks.html", {"reporter_name": name})
    return render(request, "report.html")


def search(request):
    """Safe search that reads query string."""
    query = request.GET.get("q", "")
    return render(request, "search.html", {"query": query})