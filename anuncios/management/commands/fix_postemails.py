from django.core.management.base import BaseCommand

from anuncios.models import Post


class Command(BaseCommand):
    args = ''
    help = 'Add user emails to posts and confirm.'

    def handle(self, *args, **options):
        print('Adding user email to all Posts and confirm.')
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
                if p.user is not None:
                    p.email = p.user.email
                    p.is_confirmed = True
                    p.save(update_fields=['email', 'is_confirmed'])
            print('Chunk "{}" finished.'.format(chunk))
        print('All chunks finished.')
