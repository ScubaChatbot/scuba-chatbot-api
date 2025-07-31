
# Dive Tours Chat SPA

A modern React single-page application for a diving tours business, built with Vite, TypeScript, and Tailwind CSS.

## Features
- Hash-based routing (React Router)
- Authentication (mocked OpenID Connect)
- Protected chat page (only accessible when logged in)
- Mock APIs for login and registration
- JWT stored in session storage
- Clean, modern UI with gradient backgrounds and styled inputs
- Responsive design

## Pages
- **Login**: Authenticate with username and password
- **Register**: Create a new account (mocked)
- **Chat**: Protected chat page for authenticated users

## Tech Stack
- React + TypeScript
- Vite
- Tailwind CSS
- React Router (HashRouter)

## Getting Started
1. Install dependencies:
   ```sh
   npm install
   ```
2. Start the development server:
   ```sh
   npm run dev
   ```
3. Open your browser at `http://localhost:5173` (or the port shown in the terminal)

## Project Structure
- `src/pages/` — Login, Register, and Chat pages
- `src/contexts/` — AuthContext for authentication state
- `src/services/` — Mock API and JWT storage helpers
- `src/hooks/` — Custom hooks

## Customization
- UI uses Tailwind CSS for gradients, rounded corners, and shadows
- Easily update colors and styles in `tailwind.config.js`

## License
MIT

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default tseslint.config([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
