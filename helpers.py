def levenshtein(a, b):
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

def best_match(word, words):
    best_word = None
    best_dist = float("inf")

    for w in words:
        dist = levenshtein(word, w)
        if dist < best_dist:
            best_dist = dist
            best_word = w

    return best_word, best_dist