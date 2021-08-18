<script>
  import Button, { Label, Icon } from '@smui/button';
	import MdFavorite from 'svelte-icons/md/MdFavorite.svelte'
	import Ripple from '@smui/ripple';
</script>

<style>
	.footer {
		margin-top: 2em;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 10px;
		font-family: 'Roboto', sans-serif;
		font-weight: 300;
 }
	
  .icon {
    width: 24px;
		height: 24px;
		color: #ff8a80;
		left: 50% !important;
		margin-left: 0.5em;
  }
</style>

<div class="footer" use:Ripple={{ surface: true, color: 'secondary' }}>
	<span>Powered by the <a href="https://github.com/osori/korean-romanizer" target="_blank">korean-romanizer</a> library</span><div class="icon">
		<MdFavorite />
	</div>
</div>