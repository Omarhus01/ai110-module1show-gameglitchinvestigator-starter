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

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
