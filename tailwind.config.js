module.exports = {
content: ["content/**/*.html", "content/*.html"],
  theme: {
    extend: {
      backgroundImage: {
        'none': "none",
        'hero': "url('/img/hero.jpg')",
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
      },
    },
  },
  plugins: [],
}
