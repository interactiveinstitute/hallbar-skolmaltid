
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { name: 'Home', path: '', component: () => import('pages/Index.vue') },
      { name: 'Dashboard', path: 'oversikt', component: () => import('pages/Dashboard.vue') },
      { name: 'Settings', path: 'installningar', component: () => import('pages/Settings.vue') }
    ]
  }
];

// Always leave this as last one
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '*',
    component: () => import('pages/Error404.vue')
  });
}

export default routes;
