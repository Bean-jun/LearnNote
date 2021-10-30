from django.template import Library
from apps.blog.models import Song

register = Library()


@register.inclusion_tag('inclusion/netease_music.html')
def netease_music(request):
    song = Song.objects.filter(user=request.user, is_play=True).first()
    # flag = random.randint(0, 1)

    # return {'song': song, 'flag': flag}
    return {'song': song}
