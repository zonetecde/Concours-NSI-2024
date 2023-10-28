<script>
    import { page } from '$app/stores';
    var currentUrl = window.location.href;
  </script>
  
<h1>{$page.status}: {$page.error.message} {currentUrl}</h1>