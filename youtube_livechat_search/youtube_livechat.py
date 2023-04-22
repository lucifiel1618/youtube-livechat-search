#!/opt/homebrew/bin/python3
import re
import urllib.parse
from threading import Thread
from queue import Queue
import logging
import argparse
import pytchat

def get_logger(name):
    fmt = {'fmt': '{asctime} {name} {levelname} {message}',
           'datefmt': '%H:%M:%S',
           'style': '{'
           }
    handler = logging.StreamHandler()
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    __COLOR_LOG__ = True
    try:
        import coloredlogs
        formatter = coloredlogs.ColoredFormatter(**fmt)
    except ModuleNotFoundError:
        __COLOR_LOG__ = False
        formatter = logging.Formatter(**fmt)
    handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    if not __COLOR_LOG__:
        logger.warning('coloredlogs not installed. Use default python logger.')
    return logger


LOGGER_LEVEL = logging.DEBUG
logger = get_logger('LiveChat')
logger.setLevel(LOGGER_LEVEL)

try:
    import youtube_livechat_search.graph as graph
    __GRAPH__ = True
except ModuleNotFoundError:
    logger.warning('NumPy and/or Matplotlib not installed. Graphic module deactivated.')
    __GRAPH__ = False

__MSG_FMT__ = '[{en.datetime}] {en.modified_message}'
SHOW_GRAPH = __GRAPH__
URL = urllib.parse.ParseResult(scheme='https', netloc='www.youtube.com',
                               path='/watch', params='', query='', fragment='')


class LiveChat:
    def __init__(self, video_id):
        self.video_id = video_id
        self._chat = self._get_chat(self.video_id)
        self._search_results = []
        self.show_url = False

    def search(self, pattern, occurance=0, display_search=True, show_url=None, re_flags=0, show_graph=True):
        show_url = show_url if show_url is not None else self.show_url
        q = Queue()
        t = Thread(target=self._search, args=(self._chat, pattern, q, occurance, re_flags))
        t.start()
        # self._search_results = self._search(self._chat, pattern, occurance)
        if display_search:
            logger.info('Start displaying all searched results in real time...')
            self._dequer(t, q, self._search_results, [lambda en: self.display_search(en, show_url)])
            logger.info('displaying searched results end.')
        else:
            self._dequer(t, q, self._search_results)

        if show_graph:
            graph.hist(self._search_results)
        return self._search_results

    def display_search(self, en, show_url=True):
        logger.info(__MSG_FMT__.format(en=en))
        if show_url:
            query = {'v': self.video_id, 't': self._structed_time(en.elapsedTime)}
            url = URL._replace(query=urllib.parse.urlencode(query))
            print('\033[94;1;4m', urllib.parse.urlunparse(url), '\033[0m', sep='')

    @staticmethod
    def _dequer(thread, queue, to_list=None, actions=[]):
        while thread.is_alive() or (not queue.empty()):
            if queue.empty():
                continue
            en = queue.get()
            for action in actions:
                action(en)
            if to_list is not None:
                to_list.append(en)

    @staticmethod
    def _get_chat(video_id):
        logger.debug('chat is created.')
        return pytchat.create(video_id=video_id)

    @staticmethod
    def _search(chat, pattern, queue, occurance=0, re_flags=0):
        for p in pattern:
            tail = '.' if occurance == 0 else f' until {occurance} results are found.'
            MSG = f'Searching for "{p}"{tail}'
            logger.debug(MSG)
        occ = 0
        prog = [re.compile(p, flags=re_flags) for p in pattern]
        while chat.is_alive():
            is_empty = True
            for en in chat.get().items:
                is_empty &= False
                # print(__MSG_FMT__.format(en = en))
                if any(p.search(en.message) for p in prog):
                    en.modified_message = en.message
                    for p in prog:
                        en.modified_message = p.sub(lambda m: ''.join(
                            ('\033[33;1m', m.group(0), '\033[0m')), en.modified_message)
                    queue.put(en)
                    occ += 1
                    # logger.debug('{}/{} results are found.'.format(occ, occurance))
                    if occ == occurance:
                        logger.debug('Enough results are found. Search ends.')
                        chat.terminate()
            if is_empty:
                logger.debug('Empty chat retrieved.')
        logger.debug('chat ends here.')
        chat.terminate()

    @staticmethod
    def _structed_time(time_str):
        return ''.join([d + u for d, u in zip(time_str.split(':')[::-1], ['s', 'm', 'h'])][::-1])


def main():
    parser = argparse.ArgumentParser(
        description="Youtube Live Chat Search",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('id', nargs=1, help='Video ID')
    parser.add_argument('pattern', nargs='+', default=[], type=str, help='Search pattern')
    parser.add_argument('--ignore-case', '-I', action='store_true', help='Perform case-insensitive matching.')
    parser.add_argument('--occurance', '-O', default=0, type=int, help='String occurance.')
    parser.add_argument('--hide-url', '-U', action='store_true', help='Hide url')
    parser.add_argument('--show-graph', '-G', action='store_true', help='Show statistical graph')
    parser.add_argument(
        '--debug-level', '-L',
        default='DEBUG',
        type=str,
        choices=['DEBUG', 'INFO', 'ERROR', 'CRITICAL'],
        help='debug level'
    )

    args = parser.parse_args()
    occurance = args.occurance
    show_url = not args.hide_url
    video_id = args.id[0]
    show_graph = SHOW_GRAPH & args.show_graph
    pattern = args.pattern
    re_flags = 0
    if args.ignore_case:
        re_flags = re.IGNORECASE
    logger_level = getattr(logging, args.debug_level)

    logger.setLevel(logger_level)

    lc = LiveChat(video_id)
    lc.search(pattern, occurance, display_search=True, show_url=show_url, re_flags=re_flags, show_graph=show_graph)


if __name__ == '__main__':
    main()
