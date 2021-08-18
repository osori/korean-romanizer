<script>
  import Textfield from '@smui/textfield';
  import HelperText from '@smui/textfield/helper-text/index';
	import LayoutGrid, { Cell } from '@smui/layout-grid';
	import CharacterCounter from '@smui/textfield/character-counter/index';
	import Button, { Label } from '@smui/button';

	import TopBar from './TopBar.svelte';
	import Romanizer from './Romanizer.svelte';
	import Footer from './Footer.svelte';
	
	import "./smui.css";
</script>

<style>
	@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR&family=Roboto:wght@300;500;900&display=swap');

	.container{
		margin: 0 auto;
		width: 80%;
	}

	@media screen and (min-width: 480px) {
			.centered {
						margin: 0 auto;
						width: 95%;
					}
	 }
</style>

<svelte:head>
	<title>Korean Romanizer</title>
	<html lang="en" />
</svelte:head>

<div class="container">
	<TopBar />
	<Romanizer />
	<Footer />
</div>