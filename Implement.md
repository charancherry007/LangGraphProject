# Task: Refactor SOP Generation Workflow and Implement Streamlit UI

## Objective

Analyze the existing project thoroughly using `Mastercontext.md` as the primary source of truth for the project architecture, workflow, components, constraints, and existing implementation.

Then modify the application to implement the new **Streamlit-based SOP generation workflow** described below.

The implementation must preserve all existing functionality that is not explicitly changed by this task.

---

# 1. First Analyze the Existing Project

Before making any code changes:

1. Read and understand `Mastercontext.md` completely.
2. Inspect the existing project structure.
3. Identify:

   * Current application entry point.
   * Existing UI framework/components.
   * SOP generation workflow.
   * Session/state management.
   * Input textfield implementation.
   * File upload implementation.
   * Session sidebar implementation.
   * New Session implementation.
   * L4Map processing.
   * Market input handling.
   * Process Name input handling.
   * SME question generation logic.
   * SOP generation logic.
   * Existing navigation/routing.
   * Existing prompts/LLM calls.
   * Existing state/context objects.
4. Determine how the current workflow moves from:
   `New Session → Inputs → SOP Generation → SME Questions → SOP`
5. Identify the minimum set of files that need to be modified.
6. Do not unnecessarily rewrite or restructure the project.

### Important

`Mastercontext.md` is the source of truth for understanding the existing system.

Do not assume the architecture.

Do not replace existing functionality with a new implementation unless required.

Before modifying code, understand how the existing implementation works and integrate the new workflow into it.

---

# 2. Remove Existing UI Elements

Remove the following existing UI elements from the application:

### Remove

* Input textfield.
* File upload UI that belongs to the old workflow.
* Session sidebar.

These old controls should no longer appear anywhere in the new application flow.

Do not remove backend functionality that is still required by the new workflow.

---

# 3. Preserve the New Session Prompt

The **New Session prompt must remain intact**.

Whenever the user navigates to the New Session screen/page, the application must display the New Session prompt containing:

### Required inputs

1. **L4Map upload**
2. **Market**
3. **Process Name**
4. Existing/relevant button associated with starting the session/workflow.

The New Session UI should become the primary entry point for starting the SOP generation workflow.

### Expected behavior

When the user navigates away from the New Session screen and later navigates back to it:

* The New Session prompt must still be displayed.
* The L4Map upload control must be available.
* Market input must be available.
* Process Name input must be available.
* The related action/start button must be available.

Do not replace this prompt with the removed input textfield or old file-upload workflow.

---

# 4. New SOP Generation Workflow

The workflow should become:

```text
New Session
    ↓
L4Map Upload
    ↓
Market
    ↓
Process Name
    ↓
Start / Generate
    ↓
SOP Generation
    ↓
SME Questions Generated
    ↓
HALT SOP GENERATION
    ↓
Display SME Questions One by One
    ↓
User Answer / Skip
    ↓
Next SME Question
    ↓
All Questions Answered
    ↓
Resume SOP Generation
    ↓
Generate Final SOP
```

---

# 5. Halt SOP Generation at SME Questions

This is a critical requirement.

When the SOP generation workflow reaches the point where SME questions are generated:

### STOP the SOP generation process.

Do not continue automatically to final SOP generation.

The application must transition into an interactive SME-question phase.

Example:

```text
Generate SOP
      ↓
Generate SME Questions
      ↓
SAVE QUESTIONS TO SESSION STATE
      ↓
STOP
      ↓
WAIT FOR USER INPUT
```

The application must not make assumptions about SME answers.

---

# 6. Display SME Questions One by One

After SME questions are generated, display them to the user **one question at a time**.

Example UI:

```text
SME Question 1 of 5

What is the approval process for this activity?

[ Text Input ]

[Skip]     [Skip All]
```

After the user answers the question:

```text
[Next]
```

or an equivalent action may be used to proceed to the next question.

