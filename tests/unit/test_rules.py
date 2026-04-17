def calculate_prize(
    reds: list, blues: list, target_reds: list, target_blue: int
) -> int:
    # 简单的兑奖逻辑示例
    matched_reds = len(set(reds) & set(target_reds))
    matched_blue = 1 if target_blue in blues else 0
    if matched_reds == 6 and matched_blue == 1:
        return 1
    elif matched_reds == 6:
        return 2
    elif matched_reds == 5 and matched_blue == 1:
        return 3
    elif (matched_reds == 5) or (matched_reds == 4 and matched_blue == 1):
        return 4
    elif (matched_reds == 4) or (matched_reds == 3 and matched_blue == 1):
        return 5
    elif matched_blue == 1:
        return 6
    return 0


def test_prize_rules_single():
    # 单式测试
    target_reds = [1, 2, 3, 4, 5, 6]
    target_blue = 7

    assert calculate_prize([1, 2, 3, 4, 5, 6], [7], target_reds, target_blue) == 1
    assert calculate_prize([1, 2, 3, 4, 5, 6], [8], target_reds, target_blue) == 2
    assert calculate_prize([1, 2, 3, 4, 5, 10], [7], target_reds, target_blue) == 3


def test_prize_rules_multiple():
    # 复式测试 (展开后包含头奖)
    target_reds = [1, 2, 3, 4, 5, 6]
    target_blue = 7

    reds = [1, 2, 3, 4, 5, 6, 8, 9]
    blues = [7, 10]

    # 复式会展开多注，其中必定有一注是6红1蓝
    assert calculate_prize(reds, blues, target_reds, target_blue) == 1


def test_prize_rules_dantuo():
    # 胆拖测试
    target_reds = [1, 2, 3, 4, 5, 6]
    target_blue = 7

    dan = [1, 2, 3, 4]
    tuo = [5, 6, 8, 9]
    # 组合中必定有 1,2,3,4,5,6
    assert calculate_prize(dan + tuo, [7], target_reds, target_blue) == 1
