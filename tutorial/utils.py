import base64
import json

from web3 import Web3, HTTPProvider


def imageToBase64String():
    with open("../image1.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string


def videoToBase64String():
    with open("../demo.mp4", "rb") as videoFile:
        encoded_string = base64.b64encode(videoFile.read())
        return encoded_string


def base64StringToImage(img_data):
    with open("../imageToSave.png", "wb") as fh:
        fh.write(base64.decodebytes(img_data))


def size(b64string):
    # x = (n * (3/4)) - y
    return (len(b64string) * 3) / 4 - b64string.count('=', -2)


def splitStringEveryKb(str, kb_size):
    list_of_strings = []
    kb_size = kb_size * 1024
    counter = 0
    temp_str = ''
    for s in str:
        if counter == kb_size:
            print("Temp Sttr : " + temp_str)
            list_of_strings.append(temp_str)
            counter = 0
            temp_str = ''
        else:
            counter += 1
            temp_str += s
    return list_of_strings


def splitStringEveryCharacter(line, n):
    return [line[i:i + n] for i in range(0, len(line), n)]


def collectListOfStrings(strs):
    string = ''
    counter = 0
    for s in strs:
        counter += 1
        print("[ No." + str(counter) + " size : " + str(len(s)) + " bytes" + " ]" + " -> " + s)
        string += s
    return string





if __name__ == '__main__':
    img_data = videoToBase64String()
    das = img_data.decode('utf-8')
    print("Text Bytes : " + str(len(das)))
    splittedStrs = splitStringEveryCharacter(das, 1024 * 2)
    collectedStr = collectListOfStrings(splittedStrs)
    print(collectedStr)
    # base64StringToImage(collectedStr.encode('utf-8'))
    # print()
    # uploadToNFT(splittedStrs, "0x38C1E1204C10C8be90ecA671Da8Ea8a9AEb16031")
