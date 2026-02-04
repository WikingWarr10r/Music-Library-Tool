def levenshtein(a: str, b: str) -> int:
    """Calculates the Levenshtein Distance between two strings.

    This represents the minimum number of insertions, deletions or substitutions to turn string a into string b.
    

    Args:
        a (str): The first string
        b (str): The second string

    Returns:
        int: The distance between a and b
    """
    len_a = len(a)
    len_b = len(b)

    d = [[0] * (len_b + 1) for _ in range(len_a + 1)]

    for i in range(len_a + 1):
        d[i][0] = i
    for j in range(len_b + 1):
        d[0][j] = j

    for i in range(1, len_a + 1):
        for j in range(1, len_b + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1

            d[i][j] = min(
                d[i - 1][j] + 1,
                d[i][j - 1] + 1,
                d[i - 1][j - 1] + cost
            )

    return d[len_a][len_b]

def best_match(word: str, words: list[str]) -> tuple[str, int]:
    """Finds the closest matching word from a list using Levenshtein Distance.

    Args:
        word (str): _description_
        words (list[str]): _description_

    Returns:
        tuple: A tuple containing the word and how close it matches. 
    """
    best_word = None
    best_dist = float("inf")

    for w in words:
        dist = levenshtein(word, w)
        if dist < best_dist:
            best_dist = dist
            best_word = w

    return best_word, best_dist