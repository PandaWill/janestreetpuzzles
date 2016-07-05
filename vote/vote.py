"""
https://www.janestreet.com/puzzles/get-out-the-vote/
"""
from __future__ import print_function
from __future__ import division


def solution():
    total_votes = 102
    delegates = 7

    all_possible_results = [
        [i, j, k]
        for i in range(0, total_votes + 1)
        for j in range(0, total_votes + 1)
        for k in range(0, total_votes + 1)
        if i + j + k == total_votes
    ]

    possible_round1_results = [result for result in all_possible_results if is_correct(result, [2, 2, 3], delegates)]

    delegates += 1

    for result in possible_round1_results:
        result[0] += 1

        if is_correct(result, [1, 4, 3], delegates) or \
                is_correct(result, [1, 3, 4], delegates) or \
                is_correct(result, [1, 2, 5], delegates):
            print(result)


def is_correct(votes_per_candidate, required_delegate_result, num_delegates):
    return get_delegate_results(votes_per_candidate, num_delegates) == required_delegate_result


def get_delegate_results(votes_per_candidate, num_delegates):
    total_votes = sum(votes_per_candidate)

    delegate_result = [(num_delegates * votes) // total_votes for votes in votes_per_candidate]

    remainders = [0, 1, 2]
    remainders.sort(key=lambda x: (num_delegates * votes_per_candidate[x]) % total_votes, reverse=True)

    delegates_left_over = num_delegates - sum(delegate_result)

    assert delegates_left_over < 3

    for i in remainders[0:delegates_left_over]:
        delegate_result[i] += 1

    return delegate_result


if __name__ == "__main__":
    solution()
