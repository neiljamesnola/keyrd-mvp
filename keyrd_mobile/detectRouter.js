// File: detectRouter.js

const fs = require('fs');
const path = require('path');

function hasDirectory(base, dir) {
  return fs.existsSync(path.join(base, dir));
}

const root = process.cwd();
const usesAppRouter = hasDirectory(root, 'app');
const usesPagesRouter = hasDirectory(root, 'pages');

console.log('\n🔍 Router Detection Results:\n');
if (usesAppRouter) {
  console.log('✅ App Router detected (found "app" directory)');
}
if (usesPagesRouter) {
  console.log('✅ Pages Router detected (found "pages" directory)');
}
if (!usesAppRouter && !usesPagesRouter) {
  console.log('⚠️  No "app" or "pages" directory found — cannot determine routing style.');
}
