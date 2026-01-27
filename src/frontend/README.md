# AiBot Frontend (Vue Version)

This is a migration of the AiBot frontend project from React to Vue 3.

## Project Structure

- `src/`
  - `assets/`: Static assets and global styles (Tailwind CSS)
  - `components/`: Reusable components (e.g., NavBar)
  - `router/`: Vue Router configuration
  - `views/`: Page components (migrated from React pages)
  - `App.vue`: Main application component
  - `main.js`: Application entry point

## Tech Stack

- **Framework**: Vue 3 (Composition API)
- **Routing**: Vue Router 4
- **Styling**: Tailwind CSS
- **Build Tool**: Vite
- **Icons**: Remix Icon & Font Awesome (via CDN)

## Setup & Run

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Build for production:
   ```bash
   npm run build
   ```

## Migration Notes

- All pages have been migrated to `src/views/`.
- The `NavBar` component is used in each view to match the original layout.
- Tailwind CSS configuration has been preserved to ensure consistent styling.
- Routing paths match the original React application.
