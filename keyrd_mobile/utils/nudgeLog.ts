// Simple logger — replace with actual DB write or analytics call
export async function logPush(entry: {
  userId: string;
  context: number[];
  action: string;
  timestamp: number;
}) {
  console.log('[NudgeLog]', entry);
}
