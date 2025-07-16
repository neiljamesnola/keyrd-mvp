// Minimal mock LinUCB agent for testing
const linucbAgent = {
  selectAction: (context: number[]): string => {
    // Replace with real LinUCB logic
    const actions = ['Eat fruit', 'Drink water', 'Go for walk'];
    return actions[Math.floor(Math.random() * actions.length)];
  },
};

export default linucbAgent;
