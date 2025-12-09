# fetch/views.py
import requests
from lxml import etree
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.cache import cache  # 可选：加入缓存避免频繁请求
from search import get_html_by_keyword

#
# except ImportError:
#     def get_html_by_keyword(keyword):
#         return {
#             "keyword": keyword,
#             "posts": [
#                 {"title": f"关于 {keyword} 的讨论1", "comments_count": 42, "time_range": "2025-12-01 ~ 2025-12-08"},
#                 {"title": f"{keyword} 引发热议", "comments_count": 128, "time_range": "2025-12-09"}
#             ],
#             "total_comments": 170,
#             "wordcloud_data": {"热": 50, "争议": 30, "支持": 25, "反对": 20},
#             "chart_options": ["bar", "line", "pie"]
#         }
#

def _fetch_weibo_hot_search(limit=10):
    """
    从微博热搜榜抓取实时热点词（前 limit 条）
    返回: ['关键词1', '关键词2', ...]
    """
    cache_key = "weibo_hot_search_keywords"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    url = "https://s.weibo.com/top/summary?cate=realtimehot"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        html = response.text

        tree = etree.HTML(html)
        keywords = []
        # 热搜条目通常在 table 中，每行一个
        rows = tree.xpath('//table//tr[position()>1]')  # 跳过表头
        for row in rows[:limit]:
            kw_elem = row.xpath('.//td[2]/a/text()')    #跳过热度提示词
            if kw_elem:
                kw = kw_elem[0].strip()
                if kw and not kw.startswith('http'):
                    keywords.append(kw)
        # 缓存 5 分钟
        cache.set(cache_key, keywords, timeout=300)
        return keywords
    except Exception as e:
        # 出错时返回默认热点词（可选）
        print(f"[WARNING] Failed to fetch Weibo hot search: {e}")
        return [
            "default_1",
            "default_2",
        ]


def fetch_main(request):
    """主界面：显示搜索框 + 实时热点词（来自微博API）"""
    hot_keywords = _fetch_weibo_hot_search(limit=10)
    return render(request, 'fetch/main.html', {
        'hot_keywords': hot_keywords
    })


def fetch_results(request):
    """处理关键词提交，调用爬虫并展示结果"""
    if request.method == 'POST':
        keyword = request.POST.get('keyword', '').strip()
        if not keyword:
            return render(request, 'fetch/results.html', {'error': '请输入关键词或URL'})

        try:
            data = get_html_by_keyword(keyword)
        except Exception as e:
            return render(request, 'fetch/results.html', {
                'error': f'爬取失败: {str(e)}',
                'keyword': keyword
            })

        context = {
            'keyword': keyword,
            'posts': data.get('posts', []),
            'total_comments': data.get('total_comments', 0),
            'wordcloud_data': data.get('wordcloud_data', {}),
            'chart_types': data.get('chart_options', ['词云', '柱状图']),
            'time_range': "最近7天"  # 可根据实际数据调整
        }
        return render(request, 'fetch/results.html', context)

    return redirect('fetch:main')