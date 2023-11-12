# def SortInvertedIndex(invertedIndex:dict[str,list[int]]) -> dict[str,list[int]]:
#     '''
#         Sort inverted index, return sorted dict in descending order based on len of index list
#     '''
#     return {k: v for k, v in reversed(sorted(invertedIndex.items(), key=lambda item: len(item[1])))}


def _frequent(dataset: tuple[list[list[str]]]) -> dict[str, int]:
    frequent_dict = dict()
    for lst in dataset:
        for str in lst:
            for word in str:
                frequent_dict[word] = frequent_dict.get(word, 0) + 1
    return frequent_dict


def _sortWithSortedInvertedIndex(
    lst: list[list[str]],
    invertedIndex: dict[str, list[int]],
    asceding: bool = True,
) -> list[list[str]]:
    # sortedID = SortInvertedIndex(invertedIndex=invertedIndex)
    #  loop in list and sort
    [
        e.sort(
            key=lambda x: len(invertedIndex[x]) if x in invertedIndex.keys() else 0,
            reverse=not ascending,
        )
        for e in lst
    ]
    # for i in range(len(lst)):
    #     lst[i].sort(key=lambda x: len(invertedIndex[x]))
    return lst


def SortWithInvertedIndex(
    lst: list[list[str]],
    invertedIndex: dict[str, list[int]],
    ascending: bool = True,
) -> list[list[str]]:
    """
    Sort each element of the list in ascending order of frequency from the inverted index.

    The result is a dataset in which each sentence has been reordered by word frequency

    The function will handle list deep copy by itself.
    """
    return _sortWithSortedInvertedIndex(
        lst=lst, invertedIndex=invertedIndex, ascending=ascending
    )


def SortWithFrequent(
    dataset: tuple[list[list[str]]], ascending: bool = True
) -> tuple[list[list[str]]]:
    """
    Sort the dataset by the frequency of each word.

    The result is a dataset in which each sentence has been reordered by word frequency

    The function will handle list deep copy by itself.
    """
    frequent = _frequent(dataset=dataset)
    print(frequent)
    [
        [
            ele.sort(
                key=lambda x: frequent[x] if x in frequent.keys() else 1,
                reverse=not ascending,
            )
            for ele in lst
        ]
        for lst in dataset
    ]
    return dataset
