const { chromium } = require('playwright');
const views = process.argv.slice(2);
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl'] });
  for (const v of views) {
    const p = await b.newPage({ viewport: { width: 1800, height: 1100 } });
    p.on('console', m => console.log('console:', m.text()));
    p.on('pageerror', e => console.log('pageerror:', e.message));
    await p.goto('http://127.0.0.1:8765/scene.html?v=' + v);
    try { await p.waitForFunction('window.__done===true', { timeout: 240000 }); } catch (e) { console.log('timeout view', v); }
    await p.screenshot({ path: '/home/user/Digitalissimo/piantina/render_vista' + v + '.png' });
    await p.close();
  }
  await b.close();
})();
