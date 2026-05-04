// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  // Sitenin tam adresi (Sitemap linkleri için zorunlu)
  site: 'https://ai-decoder.vercel.app', 
  integrations: [sitemap()]
});