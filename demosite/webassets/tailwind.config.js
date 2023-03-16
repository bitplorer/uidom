module.exports = {
        mode: "jit",
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
                  })
        }
        
        }
}