
from web3 import Web3


def getAddress(text):
    index = text.find('0')
    if index == -1:
        return ""
    address = text[index:]
    if not Web3.isAddress(address):
        return ""
    return address