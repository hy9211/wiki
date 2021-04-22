import json
from django_redis import get_redis_connection


def format_client_and_score(request):
    data = request.body.decode()
    data_dict = json.loads(data)
    client = data_dict['client']
    score = data_dict['score']

    return client, score


def save_client_and_score(client, score):
    # 建立连接
    con = get_redis_connection('default')
    # 存入分数
    con.zadd('score', {client: score})
