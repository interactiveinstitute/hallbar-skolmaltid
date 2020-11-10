const routes = [
  {
    path: '/',
    component: () => import('layouts/HomeLayout.vue'),
    children: [
      {
        name: 'Home',
        path: '',
        component: () => import('pages/PageLogin.vue')
      },
      {
        name: 'Logout',
        path: 'loggaut',
        component: () => import('pages/PageLogout.vue')
      }
    ]
  },
  {
    path: '/app',
    component: () => import('layouts/AppLayout.vue'),
    children: [
      {
        name: 'AppHome',
        path: '',
        component: () => import('pages/PageIndex.vue')
      },
      {
        name: 'AppBoards',
        path: 'oversikt',
        component: () => import('pages/PageDashboard.vue')
      },
      {
        name: 'AppSettings',
        path: 'installningar',
        component: () => import('pages/PageSettings.vue')
      },
      {
        name: 'AppBoard',
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
