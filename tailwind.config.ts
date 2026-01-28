import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'azure-blue': '#0078D4',
        'azure-light': '#50E6FF',
        'azure-dark': '#004578',
      },
    },
  },
  plugins: [],
}
export default config
