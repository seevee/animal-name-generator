<template>
  <div id="advanced">
    <h1>Names From Popular Films</h1>
    <h4>Find names from a list of the top 20 currently trending films.<br>Select a movie here:</h4>
    <select v-model="selectedMovie" @change="displayMovieInfo()">
      <option selected disabled>Choose a Movie</option>
      <option v-for="(movie, index) in moviesResultsObjects" :value="movie" :key="index">{{movie.title}}</option>
    </select>
    <br><br>
    <h1>{{ selectedMovie.title }}</h1><br>
    <div id="selected-movie-container" v-if="selectedMovie">
      <div id="selected-movie-poster">
        <img :src="posterUrl(selectedMovie)">
      </div>
      <div id="selected-movie-info">
        <h2>Character Names</h2>
        <ul>
          <li v-for="(char, index) in selectedMovieCharacterNames" :key="index">{{ char.character }}</li>
        </ul>
      </div>
    </div>  
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'advanced',
  data() {
    return {
      movieId: '',
      movieCharacters: [],
      moviesResultsObjects: [],
      selectedMovie: '',
      selectedMovieCharacterNames: '',
    }
  },
  methods: {
    displayMovieInfo: function() {
      this.selectedMovieCharacterNames = this.selectedMovie.credits.cast;
    },
    discoverMovies: function () {
      axios.post('/trending-movie-names')
        .then((response) => {
          // serve top 20 trending movies
          response.data.results.forEach(movie => {
            //for each movie in the list, access all information about that movie (including cast and characters)
            //I have this split into two post requests because the movie API I'm using requires a more specific
            //search in order to serve cast/characters/credits from movies than the search that allows a user to find trending movies
            //so first one must find trending movies, then search the ID of each of those movies more specifically to access character names
            axios.post('/movie-credits', {movie_id: movie.id})
              .then((response) => {
                //store more specific movie information on each movie to be referenced later
                this.moviesResultsObjects.push(response.data);
              });
          });
        })
    },
    posterUrl: function(movie) {
      return `http://image.tmdb.org/t/p/w300/${movie.poster_path}`;
    }
  },
  mounted() {
    this.discoverMovies();
  }
}
</script>

<style scoped>
h4 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  color: #2c3e50;;
  margin: 5px 10px;
  font-weight: bold;
}
#selected-movie-container {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
}
#selected-movie-info {
  margin: 0 40px;
}
</style>
