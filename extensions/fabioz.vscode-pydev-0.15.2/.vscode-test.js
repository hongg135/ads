const { defineConfig } = require("@vscode/test-cli");

module.exports = defineConfig({ files: ["outTests/**/*.test.js"] });
