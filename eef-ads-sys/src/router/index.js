import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  // {
  //   path: '/login',
  //   redirect: '/',
  //   component: () => import('@/views/login/index'),
  //   hidden: true
  // },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '首页', icon: 'dashboard' }
    }]
  },
  {
    path: '/campaign',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'CampaignIndex',
        component: () => import('@/views/campaign/index'),
        meta: { title: '活动列表', icon: 'el-icon-s-grid' }
      },
      {
        path: 'edit/:id',
        name: 'CampaignEdit',
        component: () => import('@/views/campaign/edit'),
        hidden: true,
        meta: { title: '编辑活动' }
      },
      {
        path: 'add',
        name: 'CampaignAdd',
        component: () => import('@/views/campaign/add'),
        hidden: true,
        meta: { title: '新增活动' }
      }
    ]
  },
  {
    path: '/zone',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'ZoneIndex',
        component: () => import('@/views/zone/index'),
        meta: { title: '广告位列表', icon: 'el-icon-s-open' }
      },
      {
        path: 'edit/:id',
        name: 'ZoneEdit',
        component: () => import('@/views/zone/edit'),
        hidden: true,
        meta: { title: '编辑广告位' }
      },
      {
        path: 'add',
        name: 'ZoneAdd',
        component: () => import('@/views/zone/add'),
        hidden: true,
        meta: { title: '新增广告位' }
      }
    ]
  },
  {
    path: '/banner',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'BannerIndex',
        component: () => import('@/views/banner/index'),
        meta: { title: '广告列表', icon: 'el-icon-s-help' }
      },
      {
        path: 'edit/:id',
        name: 'BannerEdit',
        component: () => import('@/views/banner/edit'),
        hidden: true,
        meta: { title: '编辑广告' }
      },
      {
        path: 'add',
        name: 'BannerAdd',
        component: () => import('@/views/banner/add'),
        hidden: true,
        meta: { title: '新增广告' }
      }
    ]
  },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
