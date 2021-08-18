<script>
  import Textfield from '@smui/textfield';
  import HelperText from '@smui/textfield/helper-text/index';
	import LayoutGrid, { Cell } from '@smui/layout-grid';
	import CharacterCounter from '@smui/textfield/character-counter/index';
	import Button, { Label } from '@smui/button';
	
	import TopBar from './TopBar.svelte';
	import Romanizer from './Romanizer.svelte';
	import Footer from './Footer.svelte';
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR&family=Roboto:wght@300;500;900&display=swap');
</style>

<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/svelte-material-ui@4.0.0/bare.min.css"
/>

<div>
	<TopBar />
	<Romanizer />
	<Footer />
</div>