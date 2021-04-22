"""
    排行榜
"""
from django.http import JsonResponse

from domain.score_about_receive import format_client_and_score, save_client_and_score
from domain.score_about_query import create_connect_redis, format_client_and_rank, get_self_rank_score, get_range_rank_score


def api_receive_score(request):
    if request.method == 'POST':
        # 格式化客户端号和分数
        client, score = format_client_and_score(request)
        # 存入redis有序集合
        save_client_and_score(client, score)
        """
            code: 状态码
        """
        return JsonResponse({'code': 200})


def api_query_rank(request):
    if request.method == 'POST':
        # 建立连接
        con = create_connect_redis()
        # 格式化客户端号，查询起始排名和结束排名
        client, start_rank, end_rank = format_client_and_rank(request)
        # 获取当前客户端号排名和分数
        self_rank, self_score = get_self_rank_score(con, client)
        # 获取查询范围内客户端号和分数
        data_list = get_range_rank_score(con, start_rank, end_rank)
        # 将当前客户端添加到列表末尾
        data_list.append([self_rank, client, self_score])
        print(data_list)
        """
            code: 状态码
            data: 数据，为二维数组
                example:
                [[1, client1, 111], 
                 [2, client2, 100],
                 [self_rank, self_client, self_score],]
                rank: 排名
                client: 客户端编号
                score: 分数
                self_rank: 当前用户排名
                self_client: 当前用户客户端编号
                self_score: 当前用户分数
                
                flag: 数组最后一个元素,是当前用户的数据
        """
        return JsonResponse({'code': 200, 'data': data_list})