Then display:

```text
SME Question 2 of 5

...

[ Text Input ]

[Skip]     [Skip All]
```

Continue until all SME questions have been processed.

---

# 7. SME Question Answering Must Be Optional

The user must **not be forced to answer SME questions**.

Provide the following controls:

### Skip

The `Skip` button should:

* Skip the current question.
* Store the question as unanswered/skipped.
* Move to the next SME question.
* Preserve all previously provided answers.

Example:

```text
Question 2

[Answer]

[Skip]
```

Clicking `Skip` should immediately move to Question 3.

---

# 8. Skip All

Provide a `Skip All` button.

When the user clicks `Skip All`:

1. Mark all remaining SME questions as skipped/unanswered.
2. Do not ask the remaining questions.
3. Preserve answers already provided.
4. Resume the SOP generation workflow immediately.
5. Continue to final SOP generation.

Example:

```text
Question 2 of 5

[Answer]

[Skip] [Skip All]
```

If `Skip All` is clicked:

```text
SME Questions
      ↓
Skip remaining questions
      ↓
Collect existing answers
      ↓
Resume SOP Generation
      ↓
Generate Final SOP
```

---

# 9. Resume SOP Generation

Once:

* All SME questions have been answered/skipped,

OR

* The user clicks `Skip All`,

resume the SOP generation process.

The application must not restart the entire workflow from the beginning.

It should resume from the point where SOP generation was halted.

---

# 10. Incorporate SME Answers Into SOP Generation

This is another critical requirement.

Any answers provided by the user must be passed into the SOP generation process and used as additional context.

The final SOP generation context should include:

```text
Original SOP Generation Context
+
L4Map
+
Market
+
Process Name
+
Existing Project Context
+
Generated SME Questions
+
SME Answers
+
Skipped/Unanswered Questions
```

Only questions that have actual answers should contribute answer content.

Skipped questions must not cause fake assumptions.

For example:

```json
{
  "question": "What system is used for approval?",
  "answer": "Salesforce"
}
```

should be incorporated into the SOP-generation prompt/context.

A skipped question could be represented as:

```json
{
  "question": "What system is used for approval?",
  "answer": null,
  "status": "skipped"
}
```

Do not invent an answer for skipped questions.

---

# 11. Session State Management

Because this is a Streamlit application, carefully manage state using Streamlit session state or the project's existing state-management mechanism.

The following information should survive Streamlit reruns:

```text
l4map
market
process_name

sop_generation_status

sme_questions

current_sme_question_index

sme_answers

skipped_questions

skip_all

final_sop
```

Suggested state structure:

```python
st.session_state.sop_workflow = {
    "l4map": None,
    "market": None,
    "process_name": None,
    "status": "new_session",
    "sme_questions": [],
    "current_question_index": 0,
    "sme_answers": {},
    "skipped_questions": [],
    "skip_all": False,
    "final_sop": None
}
```

Adapt this structure to the existing project architecture rather than blindly introducing a duplicate state-management system.

---

# 12. Navigation Behavior

Implement proper Streamlit navigation/state handling.

The application should support navigation without losing the current workflow state.

For example:

```text
New Session
   ↓
Start SOP Generation
   ↓
SME Questions
   ↓
Question 1
   ↓
Question 2
   ↓
...
```

If the user navigates back to New Session:

* The New Session prompt should still be displayed.
* L4Map upload should be available.
* Market input should be available.
* Process Name should be available.
* Existing session state should not be accidentally destroyed unless the user explicitly starts a new session.

Avoid resetting `st.session_state` on every Streamlit rerun.

---

# 13. Streamlit Implementation Requirements

Implement the UI using **Streamlit**.

Use Streamlit-native components where appropriate, such as:

```python
st.file_uploader()
st.text_input()
st.button()
st.session_state
st.container()
st.progress()
st.spinner()
st.markdown()
```

