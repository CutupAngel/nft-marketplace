import base64
import json
import uuid

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from web3 import Web3, HTTPProvider

from tutorial.utils import splitStringEveryCharacter, collectListOfStrings, base64StringToImage
from wallet.models import File, User


def uploadToNFT(list_of_arrays, walletAddress):
    web3 = Web3(HTTPProvider('https://data-seed-prebsc-1-s2.binance.org:8545/'))
    ERC20_ABI = json.loads(
        '[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256[]","name":"_tokenIds","type":"uint256[]"},{"internalType":"string[]","name":"_strs","type":"string[]"}],"name":"batchCreate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_str","type":"string"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"createItem","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getLastTokenId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"last_token_id","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"mapAccounts","outputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"string","name":"filePortion","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"tokenIdFiles","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]')
    tokenContract = '0x2A768003c2F300a617f4b3bB3b6c7C1DE8F2d016'
    tokenContract = web3.toChecksumAddress(tokenContract)

    walletAddress = web3.toChecksumAddress(walletAddress)

    public_key = '0x38C1E1204C10C8be90ecA671Da8Ea8a9AEb16031'
    public_key = web3.toChecksumAddress(public_key)
    private_key = '59a48bac86bffca9695153d414aafdcaacd960dac9a6306779b42cc9699503e6'

    myContract = web3.eth.contract(address=tokenContract, abi=ERC20_ABI)
    chainID = 97
    defaultGasLimit = 1612917 * len(list_of_arrays)
    defaultGasPrice = web3.toWei('20', 'gwei')

    lastTokenId = myContract.functions.getLastTokenId().call()
    lastTokenId += 1

    list_of_token_ids = []

    for i in range(len(list_of_arrays)):
        list_of_token_ids.append(lastTokenId + i)

    txn_data = myContract.functions.batchCreate(
        walletAddress,
        list_of_token_ids,
        list_of_arrays,
    ).buildTransaction({
        'chainId': chainID,
        'gas': defaultGasLimit,
        'gasPrice': defaultGasPrice,
        'nonce': web3.eth.getTransactionCount(public_key),
    })

    # Signing transaction with private key
    signed_txn = web3.eth.account.signTransaction(txn_data, private_key=private_key)

    # send transaction to blockchain
    web3.eth.sendRawTransaction(signed_txn.rawTransaction)

    # Transaction hash of the transaction which must be returned to client
    print(web3.toHex(web3.sha3(signed_txn.rawTransaction)))

    txHash = web3.toHex(web3.sha3(signed_txn.rawTransaction))

    data = {
        'txHash': txHash,
        'tokenIds': list_of_token_ids,
    }

    return data

@csrf_exempt
@api_view(['POST'])
def uploadImage(request):
    try:
        body = json.loads(request.POST.get('data'))
        walletAddress = body["wallet_address"]
        files = request.FILES
        keystoreFile = files.get('file', None)
        image_file = keystoreFile.read()
        encoded_string = base64.b64encode(image_file)
        das = encoded_string.decode('utf-8')
        splittedStrs = splitStringEveryCharacter(das, 1024 * 2)

        uploadData = uploadToNFT(splittedStrs, walletAddress)

        list_of_token_ids = uploadData['tokenIds']

        # uniqueFileId = uuid.uuid4()
        # userModel = User(address=walletAddress, fileType="IMAGE", fileName="D", fileId=uniqueFileId)
        # userModel.save()
        #
        # for i in range(len(list_of_token_ids)):
        #     fileModel = File(token_id=list_of_token_ids[i], token_portion=splittedStrs[i], fileId=uniqueFileId)
        #     fileModel.save()

        collectedStr = collectListOfStrings(splittedStrs)

        # base64StringToImage(collectedStr.encode('utf-8'))
        message = {
            'message': None,
            'data': {
                'txHash': uploadData['txHash'],
                'tokenIds': uploadData['tokenIds'],
                'filePortions': splittedStrs,
                'fullBase64': collectedStr
            },
            'status_code': status.HTTP_200_OK
        }
        return JsonResponse(message, status=status.HTTP_200_OK)
    except Exception as e:
        print(str(e))
        message = {
            'message': str(e),
            'data': None,
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
        }
        return JsonResponse(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def getFiles(request):
    try:
        body = request.data
        walletAddress = body["wallet_address"]

        listOfFiles = []
        fileLists = User.objects.filter(address=walletAddress)

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

        message = {
            'message': None,
            'data': {
                'address': walletAddress,
                'files': listOfFiles,
            },
            'status_code': status.HTTP_200_OK
        }
        return JsonResponse(message, status=status.HTTP_200_OK)
    except Exception as e:
        message = {
            'message': str(e),
            'data': None,
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
        }
        return JsonResponse(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
