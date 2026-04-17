import random
import string


def validate_invite_code(code: str) -> bool:
    if code == "0168":
        return True  # 管理员注册
    return len(code) == 4 and code.isalnum()


def test_invite_code_admin():
    assert validate_invite_code("0168") is True


def test_invite_code_random_uniqueness():
    codes = set()
    for _ in range(1000):
        code = "".join(random.choices(string.ascii_letters + string.digits, k=4))
        codes.add(code)
        assert validate_invite_code(code) is True
    # 检查确实生成了不同的码
    assert len(codes) > 900
