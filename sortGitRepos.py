#!/usr/bin/env python

'''
This is for Adobe Internal Use
Author: Elan Elangovan
Description:
- Get the URL
- Sort based on Updated_at field
- Print with fields required
'''

import requests
import time
import json
import logging
import argparse

def getUrl(url):
    '''
    Function to process API request
    :param: url
    :return: response data in JSON format of (list of dicts)
    '''
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        responseOutput = response.json()
        return responseOutput
    except requests.exceptions.HTTPError as errCode:
        return "An Http Error occurred: " + str(errCode)
    except requests.exceptions.ConnectionError as errCode:
        return "An Error Connecting to the API occurred: " + repr(errCode)
    except requests.exceptions.Timeout as errCode:
        return "A Timeout Error occurred: " + repr(errCode)
    except:
        return "Something wrong with URL endpoint, please check"


def sortByDate(list_dicts, str_to_sort):
    """
    Function to sort based on a time stamp
    :param: str_to_sort -> Sort based on this string/ value
    :param: list_dicts -> Unsorted list from getUrl function
    :return: list_dict -> It will be sorted by str_to_sort 
    """
    
    beforeSorted = list_dicts[0]
    logging.info('Sorting data based on the string - ')
    list_dicts.sort(key=lambda x:x[str_to_sort], reverse=True)
    return list_dicts


def dictToTable(sortedList):
    """
    Convert list of dicts to table formatted data
    :param: str_to_sort -> Sort based on this string/ value
    :param: list_dicts -> Unsorted list from getUrl function
    :return: list_dict -> It will be sorted by str_to_sort 
    """

    titleList = ["name", "stargazers_count", "updated_at"]
    newList = [titleList]
    iterList = []

    for item in sortedList: iterList.append([str(item[col] if item[col] is not None else '') for col in titleList]) 
    print ("{:<30} ||\t {:<10} ||\t {:<20}".format(*titleList))
    print("\n-------------------------------------------------------------------------------\n")

    for item in iterList:
        print ("{:<30} ||\t {:<16} ||\t {:<20}".format(*item))


if __name__ == '__main__':
    '''
    Main function to call sub functions - getUrl, sortUrlJsonResponse, outputInTableFormat
    :param: url
    '''
    
    logging.info("Welcome to sorting your GitRepos 1) Please enter your URL")

    parser = argparse.ArgumentParser(description='Sorting Git Repos')
    parser.add_argument('-url', '--url', 
                        help='Enter Git repo url to sort on the Updated/ Created/ Pushed date of your choice', nargs='?',
                        default='https://api.github.com/orgs/adobe/repos', const=1)
    parser.add_argument('-sortby', '--sortby',
                    const=1, default='updated_at', nargs='?',
                    choices=['updated_at', 'pushed_at', 'created_at'],
                    help='Please choose one of the above to sort by')

    args = parser.parse_args()
    url = args.url
    sortby = args.sortby
    print("sortby", sortby)

    '''
    getUrl - Return JSON data of the URL
    sortByDate - Sort the result based on the string to sort - this can be improvised
    '''
    responseUrlJson = getUrl(url)
    sortedList = sortByDate(responseUrlJson, sortby)
    dictToTable(sortedList)




