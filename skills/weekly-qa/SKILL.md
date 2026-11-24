---
name: weekly-qa
description: Run the weekly signed-in QA round on a web app. Scope the round, test the live app in the browser, file findings as backlog cards under a hard cap, report, and set the next round's scope. Use for every QA round the weekly-qa-loop cron fires.
---

# Weekly QA round

Run one QA round. The protocol lives in `~/workspace/studio/QA-LOOP.md`. Read it before each round. This skill is the operable form of that file.

## Before the round

1. Read the last round report in `~/workspace/goals/one-man-studio-operating-system/hidden_files/qa-rounds/`. It names the next round's scope. Use it. If no report exists, the scope is the six Sprint 32 cards (round 1).
2. Write the scope card. It names four things: the area, the journeys, the browser and device, and what is out of scope.
3. Web apps only, for now. The Closet is first.

## The run

1. Sign in to the live app in the cloud browser with the founder's Google account. The password route fails the human check. Google sign-in plus his phone approval works. If the cloud sign-in fails, fall back to his live Chrome through the extension. Notify him before each use of his browser. Never use his browser silently.
2. Test the scope area in depth. Smoke-test the core journeys every round: capture a photo, ask the stylist for a pick, log a pick as worn, open Today, open a trip.
3. If the sign-in approval does not arrive (the founder is away), stop. Record the round as skipped. File no cards. Send no report. The next Friday runs normally.
4. Use the app as a user would. Create test data only through the flows tested. Remove test data at the end, or label it clearly. Never delete his items. Never send messages.

## Findings

1. Give each finding a severity and a size. P0 blocks a core journey. P1 hits a real user often. P2 is a rough edge.
2. The cap is 5 cards per round. This cap is hard. Only P0 and P1 become cards. P2 items go to the parked list.
3. If more than 5 card-worthy items surface, take the top 5 by severity. Park the rest with their severity noted.
4. File each card in the product's BACKLOG.md in the standard format: Problem, In scope, Out of scope, Done looks like, Effort. Add one origin line: "Origin: Weekly QA round, <date>, scope <area>."
5. A finding without a card is not a finding. Cards are filed in the same pass as the round.

## The report

1. Write the round report to `~/workspace/goals/one-man-studio-operating-system/hidden_files/qa-rounds/YYYY-MM-DD.md`. Its first line carries the round status: completed or skipped.
2. The report lists: the date, the scope card, what was tested, every card filed with its number, every parked item, and the next round's scope.
3. Send the report to the Closet chat. Keep it short. Lead with the cards filed.
4. QA cards join the normal queue. A planning walk decides what ships. The round never approves its own cards for a sprint.
