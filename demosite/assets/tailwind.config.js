module.exports = {
    mode: "jit",
    darkMode: "class",
    content: {
        files:[
        "../../demosite/*.{html,py}",
        "../../demosite/**/*.{html,py}",
        "../../demosite/**/**/*.{html,py}",
        ]
        },
    plugins: [
        require('@tailwindcss/aspect-ratio'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/typography'),
        require('tailwindcss/colors'),
    ],
    theme: {
        extend: {
            fontFamily: {
                roboto: ["'Roboto'"],
                cursive: ["'Style Script'"],
                oswald: ["'Oswald'"],
                teko: ["'Teko'"],
                cinzel: ["'Cinzel Decorative'"],
                montserrat: ["'Montserrat'"],
            },
            minHeight: (theme) => ({
                ...theme('spacing'),
              }),

            keyframes: {
                'ripple': {
                    'from': {
                        opacity: 1,
                        transform: scale(0),
                    },
                    'to':  {
                        opacity: 0,
                        transform: scale(1.5),
                    }
                }
              },

            animations: {
                'ripple': 'ripple 0.5s linear',
              }
        }
    }
    
    }