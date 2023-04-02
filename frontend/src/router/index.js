import Vue from 'vue';
import VueRouter from 'vue-router';
import HomeView from '../views/HomeView.vue';
import CabDetailsView from '../views/CabDetailsView.vue';
Vue.use(VueRouter);

const routes = [
	{
		path: '*',
		redirect: '/home',
	},
	{
		path: '/home',
		name: 'home',
		component: HomeView,
	},
	{
		path: '/cabs',
		name: 'cabDetails',
		component: CabDetailsView,
	},
];

const router = new VueRouter({
	mode: 'history',
	base: process.env.BASE_URL,
	routes,
});


export default router;
