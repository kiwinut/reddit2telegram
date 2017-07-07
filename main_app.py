#encoding:utf-8

import importlib
import logging

import yaml
import praw
from sentry import report_error

import utils


logger = logging.getLogger(__name__)


@report_error
def supply(subreddit, config):
    submodule = importlib.import_module('channels.{}.app'.format(subreddit))
    reddit = praw.Reddit(user_agent=config['reddit']['user_agent'],
                        client_id=config['reddit']['client_id'],
                        client_secret=config['reddit']['client_secret'])
    submissions = reddit.subreddit(submodule.subreddit).search("flair_text:mv",sort='new',time_filter='day')
    r2t = utils.Reddit2TelegramSender(submodule.t_channel, config)
    success = False
    for submission in submissions:
        link = submission.shortlink
        if r2t.was_before(link):
            continue
        success = submodule.send_post(submission, r2t)
        if success is True:
            # Every thing is ok, post was sent
            r2t.mark_as_was_before(link)
            break
        elif success is False:
            # Do not want to send this post
            r2t.mark_as_was_before(link)
            continue
        else:
            # If None — do not want to send anything this time
            break
    if success is False:
        logger.info('Nothing to post from {sub} to {channel}.'.format(
                    sub=submodule.subreddit, channel=submodule.t_channel))


def main(config_filename, sub):
    with open(config_filename) as config_file:
        config = yaml.load(config_file.read())
    supply(sub, config)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='prod.yml')
    parser.add_argument('--sub')
    args = parser.parse_args()
    main(args.config, args.sub)
