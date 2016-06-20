from django.core.management.base import BaseCommand

from anuncios.models import Post


class Command(BaseCommand):
    args = ''
    help = 'Fix broken newline chars in Post texts.'

    def handle(self, *args, **options):
        print('Fixing all newline chars in Post texts.')
        posts = Post.objects.all().order_by('pk')
        count, j, chunksize = posts.count(), 0, 10000
        print('Posts: {}'.format(count))

        for chunk in range(int(count/chunksize)+1):
            start = chunk * chunksize
            end = (chunk + 1) * chunksize
            print('Working on posts {} to {}...'.format(start, end))
            posts = Post.objects.all().order_by('pk')[start:end]
            print('{} posts selected.'.format(posts.count()))
            for p in posts:
                j += 1
                print(' '*60, end='\r', flush=True)
                print('Post: {} / #{}'.format(p.pk, j), end='\r', flush=True)
                p.text = p.text.replace('\r\\n', '\n')
                p.save(update_fields=['text'])
            print('Chunk "{}" finished.'.format(chunk))
        print('All chunks finished.')
