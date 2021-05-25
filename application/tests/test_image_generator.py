from unittest import IsolatedAsyncioTestCase
from ..sources.generators.image_generator import generate_image


class TestImageGenerator(IsolatedAsyncioTestCase):
    async def test_image_generator(self):
        """
        testing image generator by getting some image and checking it
        """
        result = await generate_image()
        self.assertIn(result[-4:], ['.jpg', '.gif', '.png', '.svg'])