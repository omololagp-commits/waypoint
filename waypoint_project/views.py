from django.shortcuts import render
from trails.models import Trail

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
    trails = Trail.objects.filter(is_open=True).order_by('distance_km')
    return render(request, 'catalog.html', {'trails': trails})


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

def park_trails(request, park_id):
    park = Park.objects.get(id=park_id)
    trails = Trail.objects.filter(park=park, is_open=True).order_by('distance_km')
    return render(request, 'catalog.html', {'trails': trails})