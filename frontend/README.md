# RoastNotes 🌱☕️

RoastNotes is your digital corner in a cozy Roman café—a place where coffee enthusiasts can track, rate, and share their coffee roasting experiences. Built with the warmth of an Italian coffee house and the precision of a master roaster.

## Features ✨

- **Personal Roast Journal**: Track your coffee roasts with detailed information about origins, roast levels, and tasting notes
- **Collaborative Tasting**: Create groups to share and compare roasting experiences with fellow coffee enthusiasts
- **Roaster Directory**: Maintain a curated list of your favorite coffee roasters
- **Detailed Ratings**: Record brewing methods, ratios, temperatures, and tasting notes for each coffee experience
- **Beautiful Interface**: Clean, intuitive design that feels as welcoming as your favorite café

## Tech Stack 🛠

- **Frontend**: SvelteKit
- **Styling**: TailwindCSS with custom coffee-inspired theme
- **Authentication**: Token-based authentication
- **Design**: Mobile-responsive with a focus on usability

## Getting Started 🚀

### Prerequisites

- Node.js (latest LTS version recommended)
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd roastnotes/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Development 🔧

### Project Structure

- `/src/lib/components/` - Reusable Svelte components
- `/src/lib/server/` - Server-side utilities and API handlers
- `/src/routes/` - SvelteKit routes and pages
- `/src/lib/stores/` - Svelte stores for state management
- `/src/lib/types/` - TypeScript type definitions

### Key Components

- `RoastCard.svelte` - Display individual roast entries
- `GroupRoastCard.svelte` - Show group tasting experiences
- `AddRatingModal.svelte` - Interface for adding roast ratings
- `SearchableDropdown.svelte` - Reusable search component

## Contributing 🤝

We welcome contributions! Whether it's a bug fix, new feature, or documentation improvement, feel free to make a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Design Philosophy 🎨

RoastNotes embraces the essence of an Italian coffee house—cozy, laid back, yet vibrantly clean. The interface is designed to be unpretentious while maintaining the sophistication needed for serious coffee enthusiasts.

## License 📝

[Your License Here]

---

Built with ❤️ and ☕️ by coffee lovers, for coffee lovers.
