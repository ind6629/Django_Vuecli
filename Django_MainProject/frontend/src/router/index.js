import Vue from "vue";
import Router from "vue-router";
import Home from "@/components/Home";
import Order from "@/components/Order";
import ProductDetail from "@/components/ProductDetail";
import Collection from "@/components/Collection";
import Login from "@/components/Login";
import Register from "@/components/Register";
import UserProfile from "@/components/UserProfile";
import Analysis from "@/components/Analysis";
import Search from "@/components/Search";
import Realtime_Analysis from "@/components/Realtime_Analysis";
Vue.use(Router);

export default new Router({
  routes: [
    { path: "/", name: "Home", component: Home },
    { path: "/Home", name: "Home", component: Home },
    { path: "/Order", name: "Order", component: Order },
    { path: "/ProductDetail", name: "ProductDetail", component: ProductDetail },
    { path: "/Collection", name: "Collection", component: Collection },
    { path: "/Login", name: "Login", component: Login },
    { path: "/Register", name: "Register", component: Register },
    { path: "/UserProfile", name: "UserProfile", component: UserProfile },
    { path: "/Analysis", name: "Analysis", component: Analysis },
    {
      path: "/Realtime_Analysis",
      name: "Realtime_Analysis",
      component: Realtime_Analysis,
    },
    { path: "/Search", name: "Search", component: Search },
  ],
});
