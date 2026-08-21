from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {'greeting': 'Welcome to Waypoint'})

def report(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        return render(request, 'thanks.html', {'reporter_name': name})
    return render(request, 'report.html')

def search(request):
    query = request.GET.get('q', '')
    return render(request, 'search.html', {'query': query})

def catalog(request):
    trails = [
        {'name': 'Eagle Ridge Trail', 'distance': 5.2, 'elevation': 320, 'difficulty': 'moderate', 'is_open': True},
        {'name': 'Bear Mountain Loop', 'distance': 12.5, 'elevation': 850, 'difficulty': 'expert', 'is_open': True},
        {'name': 'Crystal Lake Path', 'distance': 3.1, 'elevation': 120, 'difficulty': 'easy', 'is_open': True},
        {'name': 'Thunder Peak Route', 'distance': 18.3, 'elevation': 1400, 'difficulty': 'expert', 'is_open': False},
        {'name': 'Willow Creek Walk', 'distance': 2.4, 'elevation': 50, 'difficulty': 'easy', 'is_open': True},
        {'name': 'Granite Climb', 'distance': 7.8, 'elevation': 600, 'difficulty': 'hard', 'is_open': False},
    ]
    return render(request, 'catalog.html', {'trails': trails})


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
