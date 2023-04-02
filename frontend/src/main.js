import '@babel/polyfill';
import 'mutationobserver-shim';
import Vue from 'vue';
import './plugins/bootstrap-vue';
import App from './App.vue';
import './registerServiceWorker';
import router from './router';

import VueTailwind from 'vue-tailwind';

import { TModal } from 'vue-tailwind/dist/components';

const components = {
	TModal,
};

Vue.use(VueTailwind, components);
Vue.config.productionTip = false;
new Vue({
	router,
	render: (h) => h(App),
}).$mount('#app');
