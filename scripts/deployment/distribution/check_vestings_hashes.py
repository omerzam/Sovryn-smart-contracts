from brownie import *

import time
import json
import csv
import math

def main():
    thisNetwork = network.show_active()

    # == Load config =======================================================================================================================
    if thisNetwork == "development":
        acct = accounts[0]
        configFile =  open('./scripts/contractInteraction/testnet_contracts.json')
    elif thisNetwork == "testnet":
        acct = accounts.load("rskdeployer")
        configFile =  open('./scripts/contractInteraction/testnet_contracts.json')
    elif thisNetwork == "rsk-mainnet":
        acct = accounts.load("rskdeployer")
        configFile =  open('./scripts/contractInteraction/mainnet_contracts.json')
    else:
        raise Exception("network not supported")

    # load deployed contracts addresses
    contracts = json.load(configFile)

    vestingRegistry = Contract.from_abi("VestingRegistry", address=contracts['VestingRegistry'], abi=VestingRegistry.abi, owner=acct)
    vestingRegistry2 = Contract.from_abi("VestingRegistry", address=contracts['VestingRegistry2'], abi=VestingRegistry.abi, owner=acct)
    vestingRegistry3 = Contract.from_abi("VestingRegistry", address=contracts['VestingRegistry3'], abi=VestingRegistry.abi, owner=acct)

    data = parseFile('./scripts/deployment/distribution/token-owners-list.csv')

    ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

    for teamVesting in data:
        tokenOwner = teamVesting
        vestingAddress = vestingRegistry.getTeamVesting(tokenOwner)
        if (vestingAddress == ZERO_ADDRESS):
            vestingAddress = vestingRegistry.getVesting(tokenOwner)
        if (vestingAddress == ZERO_ADDRESS):
            vestingAddress = vestingRegistry2.getTeamVesting(tokenOwner)
        if (vestingAddress == ZERO_ADDRESS):
            vestingAddress = vestingRegistry2.getVesting(tokenOwner)
        if (vestingAddress == ZERO_ADDRESS):
            vestingAddress = vestingRegistry3.getTeamVesting(tokenOwner)
        if (vestingAddress == ZERO_ADDRESS):
            vestingAddress = vestingRegistry3.getVesting(tokenOwner)

        print(vestingAddress)

def parseFile(fileName):
    print(fileName)
    teamVestingList = []
    with open(fileName, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            tokenOwner = row[0].replace(" ", "")
            teamVestingList.append(tokenOwner)

    return teamVestingList
