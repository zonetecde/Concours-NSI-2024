<script>
	import { Toaster } from 'svelte-french-toast';
	import '../app.css';
</script>

<div class="overflow-x-hidden">
	<Toaster />
	<slot />
</div>
