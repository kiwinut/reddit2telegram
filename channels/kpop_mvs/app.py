#encoding:utf-8

from utils import get_url, weighted_random_subreddit


t_channel = '@kpop_mvs'
subreddit = 'kpop'


def send_post(submission, r2t):
    what, url, ext = get_url(submission)
    title = submission.title
    link = submission.shortlink
    sub = submission.subreddit
    text = '{}\n\n/r/{}\n{}'.format(title, sub, link)

    if what == 'text':
        return False
    elif what == 'other':
        base_url = submission.url
        text = '{}\n{}\n\n/r/{}\n{}'.format(title, base_url, sub, link)
        return r2t.send_text(text)
    elif what == 'album':
        return False
    elif what in ('gif', 'img'):
        return False
    else:
        return False
