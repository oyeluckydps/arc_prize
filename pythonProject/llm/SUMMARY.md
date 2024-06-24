# Summary of Changes

- Created a function `analyze_images` in `pattern_recog.py` to handle the main logic of reading files, identifying the `total_page.jpg` file, and sending it to Gemini for analysis.
- Created a function `chat_with_gemini` in `chat_with_gemini.py` to handle the chat with Gemini for input grids of both training and test type.
- Removed unnecessary lines of code from `pattern_recog.py`.
- Added comments to the code for better understanding.
- Moved the `chat_with_gemini` function to a new file `chat_with_gemini.py`.
- Updated the `analyze_images` function to create the model and chat session, and pass the chat session to the `chat_with_gemini` function.
- Modified the `chat_with_gemini` function to accept the chat session and directly pass the image to `chat_session.send_message(image)`.
- Removed the `chat_with_gemini` function from `pattern_recog.py`.