The exact components should follow the existing application's design and architecture.

Do not introduce unnecessary frontend frameworks unless they already exist in the project.

---

# 14. Button State / Workflow Safety

Buttons must not accidentally trigger duplicate SOP generation.

For example:

```text
Start
```

should not cause multiple concurrent generation calls if the user clicks it repeatedly.

Similarly:

* Answer submission should process only the current question.
* Skip should process only the current question.
* Skip All should only execute once.
* SOP generation should resume only once after SME interaction is complete.

Use session state flags where required.

---

# 15. Loading / Progress State

Provide appropriate feedback during long-running operations.

Example:

```text
Generating SME questions...
```

and:

```text
Generating final SOP...
```

Use Streamlit mechanisms such as:

```python
with st.spinner("Generating SME questions..."):
    ...
```

Do not expose internal implementation details to the user.

---

# 16. Error Handling

Implement graceful error handling.

Handle cases such as:

### Missing L4Map

```text
Please upload an L4Map before starting.
```

### Missing Market

```text
Please provide the Market.
```

### Missing Process Name

```text
Please provide the Process Name.
```

### SME generation failure

Display a meaningful error and allow the user to retry.

### Final SOP generation failure

Display an appropriate error and do not lose the SME answers.

The user's SME answers must remain available if final SOP generation fails.

---

# 17. Preserve Existing Functionality

Do NOT unnecessarily modify:

* Existing LLM integration.
* Existing SOP-generation algorithms.
* Existing prompt templates.
* Existing L4Map parsing.
* Existing business logic.
* Existing utilities.
* Existing configuration.
* Existing logging.
* Existing tests.

Only modify them where required to support the new workflow.

If existing code already has functions for:

```text
generate_sme_questions()
generate_sop()
process_l4map()
build_prompt()
```

reuse them instead of creating duplicate implementations.

---

# 18. Prompt Construction

Separate SME question generation from final SOP generation.

Conceptually:

### Phase 1

```text
L4Map
+
Market
+
Process Name
+
Existing Context
        ↓
Generate SME Questions
```

### Phase 2

```text
L4Map
+
Market
+
Process Name
+
Existing Context
+
SME Questions
+
User SME Answers
        ↓
Generate Final SOP
```

The final SOP-generation prompt must explicitly provide the SME answers as additional factual input.

Do not accidentally include UI-specific instructions such as "Skip" in the final SOP-generation prompt.

---

# 19. SME Answer Data Model

Use a structured representation for SME responses.

For example:

```python
[
    {
        "question": "What system is used for this activity?",
        "answer": "Salesforce",
        "status": "answered"
    },
    {
        "question": "Who approves this activity?",
        "answer": None,
        "status": "skipped"
    }
]
```

This makes the information easy to pass into the final SOP-generation prompt.

Adapt the structure to existing project models if they already exist.

---

# 20. UI Requirements

The new UI should be simple and focused.

### New Session

```text
---------------------------------------
            New Session
---------------------------------------

L4Map
[ Upload L4Map ]

Market
[ __________________ ]

Process Name
[ __________________ ]

[ Start SOP Generation ]
```

### SME Questions

```text
---------------------------------------
             SME Questions
---------------------------------------

Question 1 of 5

What is the current approval process?

[ ______________________________ ]

[ Submit Answer ] [ Skip ] [ Skip All ]
```

After answering:

```text
Question 2 of 5
...
```

After the last question:

```text
All SME questions processed.

Generating final SOP...
```

Then display the generated SOP.

---

# 21. Remove Old Session Sidebar

Completely remove the old Session sidebar from the visible application UI.

Search the entire project for:

```text
sidebar
session sidebar
input textfield
file upload
old session
```

and identify all references.

Remove or refactor only the UI/functionality that belongs to the obsolete workflow.

Do not remove functionality that is required by the new L4Map-based New Session workflow.

---

# 22. Testing Requirements

