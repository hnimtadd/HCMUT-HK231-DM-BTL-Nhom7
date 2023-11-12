# def SortInvertedIndex(invertedIndex:dict[str,list[int]]) -> dict[str,list[int]]:
#     '''
#         Sort inverted index, return sorted dict in descending order based on len of index list
#     '''
#     return {k: v for k, v in reversed(sorted(invertedIndex.items(), key=lambda item: len(item[1])))}


def _sortWithSortedInvertedIndex(lst :list[list[str]], invertedIndex:dict[str,list[int]]) -> list[list[str]]:
    # sortedID = SortInvertedIndex(invertedIndex=invertedIndex)
    #  loop in list and sort
    [e.sort(key=lambda x: len(invertedIndex[x]) if x in invertedIndex.keys() else 0) for e in lst]
    # for i in range(len(lst)):
    #     lst[i].sort(key=lambda x: len(invertedIndex[x]))
    return lst

def SortWithInvertedIndex(lst :list[list[str]], invertedIndex:dict[str,list[int]]) -> list[list[str]]:
    '''
        Sort each element of lst in ascending order of frequent from invertedIndex
    '''
    return _sortWithSortedInvertedIndex(lst=lst, invertedIndex=invertedIndex)