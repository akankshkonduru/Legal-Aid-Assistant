/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                legal: {
                    navy: '#1e3a8a',
                    gold: '#b45309',
                    bg: '#f8fafc',
                    surface: '#ffffff',
                    text: '#0f172a',
                    muted: '#64748b',
                    border: '#e2e8f0',
                }
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
                serif: ['Merriweather', 'serif'],
            },
        },
    },
    plugins: [],
}
