import re


def alart(sendkey,title,content):

    print(content)

    num = re.search(r'sctp(\d+)t', sendkey).group(1)
    url = f'https://{num}.push.ft07.com/send/{sendkey}.send'

    data = {
        'title': title,
        'desp': content,
    }

    print(requests.post(url, json=data).json())