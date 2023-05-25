from django.shortcuts import render

from .models import Album, Artist, Contact, Booking


def index(request):
    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
    context = {'albums': albums}

    return render(request, 'store/index.html', context)


def listing(request):
    albums = Album.objects.filter(available=True)
    context = {'albums': albums}

    return render(request, 'store/listing.html', context)


def detail(request, album_id):
    album = Album.objects.get(pk=album_id)
    artists_name = " ". join([artist.name for artist in album.artists.all()])
    context = {
        'album_title': album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'thumbnail': album.picture
    }
    return render(request, 'store/detail.html', context)


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
            
    title = "Résultats pour la requête %s" % query
    context = {
        'albums': albums,
        'title': title
    }
    return render(request, 'store/search.html', context)
