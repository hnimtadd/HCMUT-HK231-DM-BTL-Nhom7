from sort import SortWithInvertedIndex, SortWithFrequent
from prefix_filtering import RandomPrefixFiltering, PrefixFiltering

if __name__ == "__main__":
    # b = 4, c = 2, a = 3, d = 1
    x = [
        ["c", "b"],  # expected ["c",  "b"]
        ["a", "b"],  # expected ["a", "b"]
    ]
    y = [
        ["b", "a"],  # expected ["a", "b"]
        ["d", "c", "a", "b"],  # exptected ["d", "c", "a", "b"]
    ]
    invertedIndex = {
        "a": [0, 1],
        "b": [0, 1, 2],
        "c": [0],
    }

    # Remove 1 random word from each sentence
    newList = RandomPrefixFiltering(x)
    print(newList)

    # Remove 1 word from the end of each sentenc
    newListPrefixFiltering = PrefixFiltering(x)
    print(newListPrefixFiltering)

    # sortedLst =SortWithInvertedIndex(lst=lst, invertedIndex=invertedIndex)
    # print(sortedLst)

    # Sort the dataset by the frequency of each word.
    # The result is a dataset in which each sentence has been reordered by ascending word frequency
    sortedX, sortedY = SortWithFrequent(dataset=tuple([x, y]))
    print(sortedX)
    print(sortedY)
