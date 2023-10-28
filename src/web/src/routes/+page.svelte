<script>
	import Api from '../api/Api';
</script>

<button
	on:click={() => {
		/**
		 * Appel la méthode `getThingFromPython` de l'objet Api de python
		 */
		Api.api.getThingFromPython().then(
			/** 
			 @param {*} e 
			*/
			(e) => {
				window.alert(e.aaa);
			}
		);
	}}>Test me</button
>
