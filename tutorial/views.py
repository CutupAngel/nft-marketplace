from django.shortcuts import render

from wallet.models import User, File


def index(request):
    return render(request, 'index.html')


def myfiles(request, address):
    listOfFiles = []
    fileLists = User.objects.filter(address=address)
    for file in fileLists:
        mapFileData = {}
        filePortions = File.objects.filter(fileId=file.fileId).order_by('-token_id')
        mapFileData['fileName'] = file.fileName
        mapFileData['fileType'] = file.fileType
        mapFileData['fileId'] = file.fileId
        listOfFilePortions = []
        for filePor in filePortions:
            mapFilePorData = {}
            mapFilePorData['token_id'] = filePor.token_id
            mapFilePorData['token_portion'] = filePor.token_portion
            listOfFilePortions.append(mapFilePorData)
        mapFileData['filePortions'] = listOfFilePortions
        listOfFiles.append(mapFileData)

    context = {
        'address' : address,
        'items': listOfFiles
    }
    return render(request, 'detail.html', context=context)
