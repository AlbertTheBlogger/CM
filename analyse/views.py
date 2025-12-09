from django.shortcuts import render, redirect
from django.http import JsonResponse
import json

# Create your views here.

# 预留的立场分析接口
def run_stance_analysis(comments):
    """
    预留接口：对评论列表进行立场分析
    输入: comments = [{"id": 1, "text": "xxx"}, ...]
    输出: [
        {"id": 1, "text": "xxx", "stance": "support", "confidence": 0.92},
        {"id": 2, "text": "yyy", "stance": "oppose", "confidence": 0.87},
        ...
    ]
    """
    # TODO: 替换为真实的情感/立场分析逻辑
    # 当前为模拟返回
    result = []
    for i, c in enumerate(comments):
        # 简单模拟：奇数支持，偶数反对
        stance = "support" if i % 2 == 0 else "oppose"
        confidence = round(0.8 + (i % 3) * 0.05, 2)
        result.append({
            "id": c.get("id", i),
            "text": c["text"],
            "stance": stance,
            "confidence": confidence
        })
    return result


def analyse_select(request):
    """
    展示待分析的评论列表（从前端传入）
    支持两种方式传入数据：
      1. 从 fetch/results 页面跳转，通过 session 或 POST 传递
      2. 直接 GET 请求（开发调试用）
    """
    comments = []

    if request.method == "POST":
        # 要求前端提交 JSON 格式的评论列表
        try:
            body = json.loads(request.body)
            comments = body.get("comments", [])
            request.session['pending_comments'] = comments
        except Exception:
            pass
    else:
        # 尝试从 session 获取（例如从 fetch 模块跳转）
        comments = request.session.get('pending_comments', [])

    return render(request, 'analyse/select.html', {
        'comments': comments
    })


def analyse_results(request):
    """
    执行立场分析并展示结果
    前端应 POST 提交 selected_comment_ids 或完整评论列表
    """
    if request.method != "POST":
        return redirect('analyse:select')

    try:
        data = json.loads(request.body)
        selected_ids = set(data.get("selected_ids", []))

        # 从 session 中获取原始评论列表
        all_comments = request.session.get('pending_comments', [])

        # 筛选出用户选中的评论
        selected_comments = [
            {"id": c.get("id"), "text": c["text"]}
            for c in all_comments
            if str(c.get("id")) in selected_ids or c.get("id") in selected_ids
        ]

        if not selected_comments:
            return JsonResponse({"error": "未选择任何评论"}, status=400)

        # 调用预留的立场分析接口
        analysis_results = run_stance_analysis(selected_comments)

        # 统计立场分布
        stance_counts = {"support": 0, "oppose": 0, "neutral": 0}
        for r in analysis_results:
            stance = r["stance"]
            if stance not in stance_counts:
                stance = "neutral"
            stance_counts[stance] += 1

        context = {
            "results": analysis_results,
            "stance_summary": stance_counts,
            "total": len(analysis_results)
        }

        # 渲染结果页面（也可返回 JSON 供前端 AJAX 渲染）
        return render(request, 'analyse/results.html', context)

    except Exception as e:
        return JsonResponse({"error": f"分析失败: {str(e)}"}, status=500)