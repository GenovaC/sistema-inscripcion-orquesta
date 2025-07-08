// tu_proyecto/theme/static_src/tailwind.config.js

/** @type {import('tailwindcss').Config} */
module.exports = {
  // 🚨 MUY IMPORTANTE: Asegúrate de que estas rutas sean correctas
  // para que Tailwind escanee tus archivos HTML/JS en busca de clases.
  // Las rutas son relativas a la raíz de tu proyecto de Django.
  content: [
    './templates/**/*.html',           // Para plantillas en la carpeta 'templates' de la raíz del proyecto
    './**/templates/**/*.html',        // Para plantillas dentro de subdirectorios 'templates' de tus apps,
    './**/templates/*.html',        // Plantilla del base.html
    './**/static/**/*.js',             // Si tienes archivos JS que añaden clases de Tailwind
    // Añade aquí cualquier otra ruta donde uses clases de Tailwind, por ejemplo:
    // './node_modules/flowbite/**/*.js', // Si usas Flowbite u otras librerías JS
  ],
  theme: {
    extend: {
      // Aquí puedes extender el tema por defecto de Tailwind
      // Por ejemplo, añadir colores personalizados:
      // colors: {
      //   'rosa-sistema': '#FF007F',
      // },
      // O fuentes personalizadas:
      // fontFamily: {
      //   'custom-font': ['YourCustomFont', 'sans-serif'],
      // },
    },
  },
  plugins: [
    // Aquí puedes añadir los plugins de Tailwind CSS que uses, por ejemplo:
    // require('@tailwindcss/forms'),
    // require('@tailwindcss/typography'),
    // require('flowbite/plugin'), // Si estás usando Flowbite
  ],
}