/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            fontFamily: {
                'fontFamily': ['Futura', 'sans-serif'] 
              },
            'torea-bay': {
                DEFAULT: '#171F99',
                '50': '#7C83EB',
                '100': '#6B72E9',
                '200': '#4751E3',
                '300': '#242FDE',
                '400': '#1C26BC',
                '500': '#171F99',
                '600': '#101568',
                '700': '#080B37',
                '800': '#010107',
                '900': '#000000'
              },
              'onahau': {
                DEFAULT: '#D2E7FE',
                '50': '#FFFFFF',
                '100': '#FFFFFF',
                '200': '#FFFFFF',
                '300': '#FFFFFF',
                '400': '#FAFCFF',
                '500': '#D2E7FE',
                '600': '#9BCAFD',
                '700': '#64ACFC',
                '800': '#2D8FFA',
                '900': '#0573EA'
              },
              'dawn-pink': {
                DEFAULT: '#F5EEE8',
                '50': '#FFFFFF',
                '100': '#FFFFFF',
                '200': '#FFFFFF',
                '300': '#FFFFFF',
                '400': '#FFFFFF',
                '500': '#F5EEE8',
                '600': '#E4D1C1',
                '700': '#D3B49A',
                '800': '#C29773',
                '900': '#B07A4D'
              },
            
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
