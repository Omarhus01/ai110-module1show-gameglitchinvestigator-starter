# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game it looked like a normal working guessing game — there was a text input, a submit button, a difficulty selector, and a score display. Nothing looked obviously wrong at a glance. It was only after opening the Developer Debug Info panel to see the secret number that I started noticing things were off. The hints were telling me the wrong direction, difficulty changes did not reset the round, and the game accepted inputs that should have been rejected.

- What did the game look like the first time you ran it?
  - The game appeared to work normally on the surface: the UI loaded, the difficulty selector showed three options, and the guess input accepted text. There were no error messages or crashes. Without using the debug panel to reveal the secret number, it was not obvious anything was broken.

- List at least two concrete bugs you noticed at the start:
  - **Bug 1 — Hints are backwards:** I used the debug panel to find the secret number, then entered a number that was *lower* than the secret. I expected the hint to say "Go Higher," but instead the game said "Go LOWER." The hint logic in `check_guess` has the directions swapped: `guess > secret` triggers the "Go HIGHER!" message and `guess < secret` triggers "Go LOWER!" — the opposite of what they should be.
  - **Bug 2 — Changing difficulty does not reset the game:** I expected switching from Normal to Hard to start a fresh round with a new secret number and a reset attempt counter. Instead, the old secret and attempt count carried over from the previous difficulty. The only way to get a clean reset was to refresh the entire page.
  - **Bug 3 — Negative numbers are accepted without any error:** I typed `-5` as a guess and the game processed it as a valid input. I expected an error message telling me the guess must be within the valid range (e.g., 1–100), but none appeared. The `parse_guess` function only checks whether the input is a number — it never checks if the number falls within the allowed range.
  - **Bug 4 — Hard difficulty is actually easier than Normal:** I expected Hard to be harder than Normal, so I assumed it would have a bigger range of numbers to guess from. But after Claude Code read through the code, it pointed out that Hard uses a range of 1–50 while Normal uses 1–100, meaning Hard is actually easier. I wouldn't have caught this just by playing since the range isn't obvious unless you look at the code directly.
  - **Bug 5 — The secret number turns into a string every other guess:** This one I had no idea about until Claude Code analyzed the code. On every even-numbered attempt, the secret number gets converted to a string before being compared to my guess. So the game stops doing a proper number comparison and starts comparing text instead — which means a guess like `9` could be told it's "Too High" compared to `"50"` just because `"9"` comes after `"5"` alphabetically. This made the hints randomly wrong on every second guess without any obvious reason.

---

## 2. How did you use AI as a teammate?

I used Claude Code (Anthropic's AI coding assistant) throughout this project to help me read the code, identify bugs, explain confusing logic, and make fixes. It was helpful for catching things I wouldn't have spotted just by playing the game, especially bugs that only show up when you actually read the source code.

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - I used **Claude Code** as my primary AI tool throughout the project.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - Claude Code correctly identified that the hints in `check_guess` were reversed. It read the function and pointed out that `guess > secret` was returning "Go HIGHER!" when it should say "Go LOWER!" — and vice versa. I verified this by opening the Developer Debug Info panel to see the secret number, then submitting a guess that was clearly lower than it. The old code told me to go lower when I was already below the target, which confirmed the bug. After the fix, I ran the same test and the hint correctly said "Go HIGHER!" I also verified it passed in pytest with `test_hint_message_too_high` and `test_hint_message_too_low`.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - When I asked Claude Code to explain why the existing pytest tests were failing, it initially described the issue as the tests "not importing correctly." That was misleading — the real problem was that `check_guess` returns a tuple `(outcome, message)` but the tests were comparing the full result against a plain string like `"Win"`. I verified this by reading the actual error output from pytest, which showed `assert ('Win', '🎉 Correct!') == 'Win'` — clearly a tuple vs string mismatch, not an import issue.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I used two checks: first I ran `pytest` to confirm the relevant test passed, then I ran the live app with `streamlit run app.py` and manually tested the same scenario that originally showed the bug. If both passed, I considered the fix verified.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
  - I ran the full pytest suite after fixing the reversed hints and refactoring the functions into `logic_utils.py`. Before the fix, all 3 existing tests failed because they were comparing against plain strings while `check_guess` returns a tuple. After fixing the tests to unpack the tuple and adding new tests for the hint messages, all 7 tests passed. This showed me that the refactor didn't break anything and that the hint logic was now correct.

- Did AI help you design or understand any tests? How?
  - Yes — Claude Code wrote the new test cases for me after I described what the bugs were. It suggested checking not just the outcome string (like "Too High") but also the message content (checking that "LOWER" appears in the message when the guess is too high). That was a more thorough way to test the fix than I would have thought of on my own, since it directly tests the part that was actually broken.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
  - Every time you interact with anything in a Streamlit app — clicking a button, typing in a field — the entire Python script reruns from the top. In the original app, the secret number was generated with `random.randint()` at the top level of the script with no protection, so every rerun picked a new random number. The target was literally changing on every click, making it impossible to win.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  - Imagine every time you click a button on a webpage, the whole page reloads and forgets everything — your form data, your progress, everything. That's what Streamlit does by default. Session state is like a small notebook that survives those reloads. You write something into it once, and it stays there no matter how many times the page reruns. So instead of generating a new secret number on every rerun, you check the notebook first — if there's already a number there, use it; if not, generate one and write it down.

- What change did you make that finally gave the game a stable secret number?
  - The fix was already in place using `if "secret" not in st.session_state` before generating the number. This means the secret is only generated once — the very first time the app runs. On every rerun after that, the condition is False so it skips the `random.randint()` call and keeps using the existing value stored in session state.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - Reading the code before trusting it. The game looked fine from the outside but had multiple bugs that were only visible in the source. Going forward I want to make it a habit to actually read through any AI-generated code line by line before assuming it works, especially for logic that involves comparisons or state management.

- What is one thing you would do differently next time you work with AI on a coding task?
  - I would verify AI explanations against the actual error output immediately instead of taking them at face value. When Claude Code described the failing tests as an import issue, I spent a moment confused before checking the real pytest output myself. Reading the error message directly was faster and more accurate than the AI's first explanation.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - I used to assume that if AI-generated code ran without crashing, it was probably correct. This project showed me that code can run fine on the surface while having multiple logical bugs underneath — and that the AI that wrote the broken code can also be the tool that helps you find and fix those same bugs, as long as you stay in the driver's seat and verify everything yourself.
