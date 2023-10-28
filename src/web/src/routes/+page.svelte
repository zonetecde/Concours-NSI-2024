<script>
    import { Router, Link, Route } from "svelte-routing";
    import About from './About.svelte'
    import Main from './Main.svelte'

  
    export let url = "";
  </script>
  
  <Router url="{url}">
    <nav>
      <Link to="/">Home</Link>
      <Link to="about">About</Link>
    </nav>
    <div>
      <Route path="about" component="{About}" />
      <Route path="/"><Main></Main></Route>
    </div>
  </Router>