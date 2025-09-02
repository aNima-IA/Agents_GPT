import pytest
import vcr
import httpx

from app.checks.cors import Check


@vcr.use_cassette("tests/cassettes/cors.yaml")
@pytest.mark.asyncio
async def test_cors_check():
    async with httpx.AsyncClient() as client:
        findings = await Check().run("https://example.com/", client)
    assert findings
