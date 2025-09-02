from app.models import Target
from app.scope import Scope


def test_in_scope():
    targets = [Target(host="example.com", base_url="https://example.com")]
    scope = Scope(targets, include=["extra.com"], exclude=["bad.com"])
    assert scope.in_scope("https://example.com")
    assert scope.in_scope("https://extra.com")
    assert not scope.in_scope("https://bad.com")
