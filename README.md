# langchain-box sample code

This repo contains several folders, each containing sample code for a specific `langchain-box` object.

## BoxLoader

In the `document_loader_samples` directory, there is sample code covering various scenarios with the `BoxLoader` object. This object takes a `List[str]` of Box file ids or a `str` object containing a Box folder id and returns a List of `Document` objects based on the text representation available in Box. This only works for files types that have text representations in Box.

* [Single file](document_loader_samples/one_file.py)
* [Multiple files](document_loader_samples/multiple_files.py)
* [All files in a folder](document_loader_samples/folder.py)
* [All files in a folder recursively](document_loader_samples/folder_recursive.py)
* [Character limits](document_loader_samples/character_limit.py)
* [Extra fields](document_loader_samples/extra_fields.py)

## BoxBlobLoader

In the `blob_loader_samples` directory, there is sample code covering various scenarios with the `BoxBlobLoader` object. This object accepts one of the following inputs: 
* `List[str]` of Box file ids
* `str` containing a Box folder id
* `str` containing a search query
* `BoxMetadataQuery` specifying a Metadata template, query, and paramaters

Based on the input, this object returns a List of `Blob` objects containing the raw data from any document or image file type in Box. This Blob object can be passed to your favorite `BlobParser` to generate `Document` objects.
 
* [Single file](blob_loader_samples/one_file.py)
* [Multiple files](blob_loader_samples/multiple_files.py)
* [All files in a folder](blob_loader_samples/folder.py)
* [All files in a folder recursively](blob_loader_samples/folder_recursive.py)
* [Files in a folder if a document file type](blob_loader_samples/folder_docs.py)
* [Files in a folder if an image file type](blob_loader_samples/folder_images.py)
* [Files in a folder if filename matches glob](blob_loader_samples/folder_glob.py)
* [Files in a folder if filename doesn't match glob](blob_loader_samples/folder_exclude.py)
* [Files in a folder if a document has a matching extension](blob_loader_samples/folder_suffixes.py)
* [Files based on Metadata query](blob_loader_samples/metadata.py)
* [Files based on search](blob_loader_samples/search.py)
* [Files based on search with seach filters](blob_loader_samples/search_options.py)
* [Extra fields](blob_loader_samples/extra_fields.py)

## BoxRetriever

In the `retriever_samples` directory, there is sample code covering various scenarios with the `BoxRetriever` object. This object accepts either a `str` containing a search query or both a `str` with a Box AI query and a `List[str]` with Box file ids.

Based on the input, this object returns a List of `Document` objects containing either the text representation from document file types in Box or the answer and/or citations from a Box AI API call.
 
* [Search](retriever_samples/search.py)
* [search with filters](retriever_samples/search_options.py)
* [Box AI with one file](retriever_samples/box_ai_ask_one.py)
* [Box AI with multiple files](retriever_samples/box_ai_ask_multiple.py)
* [Box AI with answer and citations](retriever_samples/box_ai_ask_one_answer_citations.py)
* [Box AI with citations only](retriever_samples/box_ai_ask_one_citations_only.py)
* [Search as an agent tool](retriever_samples/search_as_tool.py)
* [Search as part of a chain](retriever_samples/retriever_chain.py)
* [Extra fields](retriever_samples/extra_fields.py)

It also enables tests for mutiple authentication methods:
* [Developer token as an environment variable](auth_samples/env_token.py)
* [Developer token passed to Loader](auth_samples/token_direct.py)
* [Developer token passed as BoxAuth](auth_samples/token_auth.py)
* [JWT with service account](auth_samples/jwt_eid.py)
* [JWT as user](auth_samples/jwt_user.py)
* [Client credentials grant with service account](auth_samples/ccg_eid.py)
* [Client credentials grant as user](auth_samples/ccg_user.py)


## Prepare the test suite for use

Now that we have langchain ready to use locally, we can now set up the tests to run. The test scripts rely on two key components, the environment files located in the [config](config) folder and the [box search](box_search.py) object.

The environment files are use to configure the tests to work. 

File | Purpose | Required
---+---+---
[.openai.env.template](.openai.env.template) | Configure openai API key | Yes
[.box.env.template](.box.env.template) | Configure Box-specific fields like file and folder ids | Yes
[.token.env.template](.token.env.template) | Configure developer token auth | Only for token tests
[.jwt.env.template](.jwt.env.template) | Configure JWT auth | Only for JWT tests
[.ccg.env.template](.ccg.env.template) | Configure CCG Auth | Only for CCG tests

The [box search](box_search.py) object enables a "real-life" scenario after the test scripts load the appropriate Documents from Box. box_search provides a two methods, `train_ai` and `box_search`.

The `train_ai` method accepts the documents return from the BoxLoader as an argument. It then does several things with those documents. First, it splits the documents into logical chunks using langchains `RecursiveCharacterTextSplitter`. It then takes those chunks of text, converts them to OpenAI embeddings and commits them to a local Chroma vector store. Finally, it instantiates a `ChatOpenAI` as the llm of choice, creates an `LLMChainExtractor` as a compressor, and uses it and Chroma as a `ContextualCompressionRetriever`. 

Many thanks to [HTMLFiveDev](https://www.youtube.com/@htmlfivedev) for their [video](https://www.youtube.com/watch?v=_zdpmxpH7S0), on which this object is based.

OK, assuming you have completed the steps above to get the langchain fork installed and prepped, let's get this started.

1. In your terminal, clone this repository to your local machine by running `git clone https://github.com/shurrey/box-langchain-documentloader-tests.git`. **This should not be inside of the langchain directory**.
2. Change directories to the project by running `cd box-langchain-documentloader-tests`. Open the folder in your favorite editor.
3. In the config directory, copy the environment templates to new files, for example, copy `.box.env.template` to `.box.env`. You must have `.box.env`, `.openai.env`, and whichever auth modes you plan to use. Open the newly created files, and add your values. 
5. Install the libraries you need. I recommend using a virtual environment. Follow [these instructions](https://virtualenv.pypa.io/en/latest/installation.html) to install it. Once installed, you can create a virtual environment at the command line in the root directory of this application by running `virtualenv .venv`.
6. Once you complete that step, you can activate your virtual environment at the commandline by running `source .venv/bin/activate`. This should change your command line prompt and prepend it with `(.venv)`.
7. Now you can install your dependencies at the commandline in the root directory of this application by running `pip install -r requirements.txt`.
5. You should now be all set to run the tests. Each test has a variable called `prompt`, which you can set based on the file(s) or folder you choose. It will be asked to OpenAI, so you will get a real answer based on the file(s) you provide. 

To run the tests, you can either use the tools provided by your development environment, or from the command line, run `python TEST_NAME.py` where TEST_NAME is the file name of the test you wish to run. For example, to test one file, you can change to the appropriate directory like `cd document_loader_test_scripts` and then run `python test_one_-_file.py`.