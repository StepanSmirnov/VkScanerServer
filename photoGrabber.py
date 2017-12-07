import vk
# from PIL import Image
# import requests
# from io import BytesIO

class PhotoGrabber:
    def __init__(self, access_token):
        self.token = access_token

    def loadPhotos(self, owner_id = ""):
        # images = []
        session = vk.Session()
        vkapi = vk.API(access_token=self.token, session = session)
        response = vkapi.photos.getAll(owner_id = vkapi.users.get(user_ids=owner_id)[0]["uid"])[1:]
        # print(url)
        # response = requests.get(url["src"])
        # images.append(Image.open(BytesIO(response.content)))
        return [url["src"] for url in response]

if (__name__ == "__main__"):
    token = "605974277d4764bce2cca4deeec2b7b8ff7e6ae48925a110ef667d82fc4ea6fa35a0ad6f6fa9235f7cf4c"
    grabber = PhotoGrabber(token)
    print(grabber.loadPhotos())
