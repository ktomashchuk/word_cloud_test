import threading
import os
import re
from collections import Counter


class WordCloud:

    total_counter = Counter()

    def read_file(self, file):
        # Open file
        with open(file, 'r') as f:
            # Read each line, remove special characters and count words
            for line in f:
                new_line = re.sub('\W+', ' ', line)
                counter = Counter(new_line.split())
                self.total_counter += counter

    def create_file(self):
        # Remove words with less than 2 appearances and sort by most common
        two_or_more = Counter(
            {w: c for w, c in self.total_counter.items() if c > 1}
        ).most_common()
        # Count the number of appearances of the most common word
        most_common = two_or_more[0][1] if two_or_more else 0
        with open('result.html', 'w') as f:
            for word, count in two_or_more:
                # Word is most frequent
                if count == most_common:
                    f.write(f"<h1>{word.lower()}: {count}</h1> \n")
                # Word is > 60% of most frequent
                elif count >= (most_common * 0.6):
                    f.write(f"<h3>{word.lower()}: {count}</h3> \n")
                # Word is > 30% of most frequent
                elif count >= (most_common * 0.3):
                    f.write(f"<h5>{word.lower()}: {count}</h5> \n")
                else:
                    f.write(f"<p><small>{word.lower()}: {count}</small><p> \n")


if __name__ == "__main__":
    # Create an instance of word cloud
    cloud = WordCloud()
    # Find the path to text files
    files_path = os.path.join(os.getcwd(), 'files')
    files = os.listdir(files_path)
    # Create a list of threads to be able to wait for them to finish
    threads = []
    # Create a thread reading each file
    for file in files:
        if file.endswith('.txt'):
            thread = threading.Thread(
                target=cloud.read_file, args=(os.path.join(files_path, file), )
            )
            threads.append(thread)
            thread.start()
    # Wait for all threads reading the files to finish
    while True:
        if not any(thread.is_alive() for thread in threads):
            print('Done!')
            cloud.create_file()
            break

