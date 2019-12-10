<template>
  <div id="app">
    <nav id="app-nav">
      <!-- Navigation bar -->
      <template v-if="this.$route.path !== '/'">
        <router-link class="nav-bar-elem" :to="'/'">Home</router-link>
      </template>
      <template v-if="this.displayLoginRegisterButtons">
        <router-link class="nav-bar-elem" :to="'/login'">Log In</router-link>
        <router-link class="nav-bar-elem" :to="'/register'">Register</router-link>
      </template>
      <router-link class="nav-bar-elem" :to="'/favorites'">Favorites</router-link>
      <router-link class="nav-bar-elem" :to="'/advanced'">Movie Names</router-link>
      <template v-if="this.loggedIn">
        <button class="nav-bar-elem" @click="logout()">Log Out</button>
      </template>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'app',
  data() {
    return {
      userInSession: '',
      loggedIn: false
    }
  },
  methods: {
    login(user, pass) {
      // logs user in and redirects to home
      axios.post('/login', {username: user, password: pass})
        .then((resp) => {
          if (!resp.data.success){
            this.$router.go();
            return;
          }
          this.loggedIn = true;
          this.$router.push('/');
        });
    },
    logout(){
      // logs user out and redirects to home or refreshes if already on homepage
      axios.post('/logout', {user: this.userInSession})
      this.loggedIn = false;
      if (this.$route.path == '/'){
        this.$router.go();
        return;
      }
      this.$router.push('/');
    },
    async testUserInSession() {
      /* hits backend and checks to see if a user is in session - adjusts this.loggedIn accordingly
      this ensures that the correct navbar buttons are displayed at all times */
      let promise = axios.post('/users')
        .then((resp) => {
          this.loggedIn = resp.data.success;
          this.userInSession = resp.data.userInSession || this.userInSession;
          return resp.data.success;
        })
      // these lines ensure that the promise resolves before adjusting the value of this.loggedIn (accounts for asynch)
      return await promise;
    }
  },
  computed: {
    displayLoginRegisterButtons(){
      // determines if login or register buttons should be shown based on current path and this.loggedIn status
      return this.$route.path !== '/login' && !this.loggedIn;
    }
  },
  mounted() {
    this.testUserInSession()
  }
}
</script>

<style>
#app {
  margin: 10%;
  padding: 20px;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
nav#app-nav {
  display: flex;
  border-top: 1px #2c3e50 solid;
  border-bottom: 1px #2c3e50 solid;
  flex-direction: row;
  justify-content: center;
  padding: 10px;
}
button,
nav#app-nav .nav-bar-elem {
  margin: 0 10px;
  color: #2c3e50;
  background-color: #c9dbba;
  text-transform: uppercase;
  padding: 5px;
  border: 2px solid #2c3e50;
  border-radius: 6px;
  display: inline-block;
  transition: all 0.3s ease 0s;

  text-decoration: none;
}
button:hover,
nav#app-nav .nav-bar-elem:hover {
  margin: 0 10px;
  background-color: #b2c6a1;
  color: #2c3e50;
  border-radius: 50px;
  border-color: #2c3e50;
  transition: all 0.3s ease 0s;
}
</style>
