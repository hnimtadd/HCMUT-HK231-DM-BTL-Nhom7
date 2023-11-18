def evaluate(y_hat: list[tuple[int,int]], y: list[tuple[int,int]]) -> tuple[float, float, float]:
    """ Return: 3 values respectively
    1. percentage of true predictions over all predictions
    2. percentage of false predictions over all predictions
    3. percentage of true predictions over ground truth
    """
    if len(y_hat) == 0:
        print("result empty")
        return (0.0, 0.0, 0.0)
    t, f = 0,0
    for res in y_hat:
        if res in y:
            t += 1
        else:
            f += 1
    return (round(float(t/len(y_hat)),4), round(float(f/len(y_hat)),4), round(float(t/len(y)),4))