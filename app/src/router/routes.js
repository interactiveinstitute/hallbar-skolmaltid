const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        name: 'Home',
        path: '',
        component: () => import('pages/PageIndex.vue')
      },
      {
        name: 'Dashboard',
        path: 'oversikt',
        component: () => import('pages/PageDashboard.vue')
      },
      {
        name: 'Settings',
        path: 'installningar',
        component: () => import('pages/PageSettings.vue')
      },
      {
        name: 'Board',
        path: 'brade/:id',
        component: () => import('pages/PageBoard.vue')
      },
      {
        name: 'GunnarTestar',
        path: 'test',
        component: () => import('pages/GunnarTestar.vue')
      }
    ]
  }
];

// Always leave this as last one
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '*',
    component: () => import('pages/PageError404.vue')
  });
}

export default routes;
