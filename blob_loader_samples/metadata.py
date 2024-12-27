import ast
import os
from dotenv import load_dotenv

from langchain_box.blob_loaders import BoxBlobLoader
from langchain_box.utilities import BoxAuth, BoxAuthType, BoxMetadataQuery


load_dotenv("../config/.ccg.env")
load_dotenv("../config/.box.env")

box_client_id=os.getenv("BOX_CLIENT_ID")
box_client_secret=os.getenv("BOX_CLIENT_SECRET")
box_user_id=os.getenv("BOX_USER_ID")
box_metadata_template=os.getenv("BOX_METADATA_TEMPLATE")
box_metadata_query=os.getenv("BOX_METADATA_QUERY")
box_metadata_params=os.getenv("BOX_METADATA_PARAMS")
box_enterprise_id=os.getenv("BOX_ENTERPRISE_ID")

auth = BoxAuth(
    auth_type= BoxAuthType.CCG,
    box_client_id=box_client_id,
    box_client_secret=box_client_secret,
    box_user_id=box_user_id
)

params = ast.literal_eval(box_metadata_params)

query = BoxMetadataQuery(
    template_key=f"enterprise_{box_enterprise_id}.{box_metadata_template}",
    query=box_metadata_query,
    query_params=params,
    ancestor_folder_id="260932470532"
)

loader = BoxBlobLoader( 
    box_auth=auth,
    box_metadata_query=query
)

blobs = []

for blob in loader.yield_blobs():
    print(blob)