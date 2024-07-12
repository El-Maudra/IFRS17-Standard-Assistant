# Delete Unwanted Files from OpenAI's File Storage

import openai

'''
    To delete files from OpenAI's file storage, you can use the following code snippet.
'''

def main(apiKey):
    client = openai.OpenAI(api_key=apiKey)

    #Fetch the list of uploaded files
    files_uploaded = client.files.list()
    print(f"\nUploaded files: \n{files_uploaded}")
    
    list_files = []
    
    # Iterate over the files and append their IDs to list_files and print the file ids
    for file in files_uploaded.data:
        list_files.append(file.id)
    print(f"\nList of file IDs: {list_files}\nAnd the number of files: {len(list_files)}")
    
    # delete the unwanted files uploaded. We will use a while loop to delete the files
 
    while len(list_files) > 0:
        client.files.delete(list_files.pop())
        print(f"\nDeleted file. Remaining files: {len(list_files)}\n\n")
    
    return "All files deleted successfully"

if __name__ == "__main__":
    apiKey = input("Enter your OpenAI API Key: ")
    print(main(apiKey))











