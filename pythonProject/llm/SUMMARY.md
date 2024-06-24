# Summary of Changes

- Created a function `analyze_images` in `pattern_recog.py` to handle the main logic of reading files, identifying the `total_page.jpg` file, and sending it to Gemini for analysis.
- Created a function `chat_with_gemini` in `pattern_recog.py` to handle the chat with Gemini for input grids of both training and test type.
- Removed unnecessary lines of code from `pattern_recog.py`.
- Added comments to the code for better understanding.
- Created an `__init__.py` file in the root folder to mark the directory as a Python package.
- Added a new file `snapshot.py` in the current working directory with a function `get_snapshots` to get snapshots of all grids.