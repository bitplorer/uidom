module.exports = {
    mode: "jit",
    darkMode: "class",
    content: {
        files:[
        "../../apps/*.{html,py}",
        "../../apps/**/*.{html,py}",
        "../../apps/**/**/*.{html,py}",
        "../../apps/**/**/**/*.{html,py}",
        ]
        },
    plugins: [
        require('@tailwindcss/aspect-ratio'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('tailwindcss/colors'),
    ],
    theme: {
        extend: {
            keyframes:{
                ripple:{
                    '0%': {opacity:1, scale:0},
                    '100':{opacity:0, scale:1.5}
                }
            },
            animation:{
                ripple: 'ripple 0.5s linear infinite'
            },
            fontFamily: {
                plex: ['IBM Plex Mono']
            },
        }
    }
    
    }