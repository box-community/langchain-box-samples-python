import os
from dotenv import load_dotenv

from langchain_box.blob_loaders import BoxBlobLoader
from langchain_box.utilities import (
    BoxAuth,
    BoxAuthType,
    BoxSearchOptions,
    DocumentFiles,
    SearchTypeFilter
)


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

box_search_options = BoxSearchOptions(
    ancestor_folder_ids=[box_folder_id],
    search_type_filter=[SearchTypeFilter.FILE_CONTENT],
    created_date_range=["2023-01-01T00:00:00-07:00", "2024-08-01T00:00:00-07:00,"],
    file_extensions=[DocumentFiles.DOCX, DocumentFiles.PDF],
    k=200,
    size_range=[1,1000000],
    updated_data_range=None
)

loader = BoxBlobLoader( 
    box_auth=auth,
    query="Victor",
    box_search_options=box_search_options
)

blobs = []

for blob in loader.yield_blobs():
    print(blob)