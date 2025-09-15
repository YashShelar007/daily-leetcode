class Solution:
    def canBeTypedWords(self, text: str, brokenLetters: str) -> int:
        """
        LC 1935. Maximum Number of Words You Can Type

        Idea:
          - Split text into words.
          - For each word, check if it contains any broken letter.
          - If not, it is typeable; count it.

        Time Complexity:  O(n * m)  
          - n = number of words, m = len(brokenLetters)
        Space Complexity: O(1) extra (ignoring input storage).
        """
        wordList = text.split(' ')
        count = 0
        for word in wordList:
            for char in brokenLetters:
                if char in word:
                    break
            else:
                count += 1
        return count
