// File: app/utils/push.ts

import { buildContextVector } from './context';
import linucbAgent from './linucbAgent'; // Assumes a default export
import { logPush } from './nudgeLog';    // Assume this writes to DB or console

/**
 * Triggers a nudge selection and logs the push.
 * @param userId - The unique identifier for the user.
 * @returns The selected nudge action.
 */
export async function selectAndSendNudge(userId: string): Promise<string> {
  try {
    // Step 1: Build context vector (e.g., [steps, sleep, mood, timeOfDay, etc.])
    const context = await buildContextVector(userId);

    // Step 2: Select action via LinUCB
    const action = linucbAgent.selectAction(context);

    // Step 3: Log action in NudgeLog
    await logPush({ userId, context, action, timestamp: Date.now() });

    // Step 4: Return selected nudge
    return action;
  } catch (err) {
    console.error('[push.ts] Error selecting or sending nudge:', err);
    throw err;
  }
}
