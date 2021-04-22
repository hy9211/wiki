import json
from django_redis import get_redis_connection


def create_connect_redis():
    con = get_redis_connection('default')
    return con


def format_client_and_rank(request):
    data = request.body.decode()
    data_dict = json.loads(data)
    client = data_dict['client']
    start_rank = data_dict['start_rank']
    end_rank = data_dict['end_rank']
    if not start_rank and not end_rank:
        start_rank = 1
        end_rank = 10

    return client, start_rank, end_rank


def get_self_rank_score(con, client):
    rank = con.zrevrank('score', client)
    score = con.zscore("score", client)
    return rank + 1, score


def get_range_rank_score(con, start_rank, end_rank):
    i = start_rank
    start_rank -= 1
    clients = con.zrevrange('score', start_rank, end_rank, withscores=False, score_cast_func=float)
    data_list = []
    for client in clients:
        client = client.decode()
        score = con.zscore("score", client)
        data_list.append([i, client, score])
        i += 1
    return data_list
