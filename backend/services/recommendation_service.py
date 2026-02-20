import numpy as np

def recommend_outfit(user_body_ratio, clothes_list):

    recommendations = []

    for cloth in clothes_list:
        score = 1.0 / abs(cloth["fit_ratio"] - user_body_ratio + 0.01)

        recommendations.append({
            "cloth": cloth["name"],
            "score": float(score)
        })

    recommendations.sort(key=lambda x: x["score"], reverse=True)

    return recommendations[:3]

def generate_recommendation(body_data, clothes_data):

    body_ratio = body_data.get("body_ratio", 1.0)
    category = clothes_data.get("category", "unknown")

    suggestions = []

    if body_ratio > 1.1:
        suggestions.append("适合穿高腰设计提升比例")
    else:
        suggestions.append("可选择修身款式增强线条感")

    if category == "jacket":
        suggestions.append("可以搭配简约内搭增加层次感")

    if category == "dress":
        suggestions.append("建议搭配浅色鞋子增强整体协调")

    return suggestions