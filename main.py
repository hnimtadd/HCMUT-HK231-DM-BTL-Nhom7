from sort import SortWithInvertedIndex

if __name__ == "__main__":
    lst = [
        ["c", "b", "a"], # expected ["c", "a", "b"]
        ["a", "b"], # expected ["a", "b"]
        ["b", "c"],  # expected ["c", "b"]
        ["b", "c","d"],  # expected ["d","c", "b"]
    ]
    invertedIndex = {
        "a": [0,1],
        "b": [0,1,2],
        "c": [0,]
    }
    lst =SortWithInvertedIndex(lst=lst, invertedIndex=invertedIndex)
    print(lst)
