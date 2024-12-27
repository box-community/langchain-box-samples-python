import os
from dotenv import load_dotenv

from langchain_box.blob_loaders import BoxBlobLoader
from langchain_box.utilities import BoxAuth, BoxAuthType


load_dotenv("../config/.ccg.env")
load_dotenv("../config/.box.env")

box_client_id=os.getenv("BOX_CLIENT_ID")
box_client_secret=os.getenv("BOX_CLIENT_SECRET")
box_user_id=os.getenv("BOX_USER_ID")
box_folder_id = os.getenv("BOX_FOLDER_ID")

auth = BoxAuth(
    auth_type= BoxAuthType.CCG,
    box_client_id=box_client_id,
    box_client_secret=box_client_secret,
    box_user_id=box_user_id
)

loader = BoxBlobLoader( 
    box_auth=auth,
    box_folder_id=box_folder_id,
    exclude="**/*.boxnote"
)

blobs = []

for blob in loader.yield_blobs():
    print(blob)