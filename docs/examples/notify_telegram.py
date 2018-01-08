#!/usr/bin/env python3

import sys
import json
import requests


TG_TOKEN = 'place token from @botfather here'
TG_CHAT_ID = 0  # place chat id here

URI = 'https://api.telegram.org/bot' + TG_TOKEN + '/sendMessage'

MESSAGE = '''Repo was just updated!
{branch} / [{commit}]({url}) @ {author}
{message}'''


if __name__ == '__main__':
    stdin = input()
    hook_data = json.loads(stdin)

    message = MESSAGE.format(
        author=hook_data['author'],
        branch=hook_data['branch'],
        commit=hook_data['commit'][:7],
        message=hook_data['message'],
        url=hook_data['commit_url']
    )

    data = {
        'chat_id': TG_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True
    }
    res = requests.post(URI, data=data)
