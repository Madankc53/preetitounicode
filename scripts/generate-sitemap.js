const fg = require('fast-glob');
const fs = require('fs');

const base = (process.env.BASE_URL || '').replace(/\/+$/,'');
if (!base) {
  console.error('ERROR: BASE_URL not set. Set SITE_BASE_URL secret to your site URL (e.g. https://example.com).');
  process.exit(1);
}

(async () => {
  // adjust the glob to match where your published HTML files live (e.g. "public/**/*.html")
  const files = await fg(['**/*.html', '!node_modules/**', '!.github/**', '!scripts/**'], { dot: false });

  const urls = files
    .map(f => f.replace(/index\.html$/, ''))        // convert /foo/index.html -> /foo/
    .map(p => p.replace(/\\/g, '/'))                // windows paths
    .map(p => {
      const trimmed = p.replace(/^\/+|\/+$/g, '');
      return base + (trimmed ? '/' + trimmed : '/') ;
    })
    // dedupe and normalize trailing slash
    .filter((v,i,arr) => arr.indexOf(v) === i)
    .map(u => u.replace(/\/+$/,'') + '/'); // ensure trailing slash

  const xml =
    '<?xml version="1.0" encoding="UTF-8"?>\n' +
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    urls.map(u => `  <url><loc>${u}</loc></url>`).join('\n') +
    '\n</urlset>\n';

  fs.writeFileSync('sitemap.xml', xml, 'utf8');
  console.log(`Wrote sitemap.xml with ${urls.length} URLs`);
})();
