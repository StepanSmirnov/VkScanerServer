import vk

class PhotoGrabber:
    def __init__(self, access_token):
        self.token = access_token

    def loadPhotos(self, owner_id = ""):
        session = vk.Session()
        vkapi = vk.API(access_token=self.token, session = session)
        response = vkapi.photos.getAll(owner_id = vkapi.users.get(user_ids=owner_id)[0]["uid"])[1:]
        return [url["src"] for url in response]

