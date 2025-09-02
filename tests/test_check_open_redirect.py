import pytest
import vcr
import httpx

from app.checks import open_redirect


@vcr.use_cassette("tests/cassettes/open_redirect.yaml")
@pytest.mark.asyncio
async def test_open_redirect_check():
    open_redirect.PARAMS = ["next"]
    async with httpx.AsyncClient() as client:
        findings = await open_redirect.Check().run("https://example.com/redirect", client)
    assert findings
