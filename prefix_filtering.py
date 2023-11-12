import random
import copy


def PrefixFiltering(lst: list[list[str]], num: int = 1) -> list[list[str]]:
    """
    Filtering each element in the list, remove (num) words from the end.

    The function will handle list deep copy by itself.
    """
    copyLst = copy.deepcopy(lst)
    return [ele[:-num] for ele in copyLst]


def RandomPrefixFiltering(lst: list[list[str]], num: int = 1) -> list[list[str]]:
    """
    Filtering each element in the list, remove (num) words with random indices.

    The function will handle list deep copy by itself.
    """
    copyLst = copy.deepcopy(lst)
    newLst = []
    for ele in copyLst:
        if num >= len(ele):
            # simply delete that string from lst
            continue
        for _ in range(num):
            ele.pop(random.randint(0, len(ele) - 1))
        newLst.append(ele)
    return newLst
