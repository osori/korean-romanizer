<script>
  import Textfield from '@smui/textfield';
  import HelperText from '@smui/textfield/helper-text/index';
	import LayoutGrid, { Cell } from '@smui/layout-grid';
	import CharacterCounter from '@smui/textfield/character-counter/index';
	import Button, { Label } from '@smui/button';
	
	let inputText = '';
	let romanizedText = '';
	let isRomanizing = false;
	
	const romanize = async () => {
		isRomanizing = true;
		const response = await fetch('api/romanize/?text=' + inputText);
    romanizedText = await response.text();
		isRomanizing = false;
	}
</script>

<LayoutGrid>
	 <Cell spanDevices={{ desktop: 6, tablet: 4, phone: 4 }}>
    <div class="text-field">
			<Textfield
				textarea
				style="width: 100%;"
				input$style="font-family: 'Noto Sans KR', sans-serif;"
				helperLine$style="width: 100%;"
				bind:value={inputText}
				label="Text Input"
				input$maxlength="100"
			>
				<CharacterCounter slot="internalCounter">0 / 100</CharacterCounter>
				<HelperText slot="helper">Enter the word or phrase you want to romanize.</HelperText>
			</Textfield>
		 </div>
  </Cell>
	<Cell spanDevices={{ desktop: 6, tablet: 4, phone: 4 }}>
    <div class="text-field">
			<Textfield
				input$readonly="true"
				input$maxlength="10000"
				input$style="font-family: 'Noto Sans KR', sans-serif;"
				textarea
				style="width: 100%; background-color:whitesmoke; color:#FFF"
				bind:value={romanizedText}
				label="Romanized Result"
			>
			  <CharacterCounter style="visibility: hidden;" slot="internalCounter" />
			</Textfield>
		 </div>
  </Cell>
	
	<Cell spanDevices={{ desktop: 3, tablet: 1, phone: 0 }}></Cell>
	<Cell spanDevices={{ desktop: 6, tablet: 6, phone: 4 }}>
    <div style="display:flex; justify-content: center; align-items: center;">
			<Button
				variant="outlined"
				style="width:100%; font-family: 'Roboto', sans-serif; font-weight: 500;"
				on:click={romanize}>
				{#if isRomanizing === true}
						<Label>Romanizing...</Label>
				{:else}
						<Label>Romanize</Label>
				{/if}
			</Button>
		 </div>
  </Cell>
	<Cell spanDevices={{ desktop: 3, tablet: 1, phone: 0 }}></Cell>
	
</LayoutGrid>