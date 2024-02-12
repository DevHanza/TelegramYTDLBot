
def progress_hook(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    percentage_of_completion = bytes_downloaded / total_size * 100
    num_chars = int(percentage_of_completion) // 2  # Scale to 0-50 for simplicity

    # Create a string of '#' characters to represent the portion of the video that's been downloaded
    progress_bar = '█' * num_chars

    # Create a string of ' ' characters to represent the portion of the video that hasn't been downloaded yet
    remaining_bar = ' ' * (50 - num_chars)

    print(f'[{progress_bar}{remaining_bar}] {percentage_of_completion:.2f}% downloaded')
