from aiohttp import ClientSession


# link, which when accessed, will return the url of cat image
url = 'https://api.thecatapi.com/v1/images/search'

# Function that generating cat image url
async def generate_image():
    img_url = None
    # Opening async client session for making request to address
    async with ClientSession() as session:
        try:
            # Making request to the url and receiving response from the server
            async with session.get(url) as response:
                # Getting data from received response
                data = await response.json()
                # Getting url with cat image from data
                img_url = data[0]['url']

        except Exception as e:
            print(f'An error occurred while receiving the image at the address "{url}" '
                  f'Error {e}')

    return img_url
