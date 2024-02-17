"""
Docstring for this module you gotta complete later.
"""


class Trie:
    def __init__(self) -> None:
        self.root = {}

    def add_word(self, word: str) -> None:
        current_node = self.root
        for ind, letter in enumerate(word):
            if letter not in current_node:
                current_node[letter] = {"is_word": ind == len(word) - 1}
            current_node = current_node[letter]
        current_node['is_word'] = True

    def has_words_with_prefix(self, prefix) -> bool:
        current_node = self.root
        for letter in prefix:
            if letter not in current_node:
                return False
            current_node = current_node[letter]
        return True

    def has_word(self, word) -> bool:
        current_node = self.root
        for letter in word:
            if letter not in current_node:
                return False
            current_node = current_node[letter]
        return current_node['is_word']


def dfs(
        *,
        row: int, column: int, board: list[list[str]], found_words: list[str],
        used: list[list[bool]] = None, current_string: list[str] = None, trie: Trie(),
) -> None:
    # Initialize None-parameters.
    if used is None:
        used = [[False for _ in row] for row in board]
    if current_string is None:
        current_string = []
    # Update prefix you are checking.
    used[row][column] = True
    current_string.append(board[row][column])
    if trie.has_word(current_string):
        # Add existing word to found words.
        found_words.append("".join(current_string))

    if not trie.has_words_with_prefix("".join(current_string)):
        # Don't do dfs. There aren't any existing words with current_string prefix.
        current_string.pop()
        used[row][column] = False
        return

    cells = [[row + 1, column], [row - 1, column], [row, column + 1], [row, column - 1]]
    for x, y in cells:
        if 0 <= x < len(board) and 0 <= y < len(board[0]):
            if not used[x][y]:
                dfs(row=x, column=y, board=board,
                    current_string=current_string, used=used, found_words=found_words,
                    trie=trie)

    # Clear after dfs.
    current_string.pop()
    used[row][column] = False


def find_all_words(board: list[list[str]], existing_words: list[str]) -> list[str]:
    # Create an empty prefix tree.
    trie = Trie()

    # Add all existing words to prefix tree.
    for word in existing_words:
        trie.add_word(word)

    # Create resulting list. It's gonna be filled inside dfs() calls.
    found_words = []
    for x in range(len(board)):
        for y in range(len(board[0])):
            dfs(row=x, column=y, board=board, found_words=found_words, trie=trie)

    # Return resulting list.
    return list(set(found_words))