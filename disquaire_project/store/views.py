from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import Album, Artist, Contact, Booking


def index(request):
    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
    formatted_albums = ["<li>{}</li>".format(album.title) for album in albums]

    template = loader.get_template('store/index.html')
    return HttpResponse(template.render(request=request))


def listing(request):
    albums = Album.objects.filter(available=True)
    formatted_albums = ["<li>{}</li>".format(album.title) for album in albums]
    message = """
        <ul>{}</ul>
    """.format("\n".join(formatted_albums))

    return HttpResponse(message)


def detail(request, album_id):
    album = Album.objects.get(pk=album_id)
    artists = " ".join([artist.name for artist in album.artists.all()])
    message = "Le nom de l'album est {}. Il a été écrit par {}".format(
        album.title, artists)
    return HttpResponse(message)


def search(request):
    query = request.GET.get('query')
    if not query:
        albums = Album.objects.all()
        message = "Veuillez entrer un terme de recherche."
    else:
        albums = Album.objects.filter(title__icontains=query)
        if not albums.exists():
            albums = Artist.objects.filter(name__icontains=query)
        if not albums.exists():
            message = "Misère de misère, PAS DE RESULTAT !"
        else:
            formatted_albums = [
                "<li>{}</li>".format(album.title) for album in albums]
            message = """
                Nous avons trouvé les albums correspondant à votre requête ! Les voici :
                <ul>{}</ul>
            """.format("\n".join(formatted_albums))
    return HttpResponse(message)
