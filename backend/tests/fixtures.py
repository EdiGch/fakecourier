import asyncio

import pytest


@pytest.fixture
def dummy_async_function_with_result():
    future = asyncio.Future()
    future.set_result("Result")

    return future
