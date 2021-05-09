"""
Pierre-Charles Dussault
April 29, 2021

Tool to return the longest palindrome(s) substring(s) inside a given string.
Made strictly without the use of any outside resources whatsoever. Only by
sketching with a pencil and paper.
"""


def reverse_string(my_string):
    """Reverse order all the characters in a string."""
    return my_string[::-1]


def is_it_palindrome(my_string):
    for i in range(len(my_string) // 2):
        if my_string[i] != my_string[-i-1]:
            return False

    return True


def gather_substring_by_range(string, start, finish_exclusive):
    """Gather a substring from a string, with a starting index position, and,
    exclusively, an ending index position."""
    gathered_substring = ""
    for k in range(start, finish_exclusive):
        gathered_substring += string[k]

    return gathered_substring


def evaluate_palindromes(string, palindromes):
    """Evaluate if string is palindrome. Then evaluate it against the current
    palindrome(s)."""
    eval_str_len = len(string)
    current_longest_pal_len = len(palindromes[0])
    greater_flag = False
    equal_flag = False

    if is_it_palindrome(string):
        if eval_str_len > current_longest_pal_len:
            greater_flag = True
        elif eval_str_len == current_longest_pal_len:
            equal_flag = True
            for each_pal in palindromes:
                if string == each_pal:
                    equal_flag = False

    if greater_flag:
        palindromes = [string]
    elif equal_flag:
        palindromes.append(string)

    return palindromes


def palindrome_even_search(my_string):
    """Do an even-number sized search for the longest palindrome inside a given
    string. Return the palindrome as a string if one is found. If none are
    found, return 'None'."""
    str_len = len(my_string)
    # Make it into a list, in case multiple palindromes have the same length.
    current_longest_pal = [""]
    # For each index position inside the string.
    for i in range(str_len-1):
        # Iterate to find each possible string starting from the current index
        # as the string STARTING point.
        j = 0
        while((i-j) >= 0 and (i+j) < (str_len-1)):
            start_index = i - j
            finish_index_exclusive = i + j + 2
            evaluated_string = \
                gather_substring_by_range(my_string, start_index,
                                          finish_index_exclusive)

            current_longest_pal = evaluate_palindromes(evaluated_string,
                                                       current_longest_pal)

            j += 1

    return current_longest_pal


def palindrome_odd_search(my_string):
    """Do an odd-number sized search for the longest palindrome inside a given
    string. Return the palindrome as a string if one is found. If none are
    found, return a list containing an empty string."""
    str_len = len(my_string)
    # Make it into a list, in case multiple palindromes have the same length.
    current_longest_pal = [""]
    # For each index position inside the string.
    for i in range(1, str_len-1):
        # Iterate to find each possible string, starting from the current index
        # as the string CENTER point (it contains an odd number of characters).
        j = 1
        while((i-j) >= 0 and (i+j) < str_len):
            start_index = i - j
            finish_index_exclusive = i + j + 1
            evaluated_string = gather_substring_by_range(
                                                        my_string,
                                                        start_index,
                                                        finish_index_exclusive)

            current_longest_pal = evaluate_palindromes(evaluated_string,
                                                       current_longest_pal)

            j += 1

    return current_longest_pal


def longest_palindrome(my_string):
    """Return the longest palindrome inside a string, if there is one.
    Otherwise return a outputa message indicating that the given string does
    not contain a palindrome."""
    even_palindromes = palindrome_even_search(my_string)
    odd_palindromes = palindrome_odd_search(my_string)

    if even_palindromes == [""] and odd_palindromes == [""]:
        return None

    even_pal_len = len(even_palindromes[0])
    odd_pal_len = len(odd_palindromes[0])
    if even_pal_len > odd_pal_len:
        return even_palindromes
    else:
        return odd_palindromes


def main():
    s = "1eabaabyryb"
    print(longest_palindrome(s))


if __name__ == '__main__':
    main()