After implementation, verify the following scenarios.

### Scenario 1 — Normal workflow

```text
New Session
→ Upload L4Map
→ Enter Market
→ Enter Process Name
→ Start
→ Generate SME Questions
→ Answer Question 1
→ Answer Question 2
→ ...
→ Final SOP
```

Expected:

* Final SOP is generated.
* SME answers are incorporated.

---

### Scenario 2 — Skip individual questions

```text
Question 1 → Answer
Question 2 → Skip
Question 3 → Answer
Question 4 → Skip
```

Expected:

* Answered questions are incorporated.
* Skipped questions remain unanswered.
* Final SOP generation continues.

---

### Scenario 3 — Skip All

```text
Question 1 → Answer
Question 2 → Skip All
```

Expected:

* Question 1 answer is preserved.
* Remaining questions are skipped.
* Final SOP generation starts immediately.
* Question 1 answer is incorporated.

---

### Scenario 4 — No SME answers

```text
Generate SME Questions
→ Skip All
→ Final SOP
```

Expected:

* SOP is generated using the original context.
* No fake SME answers are created.

---

### Scenario 5 — Navigation

Verify that navigating between application screens does not unexpectedly reset:

```text
L4Map
Market
Process Name
SME Questions
Current Question
SME Answers
Skipped Questions
```

---

### Scenario 6 — Streamlit rerun

Verify that normal Streamlit reruns caused by button interactions do not:

* Restart SOP generation.
* Regenerate SME questions unnecessarily.
* Reset the current SME question.
* Delete existing answers.

---

# 23. Code Quality

Follow the existing project's coding conventions.

Prefer:

* Small reusable functions.
* Clear workflow/state management.
* Type hints where appropriate.
* Meaningful variable names.
* Existing project utilities.
* Existing logging framework.

Avoid:

* Duplicate logic.
* Global mutable state where avoidable.
* Hard-coded business logic.
* Unnecessary refactoring.
* Unrelated dependency changes.

---

# 24. Final Verification

Before considering the task complete:

1. Confirm `Mastercontext.md` was analyzed.
2. Confirm the old input textfield is removed.
3. Confirm the old file upload UI is removed.
4. Confirm the old Session sidebar is removed.
5. Confirm New Session contains:

   * L4Map upload
   * Market
   * Process Name
   * Start/related button
6. Confirm SME questions are generated.
7. Confirm SOP generation HALTS at SME questions.
8. Confirm questions are displayed one at a time.
9. Confirm users can answer questions.
10. Confirm `Skip` works.
11. Confirm `Skip All` works.
12. Confirm SME answers are preserved.
13. Confirm skipped questions are represented correctly.
14. Confirm SOP generation resumes after SME interaction.
15. Confirm SME answers are incorporated into the final SOP prompt.
16. Confirm Streamlit session state survives reruns/navigation.
17. Confirm errors do not destroy collected SME answers.
18. Run all existing tests.
19. Add/update tests for the new workflow where appropriate.
20. Start the Streamlit application and manually validate the complete workflow.

---

# 25. Important Implementation Rule

**Do not simply create a new standalone Streamlit application that ignores the existing project.**

The goal is to **modify and integrate with the existing project**.

Use `Mastercontext.md` and the existing codebase to understand and preserve the current architecture and business logic.

The final implementation should feel like an evolution of the existing application, not a replacement.

---

# Expected Final Deliverable

Provide:

1. Modified project implementation.
2. Updated Streamlit UI.
3. Updated SOP workflow.
4. SME interactive question flow.
5. SME answer integration into SOP generation.
6. Skip / Skip All functionality.
7. Session-state handling.
8. Tests covering the new workflow.
9. A concise summary of:

   * Files changed.
   * What was changed.
   * How the new workflow works.
   * Tests executed and their results.
   * Any assumptions or issues encountered.

Do not modify unrelated parts of the codebase.
